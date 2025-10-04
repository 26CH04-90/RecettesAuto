"""Gestion des menus hebdomadaires."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from . import DATA_DIR
from .config_manager import load_and_validate
from .gpt_api import ask_gpt

MENUS_PATH = DATA_DIR / "menus.json"


def get_week_identifier(for_date: date | None = None) -> str:
    """Retourne l'identifiant ISO (``YYYY-Www``) d'une semaine."""

    target_date = for_date or date.today()
    iso = target_date.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _parse_week_identifier(week_id: str) -> Tuple[int, int]:
    """Convertit un identifiant de semaine en tuple ``(année, semaine)``."""

    try:
        year_str, week_str = week_id.split("-W", maxsplit=1)
        return int(year_str), int(week_str)
    except (ValueError, AttributeError):  # pragma: no cover - defensive
        return (0, 0)


def _sorted_weeks(menus_by_week: Dict[str, Any]) -> List[str]:
    """Retourne les identifiants de semaines triés chronologiquement."""

    return sorted(menus_by_week.keys(), key=_parse_week_identifier, reverse=True)


def _select_recent_weeks(
    menus_by_week: Dict[str, Any],
    weeks_to_consult: int,
    current_week: str,
) -> List[str]:
    """Sélectionne les ``weeks_to_consult`` semaines précédentes disponibles."""

    if weeks_to_consult <= 0:
        return []

    ordered_weeks = [week for week in _sorted_weeks(menus_by_week) if week != current_week]
    return ordered_weeks[:weeks_to_consult]


def _collect_titles(menus: Iterable[Dict[str, Any]]) -> List[str]:
    """Extrait la liste dédoublonnée des titres de menus fournis."""

    titles = set()
    for week_menus in menus:
        if not isinstance(week_menus, dict):
            continue
        for entry in week_menus.values():
            if not isinstance(entry, dict):
                continue
            titre = entry.get("Titre")
            if titre:
                titles.add(titre)
    return sorted(titles)


def load_menus(path: Path | None = None, *, week_id: str | None = None) -> Dict[str, Any]:
    """Retourne le contenu du fichier ``menus.json``."""

    target_path = path or MENUS_PATH
    if not target_path.exists():
        return {}
    with target_path.open("r", encoding="utf-8") as file:
        menus: Dict[str, Any] = json.load(file)

    if week_id is None:
        return menus

    week_menus = menus.get(week_id)
    return week_menus if isinstance(week_menus, dict) else {}


def save_menus(menus: Dict[str, Any], path: Path | None = None) -> None:
    """Enregistre les menus dans ``menus.json``."""

    target_path = path or MENUS_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w", encoding="utf-8") as file:
        json.dump(menus, file, ensure_ascii=False, indent=2)


def update_menu_state(
    menu_id: str, state: str, *, week_id: str | None = None, path: Path | None = None
) -> Dict[str, Any]:
    """Met à jour l’état d’un repas (proposé, validé, refusé, etc.)."""

    menus_by_week = load_menus(path)
    target_week = week_id or get_week_identifier()
    if target_week not in menus_by_week or not isinstance(menus_by_week[target_week], dict):
        raise KeyError(f"La semaine '{target_week}' est introuvable.")

    week_menus = menus_by_week[target_week]
    if menu_id not in week_menus:
        raise KeyError(f"Le menu '{menu_id}' est introuvable pour la semaine '{target_week}'.")

    week_menus[menu_id]["État"] = state
    save_menus(menus_by_week, path)
    return week_menus


def generate_menus(*, prompt: str | None = None, path: Path | None = None) -> Dict[str, Any]:
    """Génère de nouveaux menus via GPT et les enregistre."""

    config = load_and_validate()
    menus_by_week = load_menus(path)
    current_week = get_week_identifier()

    weeks_to_consult = (
        config.get("options", {}).get("semaines_historique")
        if isinstance(config.get("options", {}), dict)
        else None
    )
    weeks_to_consult = weeks_to_consult if isinstance(weeks_to_consult, int) else 0
    previous_weeks = _select_recent_weeks(menus_by_week, weeks_to_consult, current_week)
    previous_menus = [menus_by_week[week] for week in previous_weeks]

    if weeks_to_consult > 0:
        default_prompt = (
            "Propose un menu hebdomadaire en JSON pour {nb} personnes en respectant les régimes "
            "et préférences fournis. Évite de répéter les plats servis durant les {nb_semaines} "
            "dernières semaines. Réponds uniquement avec du JSON."
        )
    else:
        default_prompt = (
            "Propose un menu hebdomadaire en JSON pour {nb} personnes en respectant les régimes "
            "et préférences fournis. Réponds uniquement avec du JSON."
        )

    base_prompt = (prompt or default_prompt).format(
        nb=config["nombre_personnes"],
        nb_semaines=weeks_to_consult,
    )

    payload = {
        "config": config,
        "semaine_courante": current_week,
        "menus_existants": menus_by_week.get(current_week, {}),
        "historique_menus": {week: menus_by_week[week] for week in previous_weeks},
        "historique_plats": _collect_titles(previous_menus),
    }

    response = ask_gpt(base_prompt, payload)

    if not isinstance(response, dict):
        raise RuntimeError("Le format de la réponse GPT est inattendu.")

    menus: Dict[str, Any]
    if "menus" in response and isinstance(response["menus"], dict):
        menus = response["menus"]
    else:
        menus = response

    menus_by_week[current_week] = menus
    save_menus(menus_by_week, path)
    return menus


def list_menu_states(menus: Dict[str, Any]) -> List[str]:
    """Retourne la liste des états distincts présents dans les menus."""

    states = set()

    def _walk(entries: Dict[str, Any]) -> None:
        for value in entries.values():
            if isinstance(value, dict):
                if "État" in value:
                    states.add(value.get("État", ""))
                else:
                    _walk(value)

    _walk(menus)
    states.discard("")
    return sorted(states)
