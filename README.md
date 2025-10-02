# 🥘 RecettesAuto

RecettesAuto automatise la planification des repas, le suivi du stock alimentaire, la génération de la liste de courses et, à terme, le remplissage du panier sur Coop.ch.

## 📦 Contenu du dépôt

```
RecettesAuto/
├── data/
│   ├── config.json
│   ├── courses.json
│   ├── menus.json
│   └── stock.json
├── core/
│   ├── config_manager.py
│   ├── courses_manager.py
│   ├── gpt_api.py
│   ├── menu_manager.py
│   └── stock_manager.py
├── coop_agent/
│   └── coop_playwright.py
├── main.py
└── requirements.txt
```

- **`data/`** : fichiers JSON utilisés par l’application.
- **`core/`** : logique métier (gestion de la config, du stock, des menus et des courses, + wrapper OpenAI).
- **`coop_agent/`** : futur script Playwright pour automatiser l’ajout au panier Coop.ch.
- **`main.py`** : point d’entrée orchestrant l’ensemble du workflow.
- **`requirements.txt`** : dépendances Python.

## ⚙️ Workflow

1. **Configuration** (`data/config.json`)
   - Nombre de personnes, régimes, préférences, contraintes d’achat.
   - Nouveau paramètre `options.semaines_historique` pour définir combien de semaines
     récentes sont consultées afin d’éviter les répétitions de plats.
2. **Menus** (`data/menus.json`)
   - Génération via l’API GPT en tenant compte de l’historique.
   - Validation/refus des propositions.
3. **Stock** (`data/stock.json`)
   - Tenir à jour les ingrédients disponibles (Raccourcis iOS, etc.).
4. **Courses** (`data/courses.json`)
   - Calcul des ingrédients manquants en fonction des menus validés.
5. **Panier Coop** (`coop_agent/coop_playwright.py`)
   - Automatisation optionnelle (à venir).

## 🚀 Démarrage rapide

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## 📱 Intégration Raccourcis iOS

- **Modifier le stock** : met à jour `data/stock.json`.
- **Valider les menus** : change l’état des repas (proposé, validé, refusé).
- **Générer les courses** : (à venir) appel à l’API GPT puis écriture de `data/courses.json`.

## 🗂️ Historique des menus

- Le fichier `data/menus.json` est désormais organisé par semaine (format `YYYY-Www`).
- Chaque génération crée une nouvelle entrée sans écraser les précédentes, ce qui permet
  de conserver un historique complet.
- Lors de la génération, RecettesAuto consulte automatiquement les `semaines_historique`
  dernières semaines définies dans la configuration pour éviter de reproposer les mêmes plats.

## 🔒 Configuration OpenAI

Renseigner la variable d’environnement `OPENAI_API_KEY` avant d’appeler les fonctions utilisant l’API.
