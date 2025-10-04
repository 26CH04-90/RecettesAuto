"""Point d'entree principal pour RecettesAuto."""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from core.config_manager import ConfigValidationError, load_and_validate
from core.courses_manager import generate_courses, load_courses
from core.menu_manager import generate_menus, list_menu_states, load_menus


def _print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def handle_config(_: argparse.Namespace) -> int:
    try:
        config = load_and_validate()
    except ConfigValidationError as error:
        print("Configuration invalide :")
        for message in error.errors:
            print(f" - {message}")
        return 1

    _print_json(config)
    return 0


def handle_menus(args: argparse.Namespace) -> int:
    try:
        menus = generate_menus() if args.generate else load_menus()
    except ConfigValidationError as error:
        print("Impossible de générer les menus : configuration invalide.")
        for message in error.errors:
            print(f" - {message}")
        return 1
    except RuntimeError as error:
        print(f"Erreur lors de l'appel GPT : {error}")
        return 1

    if not menus:
        print("Aucun menu disponible.")
        return 0

    _print_json(menus)
    if not args.generate:
        states = list_menu_states(menus)
        print("\nEtats presents :", ", ".join(states))
    return 0


def handle_courses(args: argparse.Namespace) -> int:
    try:
        courses = generate_courses() if args.generate else load_courses()
    except ConfigValidationError as error:
        print("Impossible de générer les courses : configuration invalide.")
        for message in error.errors:
            print(f" - {message}")
        return 1
    except RuntimeError as error:
        print(f"Erreur lors de l'appel GPT : {error}")
        return 1

    if not courses:
        print("Aucune course disponible.")
        return 0

    _print_json(courses)
    return 0


COMMAND_HANDLERS = {
    "config": handle_config,
    "menus": handle_menus,
    "courses": handle_courses,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Automatisation des menus et courses")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("config", help="Afficher la configuration")

    menus_parser = subparsers.add_parser("menus", help="Afficher ou générer les menus")
    menus_parser.add_argument("--generate", action="store_true", help="Générer via GPT")

    courses_parser = subparsers.add_parser("courses", help="Afficher ou générer les courses")
    courses_parser.add_argument("--generate", action="store_true", help="Générer via GPT")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = COMMAND_HANDLERS[args.command]
    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
