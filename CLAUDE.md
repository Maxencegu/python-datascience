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

def afficher_infographie(nom_fichier, largeur=1300):
    display(Image(url=BASE_URL + nom_fichier, width=largeur))
```

## Création des infographies

Les infographies sont générées via un script Python/Playwright : HTML écrit directement dans le script → `page.set_content()` → screenshot PNG. **Pas de fichier HTML intermédiaire.**

Script type (à adapter) :
```python
from playwright.sync_api import sync_playwright

html_content = """<!DOCTYPE html><html lang="fr"><head>...</head><body>...</body></html>"""

OUTPUT = r"assignments/tdXX_nom/images/NN_nom_pro.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 900}, device_scale_factor=2)
    page.set_content(html_content, wait_until="networkidle")
    page.screenshot(path=OUTPUT, full_page=True)
    browser.close()
```

**Système de design (thème sombre, à reproduire fidèlement) :**
- Fond : `#0d1117` — Cartes : `#161b22` — Bordures : `#21262d`
- Texte principal : `#e6edf3` — Texte secondaire : `#8b949e`
- Breadcrumb (en-tête) : `#58a6ff`, uppercase, letter-spacing 0.15em
- Accentuation des cartes (barre top de 3px) : bleu `#1f6feb`, violet `#8b5cf6`, vert `#3fb950`, orange `#d29922`, rouge `#f85149`
- Code inline : `color: #79c0ff`, `background: #0d1117`, bordure `#30363d`
- Alerte rouge : `background: #200d0d`, bordure `#f85149`
- Viewport 1200×900 + `device_scale_factor=2` → PNG 2400px de large
- Breadcrumb : `TD2 · GITHUB · PYTHON DATA SCIENCE — UPJV AMIENS`

Nommage des fichiers PNG : `NN_nom_descriptif_pro.png` (suffixe `_pro` pour la version finale).

## Pattern d'exercice interactif (3 cellules)

Tout exercice suit ce schéma fixe :

**Cellule 1 — Setup** (`# @title ⚙️ Préparation de l'exercice (exécuter d'abord)`) : crée l'environnement (dossiers, fichiers, état initial Git). Toujours commencer par `os.chdir("/content")`. Supprimer les variables de l'exercice précédent avec `try: del var / except NameError: pass`.

**Cellule 2 — Exercice** (`# @title 🔧 Exercice — Titre`) : instructions en commentaires avec le format ci-dessous, placeholders `___` à remplacer par l'étudiant.

**Cellule 3 — Validation** (`# @title ✅ Vérification`) : vérifie l'état du système et affiche un retour avec ✅ / ❌. Ne jamais afficher `💡 Indice` quand tout est ✅.

Format des commentaires dans la cellule exercice :
```python
# @title 🔧 Exercice — Titre
# ================================================================
#  EXERCICE — Description courte                      [ N étapes ]
# ================================================================
#
# Contexte / rappel de situation
#
# ----------------------------------------------------------------
# Étape 1/N — Consigne
# ----------------------------------------------------------------
variable = ___

# ----------------------------------------------------------------
# Étape 2/N — Consigne
# ----------------------------------------------------------------
___
```

**Règles critiques pour les exercices shell :**
- `%cd dossier` (pas `!cd`) pour les changements de répertoire persistants
- Commentaires **au-dessus** des commandes magiques `%`, jamais en fin de ligne
- `result = !commande` pour capturer la sortie dans une variable testable
- `!ls -1` plutôt que `!ls` pour un fichier par ligne (validation plus fiable)
- La validation utilise `os.listdir()` et `os.getcwd()` plutôt que de parser la sortie de `ls`

**Règles d'isolation entre exercices :**
- Chaque setup commence par `os.chdir("/content")`
- Si l'exercice utilise un dossier Git : `shutil.rmtree(repo)` avant `os.makedirs(repo)`
- Supprimer les variables réutilisées : `try: del journal / except NameError: pass` à la fin du setup
- `git config color.ui false` dans le setup + fonction `strip_ansi()` dans la validation pour éviter les faux négatifs sur les codes ANSI

**Pattern QCM (exercice à choix multiples) :**

Setup minimal :
```python
# @title ⚙️ Préparation de l'exercice (exécuter d'abord)
try:
    del reponse
except NameError:
    pass
print("✅ Environnement prêt")
```

Exercice :
```python
# @title 🔧 Exercice — Titre du QCM
# ================================================================
#  EXERCICE — Titre                                   [ 1 étape ]
# ================================================================
#
# Question posée ?
#
#   1 — Option A
#   2 — Option B
#   3 — Option C  (correcte)
#   4 — Option D
#
# ----------------------------------------------------------------
# Entrez le numéro de la bonne réponse (1, 2, 3 ou 4)
# ----------------------------------------------------------------
reponse = ___
```

Validation :
```python
# @title ✅ Vérification
print("Résultats :\n")

EXPLICATIONS = {
    1: "Explication pourquoi 1 est faux.",
    2: "Explication pourquoi 2 est faux.",
    3: "Correct ! Explication.",
    4: "Explication pourquoi 4 est faux.",
}

try:
    r = int(reponse)
    if r == 3:
        print(f"  ✅ Bonne réponse ({r}) : {EXPLICATIONS[r]}")
    elif r in EXPLICATIONS:
        print(f"  ❌ Réponse {r} incorrecte : {EXPLICATIONS[r]}")
    else:
        print(f"  ❌ Réponse non reconnue : {reponse!r} — attendu un nombre entre 1 et 4")
except NameError:
    print("  ❌ reponse n'est pas défini — attribuez un nombre à la variable reponse")
except (ValueError, TypeError):
    print(f"  ❌ reponse doit être un nombre (1, 2, 3 ou 4) — valeur reçue : {reponse!r}")
```

## Règles de contenu (dépôt public)

Ne jamais ajouter dans ce dépôt :
- Liste nominative des étudiants, notes, adresses e-mail, numéros étudiants
- Corrigés avant l'échéance
- Clés API ou tokens
- Données personnelles ou confidentielles

## Programme (année commune L3/M1 2026-2027)

10 TD + 2 mini-projets. Les noms de dossiers sont à confirmer au fur et à mesure de la création des TDs.

| Séance | Contenu | Dossier |
|--------|---------|---------|
| TD1 | Introduction à Git | `td01_introduction_a_git` |
| TD2 | Introduction à GitHub | `td02_introduction_aux_concepts_de_github` |
| TD3 | Les bases de Python | à créer |
| TD4 | Les fonctions, modules et NumPy | à créer |
| TD5 | Matplotlib, dictionnaires et Pandas | à créer |
| TD6 | Logique, flux de contrôle, filtrage et boucles | à créer |
| MP1 | Mini-projet 1 — Analyse exploratoire | à créer |
| TD7 | Pandas : agrégation et transformation | à créer |
| TD8 | Pandas : filtrage et opérations conditionnelles | à créer |
| MP2 | Mini-projet 2 — Nettoyage et transformation | à créer |
| TD9 | Pandas : fusion de données et jointures | à créer |
| TD10 | Séries temporelles | `td10_series_temporelles` |

**Workflow d'une séance (à ne pas modifier sans accord) :**
GitHub → Correction TD précédent (à partir TD2) → Google Forms présence (10 pts) → Colab → Exercices (20 pts) → Sauvegarde GitHub (à partir TD2) → GitHub Actions (à partir TD3) → Quiz fin de séance (10 pts, à partir TD3)

**Remarques importantes :**
- Les notebooks TD sont modifiés progressivement : ne jamais remplacer un notebook TD existant intégralement sans confirmation explicite
- Le notebook de correction (`tdXX_correction.ipynb`) est dans `.gitignore` — à stocker sur Google Drive jusqu'à la date de publication
