"""Logique métier pour RecettesAuto."""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

__all__ = ["DATA_DIR"]
