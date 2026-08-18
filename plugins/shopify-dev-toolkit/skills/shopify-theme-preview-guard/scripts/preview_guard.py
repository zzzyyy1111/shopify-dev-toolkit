#!/usr/bin/env python3
"""Preview-only Shopify theme executor with no publication code path."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_DIRS = {"assets", "config", "layout", "sections", "snippets", "templates"}
FORBIDDEN_FLAGS = {"--publish", "--live", "--allow-live"}
PROTECTED_UPDATE_FILES = {"config/settings_data.json", "config/markets.json"}
STORE_PATTERN = re.compile(r"^(?:[a-z0-9][a-z0-9-]*|[a-z0-9][a-z0-9-]*\.myshopify\.com)$", re.I)
THEME_ID_PATTERN = re.compile(r"^[1-9][0-9]*$")


def normalize_store(value: str) -> str:
    store = re.sub(r"^https?://", "", value.strip().lower()).rstrip("/")
    if not STORE_PATTERN.fullmatch(store):
        raise ValueError("Store must be a store handle or a .myshopify.com domain.")
    return store


def normalize_theme_id(value: str) -> str:
    theme_id = value.strip()
    if not THEME_ID_PATTERN.fullmatch(theme_id):
        raise ValueError("Theme ID must be a positive numeric ID.")
    return theme_id


def inspect_theme(path_value: str) -> dict:
    path = Path(path_value).expanduser().resolve()
    present = {item.name for item in path.iterdir() if item.is_dir()} if path.is_dir() else set()
    missing = sorted(REQUIRED_DIRS - present)
    recognizable = not missing and (path / "layout" / "theme.liquid").is_file()
    git = {"is_worktree": False, "branch": None, "dirty_files": []}
    if path.is_dir():
        root = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        if root.returncode == 0:
            git["is_worktree"] = True
            branch = subprocess.run(["git", "-C", str(path), "branch", "--show-current"], capture_output=True, text=True)
            status = subprocess.run(["git", "-C", str(path), "status", "--porcelain", "--untracked-files=all"], capture_output=True, text=True)
            git["branch"] = branch.stdout.strip() or None
            git["dirty_files"] = [line[3:].strip().replace("\\", "/") for line in status.stdout.splitlines() if len(line) >= 4]
    return {
        "path": str(path),
        "recognizable_theme": recognizable,
        "missing_required_directories": missing,
        "has_theme_liquid": (path / "layout" / "theme.liquid").is_file(),
        "has_settings_data": (path / "config" / "settings_data.json").is_file(),
        "git": git,
    }


def resolve_shopify() -> str | None:
    return shutil.which("shopify") or shutil.which("shopify.cmd")


def assert_safe_command(command: list[str], allow_theme_id: bool = False) -> None:
    lowered = [part.lower() for part in command]
    if any(flag in lowered for flag in FORBIDDEN_FLAGS) or lowered[1:3] == ["theme", "publish"]:
        raise RuntimeError("Safety invariant failed: publication command or flag detected.")
    if not allow_theme_id and "--theme" in lowered:
        raise RuntimeError("Safety invariant failed: Theme ID targeting is not allowed for this action.")


def build_preview_command(action: str, shopify: str, theme_path: str, store: str) -> list[str]:
    if action == "dev":
        command = [shopify, "theme", "dev", "--path", theme_path, "--store", store]
    elif action == "unpublished":
        command = [shopify, "theme", "push", "--unpublished", "--strict", "--json", "--path", theme_path, "--store", store]
    else:
        raise ValueError(f"Unsupported preview action: {action}")
    assert_safe_command(command)
    return command


def build_role_check_command(shopify: str, theme_path: str, store: str, theme_id: str) -> list[str]:
    command = [shopify, "theme", "list", "--id", theme_id, "--role", "unpublished", "--json", "--path", theme_path, "--store", store]
    assert_safe_command(command)
    return command


def load_update_manifest(manifest_value: str, theme_path: str, theme_id: str) -> list[str]:
    manifest_path = Path(manifest_value).expanduser().resolve()
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if payload.get("reviewed") is not True:
        raise ValueError("Update manifest must contain reviewed: true.")
    if normalize_theme_id(str(payload.get("theme_id", ""))) != theme_id:
        raise ValueError("Manifest Theme ID does not match the requested Theme ID.")
    files = payload.get("files")
    if not isinstance(files, list) or not files:
        raise ValueError("Update manifest must contain a non-empty files array.")
    root = Path(theme_path).resolve()
    safe_files = []
    for raw in files:
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError("Every manifest file must be a non-empty relative path.")
        rel = raw.strip().replace("\\", "/")
        if rel.startswith("/") or re.match(r"^[A-Za-z]:", rel) or ".." in Path(rel).parts or any(char in rel for char in "*?[]"):
            raise ValueError(f"Unsafe manifest path: {raw}")
        if rel.lower() in PROTECTED_UPDATE_FILES:
            raise ValueError(f"Protected configuration file cannot be uploaded to an existing theme: {rel}")
        resolved = (root / rel).resolve()
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"Manifest path escapes theme root: {rel}") from exc
        if not resolved.is_file():
            raise ValueError(f"Manifest file does not exist locally: {rel}")
        if rel not in safe_files:
            safe_files.append(rel)
    return safe_files


def build_update_command(shopify: str, theme_path: str, store: str, theme_id: str, files: list[str]) -> list[str]:
    command = [shopify, "theme", "push", "--theme", theme_id, "--strict", "--json", "--nodelete", "--path", theme_path, "--store", store]
    for rel in files:
        command.extend(["--only", rel])
    assert_safe_command(command, allow_theme_id=True)
    return command


def themes_from_json(text: str) -> list[dict]:
    payload = json.loads(text)
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        if isinstance(payload.get("themes"), list):
            return [item for item in payload["themes"] if isinstance(item, dict)]
        if isinstance(payload.get("theme"), dict):
            return [payload["theme"]]
        if "id" in payload:
            return [payload]
    return []


def verify_role_check(text: str, theme_id: str) -> dict:
    matches = [theme for theme in themes_from_json(text) if str(theme.get("id")) == theme_id and str(theme.get("role", "")).lower() == "unpublished"]
    if len(matches) != 1:
        raise RuntimeError("Theme ID was not uniquely verified as unpublished. Update blocked.")
    return matches[0]


def verify_push_output(text: str, expected_id: str | None = None) -> dict:
    themes = themes_from_json(text)
    if len(themes) != 1:
        raise RuntimeError("Shopify response did not contain exactly one theme.")
    theme = themes[0]
    if str(theme.get("role", "")).lower() != "unpublished":
        raise RuntimeError("Shopify response was not verified as an unpublished theme.")
    if expected_id and str(theme.get("id")) != expected_id:
        raise RuntimeError("Shopify response Theme ID does not match the approved Theme ID.")
    if not theme.get("id") or not theme.get("preview_url"):
        raise RuntimeError("Shopify response is missing theme ID or preview URL.")
    return theme


def base_inspection(action: str, theme_path: str, store_value: str, command: list[str] | None) -> dict:
    theme = inspect_theme(theme_path)
    store = normalize_store(store_value)
    shopify = resolve_shopify()
    errors = []
    warnings = []
    if not theme["recognizable_theme"]:
        errors.append("Path is not a recognizable Shopify theme.")
    if not shopify:
        warnings.append("Shopify CLI is not available on PATH; inspection can continue but execution cannot.")
    if not theme["git"]["is_worktree"]:
        warnings.append("Theme is not in a Git worktree; rollback evidence is limited.")
    if theme["git"]["dirty_files"]:
        warnings.append("Theme contains local changes; preserve them and verify they are intended for preview.")
    if not theme["has_settings_data"]:
        warnings.append("config/settings_data.json is missing; preview configuration may not match the store.")
    return {
        "ok": not errors,
        "action": action,
        "store": store,
        "theme": theme,
        "shopify_cli": shopify,
        "safe_command": command,
        "errors": errors,
        "warnings": warnings,
        "live_theme_capability": False,
    }


def run_captured(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True)


def self_test() -> int:
    dev = build_preview_command("dev", "shopify", "C:/theme", "test-store")
    draft = build_preview_command("unpublished", "shopify", "C:/theme", "test-store")
    role = build_role_check_command("shopify", "C:/theme", "test-store", "123")
    update = build_update_command("shopify", "C:/theme", "test-store", "123", ["assets/test.css"])
    assertions = [
        dev[1:3] == ["theme", "dev"],
        draft[1:3] == ["theme", "push"] and "--unpublished" in draft,
        role[1:3] == ["theme", "list"] and "--role" in role,
        update[1:3] == ["theme", "push"] and "--theme" in update and "--only" in update,
        all(flag not in [part.lower() for part in command] for command in (dev, draft, role, update) for flag in FORBIDDEN_FLAGS),
        verify_role_check('[{"id":123,"role":"unpublished"}]', "123")["id"] == 123,
        verify_push_output('{"theme":{"id":123,"role":"unpublished","preview_url":"https://example"}}', "123")["id"] == 123,
    ]
    if not all(assertions):
        raise RuntimeError("Preview guard self-test failed.")
    print(json.dumps({"ok": True, "publish_capability": False, "allowed_actions": ["inspect", "dev", "unpublished", "update-unpublished"]}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("self-test")
    for action in ("inspect", "dev", "unpublished"):
        sub = subparsers.add_parser(action)
        sub.add_argument("--theme-path", required=True)
        sub.add_argument("--store", required=True)
        if action != "inspect":
            sub.add_argument("--execute", action="store_true")
    update = subparsers.add_parser("update-unpublished")
    update.add_argument("--theme-path", required=True)
    update.add_argument("--store", required=True)
    update.add_argument("--theme-id", required=True)
    update.add_argument("--files-manifest", required=True)
    update.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    if args.action == "self-test":
        return self_test()

    theme = inspect_theme(args.theme_path)
    store = normalize_store(args.store)
    shopify = resolve_shopify() or "shopify"

    if args.action == "inspect":
        command = build_preview_command("dev", shopify, theme["path"], store)
        result = base_inspection("inspect", theme["path"], store, command)
        result["executed"] = False
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["ok"] else 2

    if args.action in {"dev", "unpublished"}:
        command = build_preview_command(args.action, shopify, theme["path"], store)
        result = base_inspection(args.action, theme["path"], store, command)
        if not args.execute or not result["ok"] or not result["shopify_cli"]:
            result["executed"] = False
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0 if result["ok"] and not args.execute else 2
        completed = subprocess.run(command, capture_output=args.action == "unpublished", text=True)
        if completed.returncode != 0:
            if completed.stdout:
                print(completed.stdout)
            if completed.stderr:
                print(completed.stderr, file=sys.stderr)
            return completed.returncode
        if args.action == "unpublished":
            remote_theme = verify_push_output(completed.stdout)
            print(json.dumps({"ok": True, "state": "unpublished_review_theme_created", "theme": remote_theme, "live_theme_capability": False}, indent=2, ensure_ascii=False))
        return 0

    theme_id = normalize_theme_id(args.theme_id)
    files = load_update_manifest(args.files_manifest, theme["path"], theme_id)
    role_command = build_role_check_command(shopify, theme["path"], store, theme_id)
    push_command = build_update_command(shopify, theme["path"], store, theme_id, files)
    result = base_inspection("update-unpublished", theme["path"], store, push_command)
    result["role_check_command"] = role_command
    result["approved_files"] = files
    if not args.execute or not result["ok"] or not result["shopify_cli"]:
        result["executed"] = False
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["ok"] and not args.execute else 2

    checked = run_captured(role_command)
    if checked.returncode != 0:
        print(checked.stderr or checked.stdout, file=sys.stderr)
        return checked.returncode
    verified = verify_role_check(checked.stdout, theme_id)
    pushed = run_captured(push_command)
    if pushed.returncode != 0:
        print(pushed.stderr or pushed.stdout, file=sys.stderr)
        return pushed.returncode
    remote_theme = verify_push_output(pushed.stdout, theme_id)
    print(json.dumps({
        "ok": True,
        "state": "existing_unpublished_theme_updated",
        "verified_before_upload": verified,
        "theme": remote_theme,
        "uploaded_files": files,
        "live_theme_capability": False,
    }, indent=2, ensure_ascii=False))
    return 0


def blocked_reason(exc: Exception) -> str:
    message = str(exc).lower()
    if "not uniquely verified as unpublished" in message or "not verified as an unpublished" in message:
        return "TARGET_NOT_UNPUBLISHED"
    if "manifest" in message or "unsafe" in message or "protected configuration" in message:
        return "UNSAFE_MANIFEST"
    if "theme id" in message:
        return "INVALID_THEME_ID"
    if "store" in message:
        return "INVALID_STORE"
    if "publication" in message:
        return "PUBLISH_FORBIDDEN"
    return "PREVIEW_GUARD_ERROR"


def entrypoint() -> int:
    try:
        return main()
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        report = {
            "ok": False,
            "status": "blocked",
            "reason_code": blocked_reason(exc),
            "reason": str(exc),
            "local_files_changed": False,
            "remote_shopify_state_changed": False,
            "safest_next_step": "Correct the reported input or verification failure, run inspect again, and do not publish the theme.",
            "live_theme_capability": False,
        }
        print(json.dumps(report, indent=2, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(entrypoint())
