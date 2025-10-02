"""Wrapper minimal autour de l’API OpenAI."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

try:
    import openai
except ModuleNotFoundError:  # pragma: no cover - dépendance optionnelle
    openai = None  # type: ignore


def ask_gpt(prompt: str, input_data: Optional[Dict[str, Any]] = None, *, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    """Envoie une requête à l’API OpenAI et retourne la réponse JSON.

    Si la librairie ``openai`` n’est pas installée ou si la clé d’API n’est pas
    définie, une ``RuntimeError`` est levée. Les appels sont normalisés pour
    retourner un dictionnaire Python.
    """

    if openai is None:
        raise RuntimeError("La librairie 'openai' n'est pas installée.")

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
