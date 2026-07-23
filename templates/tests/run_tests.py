"""
Runner universel de tests pour les notebooks étudiants.
Téléchargé automatiquement par le workflow GitHub Actions au moment de l'exécution.
Usage : python run_tests.py <tdXX_enonce.ipynb> <tdXX_expected.json>
"""
import sys
import json
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

if len(sys.argv) != 3:
    print("Usage : python run_tests.py <notebook.ipynb> <expected.json>")
    sys.exit(1)

nb_path, expected_path = sys.argv[1], sys.argv[2]

print(f"📓 Exécution de {nb_path}...")

with open(nb_path, encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
try:
    ep.preprocess(nb, {"metadata": {"path": "."}})
except Exception as e:
    print(f"❌ Le notebook a planté pendant l'exécution :\n   {e}")
    sys.exit(1)

print("✅ Notebook exécuté sans erreur\n")
print("🔍 Vérification des résultats...\n")

with open(expected_path, encoding="utf-8") as f:
    expected = json.load(f)

errors = []
for cell_idx, exp in expected.items():
    cell = nb.cells[int(cell_idx)]
    parts = []
    for out in cell.outputs:
        if out.output_type == "stream":
            parts.append(out.get("text", ""))
        elif out.output_type in ("execute_result", "display_data"):
            parts.append(out.get("data", {}).get("text/plain", ""))
    actual = "".join(parts).strip()
    if actual != exp.strip():
        errors.append(
            f"  Cellule {cell_idx}\n"
            f"    attendu  : {exp.strip()!r}\n"
            f"    obtenu   : {actual!r}"
        )

if errors:
    print(f"❌ {len(errors)} test(s) échoué(s) :\n")
    for e in errors:
        print(e)
    sys.exit(1)

print(f"✅ Tous les tests passent ({len(expected)} cellules vérifiées)")
