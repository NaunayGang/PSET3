"""Apply migrations and seed initial data.

Usage:
    python scripts/bootstrap_db.py
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    migrate_script = backend_root / "scripts" / "migrate.py"
    seed_script = backend_root / "scripts" / "seed_data.py"

    subprocess.run([sys.executable, str(migrate_script)], check=True, cwd=backend_root)
    subprocess.run([sys.executable, str(seed_script)], check=True, cwd=backend_root)
    print("✅ Database bootstrap completed.")


if __name__ == "__main__":
    main()