"""
Script ENSEIGNANT — génère le fichier JSON des outputs attendus à partir du notebook de correction.
À exécuter une fois après avoir finalisé et exécuté le notebook de correction.

Usage : python generate_expected.py <tdXX_correction.ipynb> <tdXX_expected.json>
Exemple : python generate_expected.py td03_correction.ipynb td03_expected.json

Le fichier JSON produit est à déposer dans templates/tests/ du dépôt du cours.
"""
import sys
import json
import nbformat

if len(sys.argv) != 3:
    print("Usage : python generate_expected.py <correction.ipynb> <output.json>")
    sys.exit(1)

nb_path, out_path = sys.argv[1], sys.argv[2]

with open(nb_path, encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

expected = {}
skipped = 0

for i, cell in enumerate(nb.cells):
    if cell.cell_type != "code" or not cell.outputs:
        continue
    parts = []
    for out in cell.outputs:
        if out.output_type == "stream":
            parts.append(out.text)
        elif out.output_type in ("execute_result", "display_data"):
            parts.append(out.get("data", {}).get("text/plain", ""))
    text = "".join(parts).strip()
    if text:
        expected[str(i)] = text
    else:
        skipped += 1

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(expected, f, indent=2, ensure_ascii=False)

print(f"✅ {len(expected)} cellules avec output indexées dans {out_path}")
if skipped:
    print(f"   ({skipped} cellules sans output ignorées)")
print()
print("Pensez à relire le JSON et à supprimer les cellules non pertinentes")
print("(affichages HTML, images, cellules de configuration).")
