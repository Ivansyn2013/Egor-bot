#!/usr/bin/env python3
"""After agent turns that edited code, run project tests and report failures."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = Path(__file__).resolve().parent / ".pending-edits"
MAX_OUTPUT = 12000


def emit(obj: dict) -> None:
    print(json.dumps(obj, ensure_ascii=False))
    sys.stdout.flush()
    time.sleep(0.05)


def resolve_cmd() -> list[str]:
    venv_python = ROOT / "venv" / "bin" / "python"
    python = str(venv_python) if venv_python.exists() else sys.executable
    return [python, "-m", "pytest", "tests/", "-q", "--tb=short"]


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        emit({})
        return

    if (payload.get("status") or "completed") != "completed":
        emit({})
        return

    if not STATE.exists():
        emit({})
        return

    edited = sorted({line.strip() for line in STATE.read_text(encoding="utf-8").splitlines() if line.strip()})
    try:
        STATE.unlink(missing_ok=True)
    except OSError:
        pass

    if not edited:
        emit({})
        return

    cmd = resolve_cmd()
    try:
        result = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            timeout=280,
        )
    except subprocess.TimeoutExpired as exc:
        out = ((exc.stdout or "") + "\n" + (exc.stderr or ""))[-MAX_OUTPUT:]
        emit({
            "followup_message": (
                "Automated post-edit tests timed out.\n\n"
                f"Command: `{' '.join(cmd)}`\n\n"
                f"```text\n{out}\n```"
            )
        })
        return
    except Exception as exc:
        emit({
            "followup_message": (
                "Automated post-edit tests failed to start.\n\n"
                f"Error: {exc}\nPlease investigate and continue."
            )
        })
        return

    if result.returncode == 0:
        print(f"[run-tests-on-stop] OK ({len(edited)} file(s))", file=sys.stderr)
        emit({})
        return

    combined = (result.stdout or "") + ("\n" if result.stdout and result.stderr else "") + (result.stderr or "")
    combined = combined[-MAX_OUTPUT:]
    sample = "\n".join(f"- {p}" for p in edited[:20])
    emit({
        "followup_message": (
            "Automated checks failed after your code updates. Please fix the failures below, "
            "then continue. Do not claim success until tests pass.\n\n"
            f"**Command:** `{' '.join(cmd)}` (exit {result.returncode})\n\n"
            f"**Edited files (sample):**\n{sample}\n\n"
            f"```text\n{combined}\n```"
        )
    })


if __name__ == "__main__":
    main()
