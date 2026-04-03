"""Seed initial test users.

Usage:
    python scripts/seed_data.py
"""

from pathlib import Path
import sys

backend_root = Path(__file__).resolve().parents[1]
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from src.seed import seed_initial_users


if __name__ == "__main__":
    seed_initial_users()