"""Wrapper minimal autour de l’API OpenAI."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import openai
except ModuleNotFoundError:  # pragma: no cover - dépendance optionnelle
    openai = None  # type: ignore


_ENV_FILE_CANDIDATES = (
    Path(__file__).resolve().parents[1] / ".env",
    Path.cwd() / ".env",
)


def _ensure_env_loaded() -> None:
    """Charge les variables d'environnement depuis un fichier ``.env`` si présent."""

    if getattr(_ensure_env_loaded, "_loaded", False):  # type: ignore[attr-defined]
        return

    for candidate in _ENV_FILE_CANDIDATES:
        if not candidate.exists():
            continue
        try:
            content = candidate.read_text(encoding="utf-8")
        except OSError:
            continue

        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", maxsplit=1)
            key = key.strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            if key and key not in os.environ:
                os.environ[key] = value

    setattr(_ensure_env_loaded, "_loaded", True)


def ask_gpt(prompt: str, input_data: Optional[Dict[str, Any]] = None, *, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    """Envoie une requête à l’API OpenAI et retourne la réponse JSON.

    Si la librairie ``openai`` n’est pas installée ou si la clé d’API n’est pas
    définie, une ``RuntimeError`` est levée. Les appels sont normalisés pour
    retourner un dictionnaire Python.
    """

    if openai is None:
        raise RuntimeError("La librairie 'openai' n'est pas installée.")

    _ensure_env_loaded()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("La variable d'environnement OPENAI_API_KEY est absente.")

    client = openai.OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": "Tu es un assistant spécialisé en planification de menus."},
        {"role": "user", "content": prompt},
    ]

    if input_data:
        messages.append(
            {
                "role": "user",
                "content": json.dumps(input_data, ensure_ascii=False),
            }
        )

    response = client.responses.create(model=model, input=messages)

    if not response.output:
        raise RuntimeError("Réponse vide de l'API OpenAI.")

    # On extrait la première réponse textuelle disponible.
    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "text":
                    text = content.text
                    break
            else:
                continue
            break
    else:
        raise RuntimeError("Impossible de lire le contenu de la réponse OpenAI.")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}
