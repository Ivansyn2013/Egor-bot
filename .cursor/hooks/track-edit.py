#!/usr/bin/env python3
"""Record agent code edits so the stop hook can run tests."""
import json
import sys
import time
from pathlib import Path

STATE = Path(__file__).resolve().parent / ".pending-edits"
CODE_SUFFIXES = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".css", ".scss", ".html",
    ".sql", ".toml", ".yaml", ".yml", ".json",
}
SKIP_PARTS = {".cursor/hooks", "node_modules", "venv", ".venv", "__pycache__", "dist", "build"}


def is_code(path: Path) -> bool:
    text = str(path)
    if any(part in text for part in SKIP_PARTS):
        return False
    if path.suffix.lower() in CODE_SUFFIXES:
        return True
    name = path.name.lower()
    return name in {"requirements.txt", "package.json", "pyproject.toml", "main.py"}


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print("{}")
        return

    file_path = Path(payload.get("file_path") or "")
    if file_path and is_code(file_path):
        STATE.parent.mkdir(parents=True, exist_ok=True)
        with STATE.open("a", encoding="utf-8") as fh:
            fh.write(f"{file_path}\n")

    print("{}")
    sys.stdout.flush()
    time.sleep(0.05)


if __name__ == "__main__":
    main()
