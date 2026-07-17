# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Ce que contient ce dépôt

Dépôt enseignant public du cours **Python & Data Science** (L3 / M1 Économie, UPJV Amiens). Il contient les notebooks de TD, les jeux de données, la documentation et les ressources pédagogiques. Ce n'est pas un projet logiciel : il n'y a pas de commandes de build, de lint ou de tests à exécuter localement. Les tests automatiques sont exécutés dans les dépôts étudiants via GitHub Actions.

La référence complète des décisions pédagogiques et techniques est dans **PLAN.md**.

## Structure

```
assignments/tdXX_nom_du_td/     ← notebooks d'énoncé, organisés par TD
    images/                     ← infographies PNG co-localisées avec le TD
datasets/                       ← jeux de données légers partagés entre TD
docs/                           ← guides techniques (Colab, Git, GitHub, erreurs)
faq/                            ← questions fréquentes étudiants
projects/                       ← consignes mini-projets (MP1, MP2) et projets groupe
resources/                      ← fiches mémo et ressources complémentaires
templates/                      ← modèles de fichiers (solutions.py, tests.yml, etc.)
assets/                         ← visuels du dépôt (banner, images README)
```

Les corrigés ne sont **jamais** dans ce dépôt public. Ils sont conservés dans un dépôt privé séparé ou sur Google Drive, et publiés dans `assignments/tdXX/` après l'échéance.

## Convention de nommage

| Élément | Convention | Exemple |
|---------|-----------|---------|
| Dossier TD | `tdXX_nom_descriptif` | `td01_fondements_de_github` |
| Notebook énoncé | `tdXX_enonce.ipynb` | `td01_enonce.ipynb` |
| Notebook correction | `tdXX_correction.ipynb` | `td01_correction.ipynb` |
| Infographies | `NN_nom_descriptif.png` | `01_gestion_de_versions.png` |
| Données | snake_case, année si pertinent | `salaires_2023.csv` |

## Structure d'un notebook Colab

Chaque notebook commence par :
1. Un badge **Open in Colab** en première cellule
2. Une cellule `# @title ⚙️ Configuration` (cachée) qui définit la fonction helper d'infographie et recrée l'environnement si nécessaire
3. Les sections pédagogiques

Badge Open in Colab :
```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maxencegu/python-datascience/blob/main/assignments/tdXX_nom/tdXX_enonce.ipynb)
```

Fonction helper infographie (à adapter par TD) :
```python
# @title ⚙️ Configuration des ressources (ne pas modifier)
from IPython.display import Image, display

BASE_URL = "https://raw.githubusercontent.com/Maxencegu/python-datascience/main/assignments/tdXX_nom/images/"

def afficher_infographie(nom_fichier, largeur=950):
    display(Image(url=BASE_URL + nom_fichier, width=largeur))
```

## Pattern d'exercice interactif (3 cellules)

Tout exercice suit ce schéma fixe :

**Cellule 1 — Setup** (`# @title ⚙️ Préparation`) : crée l'environnement (dossiers, fichiers, état initial). Cachée, à exécuter en premier.

**Cellule 2 — Exercice** (`# @title 🔧 Exercice — Titre`) : instructions en commentaires, placeholders `___` à remplacer par l'étudiant.

**Cellule 3 — Validation** (`# @title ✅ Vérification`) : vérifie l'état du système et affiche un retour par étape avec ✅ / ❌.

Règles critiques pour les exercices shell :
- `%cd dossier` (pas `!cd`) pour les changements de répertoire persistants
- Commentaires **au-dessus** des commandes magiques `%`, jamais en fin de ligne
- `result = !commande` pour capturer la sortie dans une variable testable
- `!ls -1` plutôt que `!ls` pour un fichier par ligne (validation plus fiable)
- La validation utilise `os.listdir()` et `os.getcwd()` plutôt que de parser la sortie de `ls`

## Règles de contenu (dépôt public)

Ne jamais ajouter dans ce dépôt :
- Liste nominative des étudiants, notes, adresses e-mail, numéros étudiants
- Corrigés avant l'échéance
- Clés API ou tokens
- Données personnelles ou confidentielles

## Programme (année commune L3/M1 2026-2027)

| Séance | Contenu |
|--------|---------|
| TD1 | Git, GitHub et Google Colab |
| TD2 | Les bases de Python et les listes |
| TD3 | Les fonctions, modules et NumPy |
| TD4 | Matplotlib, dictionnaires et Pandas |
| TD5 | Logique, flux de contrôle, filtrage et boucles |
| MP1 | Mini-projet 1 — Analyse exploratoire |
| TD6 | Pandas : agrégation et transformation |
| TD7 | Pandas : filtrage et opérations conditionnelles |
| MP2 | Mini-projet 2 — Nettoyage et transformation |
| TD8 | Pandas : fusion et jointures |
| TD9 | Pandas : fusions avancées et séries temporelles |
