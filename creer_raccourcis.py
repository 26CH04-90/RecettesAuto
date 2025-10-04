import json

shortcut = {
  "WFWorkflowActions": [
    # 1. Lire menus.json
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.getfile",
      "WFWorkflowActionParameters": {
        "WFFilePath": "RecettesAuto/menus.json",
        "WFGetFileActionMode": "AskWhereToSave"
      }
    },
    # 2. Obtenir contenu JSON
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.getfilecontents",
      "WFWorkflowActionParameters": {}
    },
    # 3. Choisir un repas
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.choosefromlist",
      "WFWorkflowActionParameters": {
        "WFItems": ["Repas1", "Repas2", "Repas3"]
      }
    },
    # 4. Construire le prompt
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.text",
      "WFWorkflowActionParameters": {
        "WFTextActionText": "Fais-moi la recette complète pour 2 personnes du plat suivant : [[Choix de liste]]"
      }
    },
    # 5. Envoyer à l’API OpenAI
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.getcontentsurl",
      "WFWorkflowActionParameters": {
        "WFHTTPMethod": "POST",
        "WFURL": "https://api.openai.com/v1/chat/completions",
        "WFHTTPHeaders": {
          "Content-Type": "application/json",
          "Authorization": "Bearer VOTRE_CLE_API"
        },
        "WFHTTPBody": json.dumps({
          "model": "gpt-4o-mini",
          "messages": [
            {"role": "system", "content": "Tu es un chef qui écrit des recettes précises."},
            {"role": "user", "content": "Fais-moi la recette complète pour 2 personnes du plat choisi."}
          ]
        })
      }
    },
    # 6. Extraire réponse
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.getdictionaryvalue",
      "WFWorkflowActionParameters": {
        "WFDictionaryKey": "choices.0.message.content"
      }
    },
    # 7. Sauvegarder la recette
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.savefile",
      "WFWorkflowActionParameters": {
        "WFFilePath": "RecettesAuto/recettes.json",
        "WFSaveFileOverwrite": True
      }
    }
  ],
  "WFWorkflowClientRelease": "2.1",
  "WFWorkflowTypes": ["NCWidget"],
  "WFWorkflowIcon": {
    "WFWorkflowIconGlyphNumber": 59511,
    "WFWorkflowIconColor": 0
  },
  "WFWorkflowImportQuestions": []
}

with open("RecetteGPT.shortcut", "w", encoding="utf-8") as f:
    json.dump(shortcut, f, indent=2)

print("✅ Fichier 'RecetteGPT.shortcut' généré.")
