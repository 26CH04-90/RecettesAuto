"""Gestion de la liste de courses."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from . import DATA_DIR
from .config_manager import load_and_validate
from .gpt_api import ask_gpt
from .menu_manager import load_menus
from .stock_manager import load_stock

COURSES_PATH = DATA_DIR / "courses.json"


def load_courses(path: Path | None = None) -> Dict[str, Any]:
    """Charge la liste de courses existante."""

    target_path = path or COURSES_PATH
    if not target_path.exists():
        return {}
    with target_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_courses(courses: Dict[str, Any], path: Path | None = None) -> None:
    """Enregistre la liste de courses."""

    target_path = path or COURSES_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w", encoding="utf-8") as file:
        json.dump(courses, file, ensure_ascii=False, indent=2)


def generate_courses(*, path: Path | None = None) -> Dict[str, Any]:
    """Demande à GPT de produire une nouvelle liste de courses."""

    config = load_and_validate()
    menus = load_menus()
    stock = load_stock()

    prompt = (
        "À partir des menus validés, du stock disponible et de la configuration, génère la liste des ingrédients "
        "à acheter. Réponds uniquement avec du JSON structuré."
    )

    payload = {
        "config": config,
        "menus": menus,
        "stock": stock,
    }

    response = ask_gpt(prompt, payload)
    if not isinstance(response, dict):
        raise RuntimeError("Le format de la réponse GPT est inattendu.")

    save_courses(response, path)
    return response
