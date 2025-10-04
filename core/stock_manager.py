"""Utilitaires pour la gestion du stock."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from . import DATA_DIR

STOCK_PATH = DATA_DIR / "stock.json"


def load_stock(path: Path | None = None) -> Dict[str, Any]:
    """Charge le stock depuis le fichier JSON."""

    target_path = path or STOCK_PATH
    with target_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_stock(stock: Dict[str, Any], path: Path | None = None) -> None:
    """Enregistre le stock dans le fichier JSON."""

    target_path = path or STOCK_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w", encoding="utf-8") as file:
        json.dump(stock, file, ensure_ascii=False, indent=2)


def update_item(category: str, item: str, quantity: float, *, path: Path | None = None) -> Dict[str, Any]:
    """Met à jour la quantité d’un produit dans le stock."""

    stock = load_stock(path)
    stock.setdefault(category, {})[item] = quantity
    save_stock(stock, path)
    return stock
