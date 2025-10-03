const state = {
  etapes: [],
  indexEtape: 0,
};

const selectors = {
  titre: document.getElementById("app-title"),
  description: document.getElementById("recette-description"),
  ingredients: document.getElementById("ingredients-list"),
  recetteComplete: document.getElementById("recette-complete"),
  etapeContenu: document.getElementById("etape-contenu"),
  etapeCompteur: document.getElementById("etape-compteur"),
  precedent: document.getElementById("precedent"),
  suivant: document.getElementById("suivant"),
  panels: Array.from(document.querySelectorAll(".panel")),
  navButtons: Array.from(document.querySelectorAll(".nav-button")),
};

document.addEventListener("DOMContentLoaded", () => {
  chargerRecette();
  initialiserNavigation();
  initialiserControleEtapes();
});

async function chargerRecette() {
  if (window.location.protocol === "file:") {
    afficherErreur(
      "Impossible de charger la recette du jour en ouvrant directement le fichier. Lancez un serveur HTTP local (par exemple : python -m http.server --directory RecettesUtils 8000) puis ouvrez http://localhost:8000/recette.html."
    );
    return;
  }

  try {
    const response = await fetch("recette_du_jour.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Impossible de lire recette_du_jour.json (status ${response.status})`);
    }

    const data = await response.json();
    renseignerInterface(data);
  } catch (error) {
    console.error(error);
    afficherErreur(
      "Impossible de charger la recette du jour. Vérifiez que le fichier recette_du_jour.json est présent dans le même dossier."
    );
  }
}

function renseignerInterface(data) {
  const titre = data.titre || "Recette du jour";
  document.title = titre;
  selectors.titre.textContent = titre;
  selectors.description.textContent = data.description ||
    "Ajoutez une description dans votre fichier recette_du_jour.json pour voir un aperçu ici.";

  mettreAJourIngredients(data.ingredients);
  mettreAJourRecetteComplete(data);
  mettreAJourEtapes(data.etapes);
}

function mettreAJourIngredients(ingredients) {
  selectors.ingredients.innerHTML = "";
  if (!Array.isArray(ingredients) || ingredients.length === 0) {
    const item = document.createElement("li");
    item.textContent = "Aucun ingrédient trouvé. Ajoutez des entrées dans la propriété \"ingredients\".";
    selectors.ingredients.appendChild(item);
    return;
  }

  const fragment = document.createDocumentFragment();
  for (const ingr of ingredients) {
    const item = document.createElement("li");
    item.textContent = ingr;
    fragment.appendChild(item);
  }
  selectors.ingredients.appendChild(fragment);
}

function mettreAJourRecetteComplete(data) {
  let texteComplet =
    data.recette_complete ||
    data.recetteComplete ||
    (Array.isArray(data.etapes)
      ? data.etapes
          .map((etape, index) =>
            `${index + 1}. ${etape.titre ? `${etape.titre} - ` : ""}${etape.instructions || etape}`.trim()
          )
          .join("\n\n")
      : "");

  if (!texteComplet) {
    texteComplet =
      "Ajoutez un champ \"recette_complete\" ou \"recetteComplete\" dans votre JSON, ou une liste d'étapes pour générer le texte complet.";
  }

  selectors.recetteComplete.textContent = texteComplet;
}

function mettreAJourEtapes(etapes) {
  if (!Array.isArray(etapes) || etapes.length === 0) {
    state.etapes = [];
    selectors.etapeContenu.innerHTML =
      "<p>Aucune étape trouvée. Ajoutez un tableau \"etapes\" avec des instructions.</p>";
    selectors.precedent.disabled = true;
    selectors.suivant.disabled = true;
    selectors.etapeCompteur.textContent = "";
    return;
  }

  state.etapes = etapes.map((etape, index) => {
    if (typeof etape === "string") {
      return { titre: `Étape ${index + 1}`, instructions: etape };
    }
    return {
      titre: etape.titre || `Étape ${index + 1}`,
      instructions: etape.instructions || "",
    };
  });

  state.indexEtape = 0;
  mettreAJourVueEtape();
}

function mettreAJourVueEtape() {
  if (state.etapes.length === 0) {
    return;
  }

  const etape = state.etapes[state.indexEtape];
  selectors.etapeContenu.innerHTML = "";

  const titre = document.createElement("h3");
  titre.className = "etape-titre";
  titre.textContent = etape.titre;

  const instructions = document.createElement("p");
  instructions.textContent = etape.instructions;

  selectors.etapeContenu.append(titre, instructions);

  selectors.etapeCompteur.textContent = `${state.indexEtape + 1} / ${state.etapes.length}`;

  selectors.precedent.disabled = state.indexEtape === 0;
  selectors.suivant.textContent =
    state.indexEtape === state.etapes.length - 1 ? "Terminer" : "Suivant";
}

function initialiserNavigation() {
  selectors.navButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetId = button.dataset.target;
      afficherSection(targetId);
    });
  });
}

function afficherSection(id) {
  selectors.panels.forEach((panel) => {
    panel.classList.toggle("active", panel.id === id);
  });

  selectors.navButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.target === id);
  });
}

function initialiserControleEtapes() {
  selectors.precedent.addEventListener("click", () => {
    if (state.indexEtape > 0) {
      state.indexEtape -= 1;
      mettreAJourVueEtape();
    }
  });

  selectors.suivant.addEventListener("click", () => {
    if (state.indexEtape < state.etapes.length - 1) {
      state.indexEtape += 1;
      mettreAJourVueEtape();
    } else {
      state.indexEtape = 0;
      mettreAJourVueEtape();
      afficherSection("intro");
    }
  });
}

function afficherErreur(message) {
  selectors.description.textContent = message;
  selectors.ingredients.innerHTML = "";
  selectors.recetteComplete.textContent = "";
  selectors.etapeContenu.innerHTML = `<p>${message}</p>`;
  selectors.precedent.disabled = true;
  selectors.suivant.disabled = true;
  selectors.etapeCompteur.textContent = "";
}

