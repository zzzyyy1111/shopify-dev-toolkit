#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


SCHEMA_RE = re.compile(r"{%\s*schema\s*%}(.*?){%\s*endschema\s*%}", re.S)
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
TRAILING_COMMA_RE = re.compile(r",\s*([}\]])")


def load_json(path):
    return loads_jsonc(path.read_text(encoding="utf-8-sig"))


def loads_jsonc(text):
    return json.loads(TRAILING_COMMA_RE.sub(r"\1", COMMENT_RE.sub("", text)))


def finding(level, file, code, message, location=None):
    item = {"level": level, "file": file, "code": code, "message": message}
    if location:
        item["location"] = location
    return item


def setting_map(items, findings, rel, owner):
    result = {}
    seen = set()
    for setting in items or []:
        sid = setting.get("id") if isinstance(setting, dict) else None
        if not sid:
            continue
        if sid in seen:
            findings.append(finding("upload_blocking", rel, "DUPLICATE_SETTING_ID", f"Duplicate setting id '{sid}'", owner))
        seen.add(sid)
        result[sid] = setting
        validate_value(setting, setting.get("default"), findings, rel, f"{owner}.default.{sid}", default=True)
    return result


def validate_value(schema, value, findings, rel, location, default=False):
    if value is None:
        return
    kind = schema.get("type")
    prefix = "Default" if default else "Setting"
    if kind == "range" and isinstance(value, (int, float)):
        low, high = schema.get("min"), schema.get("max")
        if low is not None and value < low or high is not None and value > high:
            findings.append(finding("upload_blocking", rel, "RANGE_OUT_OF_BOUNDS", f"{prefix} '{schema.get('id')}' value {value} is outside {low}..{high}", location))
    if kind in {"select", "radio"}:
        allowed = [o.get("value") for o in schema.get("options", []) if isinstance(o, dict)]
        if allowed and value not in allowed:
            findings.append(finding("warning", rel, "INVALID_OPTION", f"{prefix} '{schema.get('id')}' value {value!r} is not in {allowed}", location))


def main():
    parser = argparse.ArgumentParser(description="Validate Shopify section schemas and JSON templates")
    parser.add_argument("theme_path")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    root = Path(args.theme_path).expanduser().resolve()
    findings, schemas = [], {}

    for required in ("layout", "templates", "sections", "snippets", "assets", "config", "locales"):
        if not (root / required).is_dir():
            findings.append(finding("fatal", required, "MISSING_DIRECTORY", f"Missing required directory: {required}"))
    if not (root / "layout" / "theme.liquid").is_file():
        findings.append(finding("fatal", "layout/theme.liquid", "MISSING_THEME_LAYOUT", "Missing layout/theme.liquid"))

    for path in sorted((root / "sections").glob("*.liquid")):
        rel = path.relative_to(root).as_posix()
        match = SCHEMA_RE.search(path.read_text(encoding="utf-8-sig"))
        if not match:
            continue
        try:
            schema = loads_jsonc(match.group(1))
        except Exception as exc:
            findings.append(finding("fatal", rel, "INVALID_SECTION_SCHEMA_JSON", str(exc)))
            continue
        section_settings = setting_map(schema.get("settings"), findings, rel, "section")
        block_schemas = {}
        for block in schema.get("blocks", []):
            if isinstance(block, dict) and block.get("type"):
                block_schemas[block["type"]] = setting_map(block.get("settings"), findings, rel, f"block.{block['type']}")
        schemas[path.stem] = {"settings": section_settings, "blocks": block_schemas}

    templates = root / "templates"
    for path in sorted(templates.glob("*.json")):
        rel = path.relative_to(root).as_posix()
        if ".context." in path.name:
            parent = path.name.split(".context.", 1)[0] + ".json"
            if not (templates / parent).is_file():
                findings.append(finding("upload_blocking", rel, "MISSING_CONTEXT_PARENT", f"Parent template does not exist: {parent}"))
        try:
            doc = load_json(path)
        except Exception as exc:
            findings.append(finding("fatal", rel, "INVALID_TEMPLATE_JSON", str(exc)))
            continue
        for section_id, instance in (doc.get("sections") or {}).items():
            if not isinstance(instance, dict) or instance.get("disabled") is True:
                continue
            stype = instance.get("type")
            if not stype:
                continue
            schema = schemas.get(stype)
            if schema is None:
                findings.append(finding("upload_blocking", rel, "UNKNOWN_SECTION_TYPE", f"Section type '{stype}' has no sections/{stype}.liquid", f"sections.{section_id}"))
                continue
            for sid, value in (instance.get("settings") or {}).items():
                rule = schema["settings"].get(sid)
                if rule:
                    validate_value(rule, value, findings, rel, f"sections.{section_id}.settings.{sid}")
            for block_id, block in (instance.get("blocks") or {}).items():
                btype = block.get("type") if isinstance(block, dict) else None
                rules = schema["blocks"].get(btype)
                if rules is None and isinstance(btype, str) and btype.startswith("shopify://apps/") and "@app" in schema["blocks"]:
                    rules = {}
                if rules is None:
                    findings.append(finding("upload_blocking", rel, "UNKNOWN_BLOCK_TYPE", f"Block type '{btype}' is not defined by section '{stype}'", f"sections.{section_id}.blocks.{block_id}"))
                    continue
                for sid, value in (block.get("settings") or {}).items():
                    rule = rules.get(sid)
                    if rule:
                        validate_value(rule, value, findings, rel, f"sections.{section_id}.blocks.{block_id}.settings.{sid}")

    counts = {level: sum(1 for x in findings if x["level"] == level) for level in ("fatal", "upload_blocking", "warning", "information")}
    result = {"ok": counts["fatal"] == 0 and counts["upload_blocking"] == 0, "theme_root": str(root), "counts": counts, "findings": findings}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_output:
        Path(args.json_output).write_text(text + "\n", encoding="utf-8")
    print(text)
    raise SystemExit(0 if result["ok"] else 2)


if __name__ == "__main__":
    main()
