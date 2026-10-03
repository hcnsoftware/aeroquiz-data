"""Verifie tes questions AVANT de les envoyer sur GitHub.  Usage:  python check.py"""
import json, os, sys
LANGS = ["en", "fr", "ar", "es", "pt"]
root = os.path.dirname(os.path.abspath(__file__))
meta = json.load(open(os.path.join(root, "version.json"), encoding="utf-8"))
errors, total = [], 0
for name in meta["files"]:
    path = os.path.join(root, "questions", name + ".json")
    if not os.path.exists(path):
        errors.append(f"{name}.json introuvable"); continue
    try:
        data = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        errors.append(f"{name}.json: JSON invalide ({e})"); continue
    for i, q in enumerate(data):
        where = f"{name}.json #{i + 1}"
        a = q.get("a")
        if not isinstance(a, int):
            errors.append(f"{where}: 'a' doit etre un entier"); continue
        for l in LANGS:
            t = q.get(l)
            if not isinstance(t, dict) or not isinstance(t.get("q"), str):
                errors.append(f"{where}: langue '{l}' manquante ou sans 'q'"); continue
            c = t.get("c")
            if not isinstance(c, list) or len(c) < 2 or not 0 <= a < len(c):
                errors.append(f"{where}: langue '{l}': 'c' invalide ou 'a' hors limites")
            elif len(c) != len(q["fr"]["c"]):
                errors.append(f"{where}: '{l}' n'a pas le meme nombre de choix que 'fr'")
        img = q.get("image")
        if img and not img.startswith("http") and not os.path.exists(os.path.join(root, "images", img)):
            errors.append(f"{where}: image '{img}' absente du dossier images/")
        total += 1
print(f"version {meta['version']} - {total} questions verifiees")
if errors:
    print("\n".join("ERREUR: " + e for e in errors)); sys.exit(1)
print("Tout est bon, tu peux envoyer sur GitHub.")
