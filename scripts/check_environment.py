#!/usr/bin/env python3
"""Check the local runtime required by product-detail-page-maker."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ASSEMBLER = ROOT / "scripts" / "assemble_detail_modules.py"
MIN_PYTHON = (3, 10)


def print_result(ok: bool, label: str, detail: str) -> None:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {label}: {detail}")


def main() -> int:
    failures: list[str] = []

    python_ok = sys.version_info >= MIN_PYTHON
    python_version = ".".join(str(part) for part in sys.version_info[:3])
    print_result(python_ok, "Python", python_version)
    if not python_ok:
        failures.append("Python 3.10 or newer is required.")

    pillow_spec = importlib.util.find_spec("PIL")
    pillow_ok = pillow_spec is not None
    pillow_detail = "installed"
    if pillow_ok:
        from PIL import __version__ as pillow_version

        pillow_detail = pillow_version
    else:
        pillow_detail = "not installed"
        failures.append("Pillow is required.")
    print_result(pillow_ok, "Pillow", pillow_detail)

    assembler_exists = ASSEMBLER.is_file()
    print_result(assembler_exists, "Assembler script", str(ASSEMBLER))
    if not assembler_exists:
        failures.append("scripts/assemble_detail_modules.py is missing.")

    assembler_ok = False
    if python_ok and pillow_ok and assembler_exists:
        result = subprocess.run(
            [sys.executable, str(ASSEMBLER), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        assembler_ok = result.returncode == 0
        detail = "command loaded successfully" if assembler_ok else result.stderr.strip()
        print_result(assembler_ok, "Assembler command", detail)
        if not assembler_ok:
            failures.append("The assembler command could not start.")

    if failures:
        print("\nEnvironment check failed:")
        for failure in failures:
            print(f"- {failure}")
        print("\nInstall the Python dependency with:")
        print(f'  "{sys.executable}" -m pip install -r "{ROOT / "requirements.txt"}"')
        print("Then run this check again.")
        return 1

    print("\nEnvironment check passed. The stitching and compression script is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
