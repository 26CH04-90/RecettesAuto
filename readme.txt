🥘 RecettesAuto
📖 Description

RecettesAuto est un projet qui automatise la génération et la gestion des menus hebdomadaires, des stocks alimentaires et de la liste de courses, en combinant l’API ChatGPT, des fichiers JSON et des Raccourcis iOS.

L’objectif est de planifier les repas en fonction des préférences et régimes alimentaires, mettre à jour le stock, générer automatiquement la liste de courses, puis faciliter le remplissage du panier sur Coop.ch.

⚙️ Fonctionnement global

Configuration (config.json)

Nombre de personnes

Régimes alimentaires (sans gluten, végétarien, etc.)

Préférences (plats épicés, en sauce…)

Options (budget, saisonnalité)

Stratégie d’achat (priorité bio, prix moyen, etc.)

Stock (stock.json)

Contient les ingrédients disponibles, organisés par catégories (placard, frigo, fruits, légumes…).

Mis à jour via un Raccourci iPhone (ajout/retrait/fixer quantité).

Menus (menus.json)

Générés automatiquement par l’API ChatGPT en fonction de config.json.

Chaque repas contient : nom, ingrédients, état (proposé, validé, refusé).

Validation/refus des repas via un Raccourci iPhone.

Les repas refusés peuvent être renvoyés à ChatGPT pour proposer des alternatives.

Courses (courses.json)

Générées automatiquement par ChatGPT à partir de :

Menus validés (menus.json)

Stock actuel (stock.json)

Config (bio, budget, stratégie prix…)

Contient uniquement les ingrédients manquants à acheter.

Panier Coop.ch

Étape finale : remplir le panier sur coop.ch.

Pas d’API publique Coop disponible → étape réalisée manuellement ou via un agent GPT/script Playwright qui lit courses.json et ajoute les produits au panier.

📱 Raccourcis iOS

Modifier stock : met à jour stock.json.

Valider menus : parcourt les menus proposés et change leur état (proposé/validé/refusé).

(Futur) Générer courses : appel API GPT → met à jour courses.json.

