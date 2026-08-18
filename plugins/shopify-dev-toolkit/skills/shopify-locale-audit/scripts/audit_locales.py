#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"{{\s*[^}]+\s*}}|%\{[^}]+\}")
LIQUID_T_RE = re.compile(r"['\"]([^'\"]+)['\"]\s*\|\s*t\b")
SCHEMA_T_RE = re.compile(r"['\"]t:([^'\"]+)['\"]")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
TRAILING_COMMA_RE = re.compile(r",\s*([}\]])")


def flatten(value, prefix=""):
    out = {}
    if isinstance(value, dict):
        for key, child in value.items():
            name = f"{prefix}.{key}" if prefix else key
            out.update(flatten(child, name))
    else:
        out[prefix] = value
    return out


def placeholders(value):
    return sorted(set(PLACEHOLDER_RE.findall(value))) if isinstance(value, str) else []


def main():
    parser = argparse.ArgumentParser(description="Audit Shopify locale JSON files")
    parser.add_argument("theme_path")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    root = Path(args.theme_path).expanduser().resolve()
    locale_dir = root / "locales"
    findings, documents = [], {}

    for path in sorted(locale_dir.glob("*.json")):
        rel = path.relative_to(root).as_posix()
        try:
            text = COMMENT_RE.sub("", path.read_text(encoding="utf-8-sig"))
            documents[path.name] = flatten(json.loads(TRAILING_COMMA_RE.sub(r"\1", text)))
        except Exception as exc:
            findings.append({"level": "fatal", "file": rel, "code": "INVALID_LOCALE_JSON", "message": str(exc)})

    groups = {
        "storefront": [n for n in documents if ".schema." not in n],
        "schema": [n for n in documents if ".schema." in n],
    }
    for group, names in groups.items():
        defaults = [n for n in names if ".default" in n]
        if len(defaults) != 1:
            findings.append({"level": "fatal", "file": "locales", "code": "AMBIGUOUS_DEFAULT_LOCALE", "message": f"{group} requires exactly one default locale; found {defaults}"})
            continue
        default_name = defaults[0]
        baseline = documents[default_name]
        for name in names:
            if name == default_name:
                continue
            current = documents[name]
            for key in sorted(baseline.keys() - current.keys()):
                findings.append({"level": "warning", "file": f"locales/{name}", "code": "MISSING_KEY", "key": key, "message": f"Missing key from {default_name}"})
            for key in sorted(current.keys() - baseline.keys()):
                findings.append({"level": "information", "file": f"locales/{name}", "code": "EXTRA_KEY", "key": key, "message": f"Key is absent from {default_name}"})
            for key in sorted(baseline.keys() & current.keys()):
                expected, actual = placeholders(baseline[key]), placeholders(current[key])
                if expected != actual:
                    findings.append({"level": "warning", "file": f"locales/{name}", "code": "PLACEHOLDER_MISMATCH", "key": key, "message": f"Expected placeholders {expected}, found {actual}"})

    storefront_default = next((documents[n] for n in groups["storefront"] if ".default" in n), {})
    schema_default = next((documents[n] for n in groups["schema"] if ".default" in n), {})
    storefront_used, schema_used = set(), set()
    for folder in ("layout", "sections", "snippets", "templates"):
        for path in (root / folder).rglob("*") if (root / folder).exists() else []:
            if path.is_file() and path.suffix in {".liquid", ".json"}:
                text = path.read_text(encoding="utf-8-sig", errors="replace")
                storefront_used.update(LIQUID_T_RE.findall(text))
                schema_used.update(SCHEMA_T_RE.findall(text))
    for key in sorted(storefront_used - storefront_default.keys()):
        findings.append({"level": "warning", "file": "theme code", "code": "MISSING_DEFAULT_KEY", "key": key, "message": "Translation key is used but absent from the default storefront locale"})
    for key in sorted(schema_used - schema_default.keys()):
        findings.append({"level": "warning", "file": "theme schema", "code": "MISSING_DEFAULT_SCHEMA_KEY", "key": key, "message": "Schema translation key is used but absent from the default schema locale"})

    counts = {level: sum(1 for x in findings if x["level"] == level) for level in ("fatal", "warning", "information")}
    result = {"ok": counts["fatal"] == 0, "theme_root": str(root), "counts": counts, "findings": findings}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_output:
        Path(args.json_output).write_text(text + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result["ok"] else 2)


if __name__ == "__main__":
    main()
