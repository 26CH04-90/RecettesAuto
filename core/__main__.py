"""Entrée de secours pour le module core."""

from __future__ import annotations

from . import DATA_DIR


def main() -> None:
    print(f"Répertoire des données : {DATA_DIR}")


if __name__ == "__main__":
    main()
