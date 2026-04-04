"""Run Alembic migrations to the latest revision.

Usage:
    python scripts/migrate.py
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    command = [sys.executable, "-m", "alembic", "upgrade", "head"]
    subprocess.run(command, check=True, cwd=backend_root)
    print("✅ Database migrations applied successfully.")


if __name__ == "__main__":
    main()