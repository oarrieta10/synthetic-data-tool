"""app — workbench for building synthetic warehouse clients.

    python -m synthtool.app        (opens http://localhost:8502)

Needs the optional extra: pip install -e .[app]
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # repo root: profiles/, data/
