"""Gestion du fichier de configuration `config.json`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from . import DATA_DIR

CONFIG_PATH = DATA_DIR / "config.json"


class ConfigValidationError(Exception):
    """Exception levée lorsque la configuration est invalide."""

    def __init__(self, errors: List[str]) -> None:
        super().__init__("Configuration invalide")
        self.errors = errors


def load_config(path: Path | None = None) -> Dict[str, Any]:
    """Charge le fichier de configuration JSON.

    Parameters
    ----------
    path:
        Chemin optionnel vers le fichier de configuration. Par défaut ``CONFIG_PATH``.

    Returns
    -------
    dict
        Dictionnaire représentant la configuration.
    """

    target_path = path or CONFIG_PATH
    with target_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_config(config: Dict[str, Any], path: Path | None = None) -> None:
    """Écrit le fichier de configuration JSON."""

    target_path = path or CONFIG_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)


def validate_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Valide la structure minimale attendue de la configuration.

    Pour l’instant, seules quelques vérifications de base sont effectuées. Cette
    fonction pourra être enrichie lorsque le schéma sera stabilisé.
    """

    errors: List[str] = []

    if not isinstance(config, dict):
        errors.append("La configuration doit être un objet JSON.")
        return False, errors

    if "nombre_personnes" not in config:
        errors.append("Le champ 'nombre_personnes' est obligatoire.")
    elif not isinstance(config["nombre_personnes"], int) or config["nombre_personnes"] <= 0:
        errors.append("'nombre_personnes' doit être un entier strictement positif.")

    for section in ("regimes", "preferences", "options", "achats"):
        if section in config and not isinstance(config[section], dict):
            errors.append(f"La section '{section}' doit être un objet JSON.")

    return not errors, errors


def load_and_validate(path: Path | None = None) -> Dict[str, Any]:
    """Charge la configuration puis valide sa structure."""

    config = load_config(path)
    is_valid, errors = validate_config(config)
    if not is_valid:
        raise ConfigValidationError(errors)
    return config
