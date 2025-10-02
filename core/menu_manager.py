"""Gestion des menus hebdomadaires."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from . import DATA_DIR
from .config_manager import load_and_validate
from .gpt_api import ask_gpt

MENUS_PATH = DATA_DIR / "menus.json"


def load_menus(path: Path | None = None) -> Dict[str, Any]:
    """Retourne le contenu du fichier ``menus.json``."""

    target_path = path or MENUS_PATH
    if not target_path.exists():
        return {}
    with target_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_menus(menus: Dict[str, Any], path: Path | None = None) -> None:
    """Enregistre les menus dans ``menus.json``."""

    target_path = path or MENUS_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w", encoding="utf-8") as file:
        json.dump(menus, file, ensure_ascii=False, indent=2)


def update_menu_state(menu_id: str, state: str, *, path: Path | None = None) -> Dict[str, Any]:
    """Met à jour l’état d’un repas (proposé, validé, refusé, etc.)."""

    menus = load_menus(path)
    if menu_id not in menus:
        raise KeyError(f"Le menu '{menu_id}' est introuvable.")
    menus[menu_id]["État"] = state
    save_menus(menus, path)
    return menus


def generate_menus(*, prompt: str | None = None, path: Path | None = None) -> Dict[str, Any]:
    """Génère de nouveaux menus via GPT et les enregistre."""

    config = load_and_validate()
    current_menus = load_menus(path)

    base_prompt = prompt or (
        "Propose un menu hebdomadaire en JSON pour {nb} personnes en respectant les régimes "
        "et préférences fournis. Réponds uniquement avec du JSON."
    ).format(nb=config["nombre_personnes"])

    payload = {
        "config": config,
        "menus_existants": current_menus,
    }

    response = ask_gpt(base_prompt, payload)

    if not isinstance(response, dict):
        raise RuntimeError("Le format de la réponse GPT est inattendu.")

    menus: Dict[str, Any]
    if "menus" in response and isinstance(response["menus"], dict):
        menus = response["menus"]
    else:
        menus = response

    save_menus(menus, path)
    return menus


def list_menu_states(menus: Dict[str, Any]) -> List[str]:
    """Retourne la liste des états distincts présents dans les menus."""

    return sorted({entry.get("État", "") for entry in menus.values()})
