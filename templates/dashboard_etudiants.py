"""
Tableau de bord — vérification des dépôts étudiants.
Usage : python templates/dashboard_etudiants.py td03

Pour chaque étudiant, vérifie :
  - le notebook tdXX_enonce.ipynb est présent sur main
  - GitHub Actions a tourné sur la branche dev_tdXX
  - le dernier run Actions est passé (success) ou non

Prérequis : gh CLI authentifié (gh auth login)
"""
import subprocess
import json
import sys

# ── Liste des pseudos GitHub étudiants ──────────────────────────
ETUDIANTS = [
    # "pseudo1",
    # "pseudo2",
    # Compléter avec les pseudos réels
]

REPO_NAME = "upjv-python-datascience"

def gh(args, check=False):
    result = subprocess.run(
        ["gh"] + args,
        capture_output=True, text=True
    )
    return result.stdout.strip(), result.returncode

def check_etudiant(username, td):
    """Retourne un dict de statut pour un étudiant et un TD."""
    repo = f"{username}/{REPO_NAME}"
    branch = f"dev_{td}"
    notebook = f"{td}_enonce.ipynb"

    # 1. Notebook présent sur main ?
    out, code = gh(["api", f"repos/{repo}/contents/{notebook}",
                    "--jq", ".name"])
    notebook_ok = code == 0 and notebook in out

    # 2. Actions a tourné sur dev_tdXX ?
    out, code = gh(["run", "list", "--repo", repo, "--branch", branch,
                    "--limit", "1", "--json", "status,conclusion,createdAt",
                    "--jq", ".[0]"])
    if code != 0 or not out or out == "null":
        return {
            "username": username,
            "notebook_main": notebook_ok,
            "actions_run": False,
            "actions_ok": False,
            "created_at": "—",
        }

    run = json.loads(out)
    return {
        "username": username,
        "notebook_main": notebook_ok,
        "actions_run": True,
        "actions_ok": run.get("conclusion") == "success",
        "created_at": run.get("createdAt", "")[:10],
    }

def main():
    if len(sys.argv) < 2:
        print("Usage : python dashboard_etudiants.py td03")
        sys.exit(1)

    td = sys.argv[1]
    print(f"\n{'─'*70}")
    print(f"  Tableau de bord — {td.upper()}")
    print(f"{'─'*70}")
    print(f"  {'Étudiant':<22} {'Notebook/main':<16} {'Actions run':<14} {'Tests OK':<10} {'Date'}")
    print(f"{'─'*70}")

    ok_count = 0
    for username in ETUDIANTS:
        s = check_etudiant(username, td)
        notebook  = "✅" if s["notebook_main"]  else "❌"
        run       = "✅" if s["actions_run"]     else "—"
        tests     = "✅" if s["actions_ok"]      else ("❌" if s["actions_run"] else "—")
        date      = s["created_at"]
        if s["notebook_main"] and s["actions_ok"]:
            ok_count += 1
        print(f"  {username:<22} {notebook:<16} {run:<14} {tests:<10} {date}")

    print(f"{'─'*70}")
    print(f"  {ok_count}/{len(ETUDIANTS)} étudiants validés\n")

if __name__ == "__main__":
    main()
