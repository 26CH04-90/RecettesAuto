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
├── RecettesUtils/
│   ├── recette.html
│   ├── recette_du_jour.json
│   ├── script.js
│   └── style.css
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
- **`RecettesUtils/`** : utilitaire HTML/CSS/JS autonome pour consulter la recette finale du jour depuis iCloud.
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

## 📖 Utilitaire HTML « Recette du jour »

Le dossier `RecettesUtils/` peut être copié tel quel dans `iCloud Drive/Raccourcis/RecettesUtils/`.
Il contient une page statique qui lit le fichier `recette_du_jour.json` enregistré par un raccourci iOS :

1. Le raccourci interroge l’API ChatGPT et génère un JSON structuré (titre, description, ingrédients, étapes).
2. Le JSON est sauvegardé sous `recette_du_jour.json` dans le même dossier iCloud.
3. En ouvrant `recette.html`, le script charge ce fichier et affiche automatiquement :
   - une introduction (titre + description),
   - la liste des ingrédients,
   - la recette complète d’un seul bloc,
   - un mode pas-à-pas en plein écran avec boutons « Précédent/Suivant ».

> 💡 **Astuce** : les navigateurs modernes bloquent les requêtes `fetch` depuis un fichier ouvert directement (`file://`).
> Pour prévisualiser la page en local, lance un petit serveur HTTP depuis la racine du dossier :

```bash
python -m http.server --directory RecettesUtils 8000
```

Ensuite, ouvre [http://localhost:8000/recette.html](http://localhost:8000/recette.html) dans ton navigateur pour charger correctement la recette du jour.

Le fichier `recette_du_jour.json` fourni est un exemple : il peut être remplacé librement par le raccourci.

## 🗂️ Historique des menus

- Le fichier `data/menus.json` est désormais organisé par semaine (format `YYYY-Www`).
- Chaque génération crée une nouvelle entrée sans écraser les précédentes, ce qui permet
  de conserver un historique complet.
- Lors de la génération, RecettesAuto consulte automatiquement les `semaines_historique`
  dernières semaines définies dans la configuration pour éviter de reproposer les mêmes plats.

## 🔒 Configuration OpenAI

Renseigner la variable d’environnement `OPENAI_API_KEY` avant d’appeler les fonctions utilisant l’API.

Vous pouvez la définir directement dans votre shell (`export OPENAI_API_KEY=...`) **ou** créer un fichier `.env`
à la racine du projet contenant une ligne `OPENAI_API_KEY=...`. Le chargeur intégré lit automatiquement ce
fichier et n’écrase jamais une variable déjà présente dans l’environnement.
