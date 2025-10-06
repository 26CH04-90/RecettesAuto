"""Automatisation future du panier Coop via Playwright."""

from __future__ import annotations

from pathlib import Path
from typing import Dict


def load_courses_file(path: Path) -> Dict:
    """Charge le fichier `courses.json` (a utiliser par Playwright)."""

    import json

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    """Point d'entree futur pour l'automatisation Coop."""

    raise NotImplementedError("Automatisation Coop non implementee.")


if __name__ == "__main__":
    main()
