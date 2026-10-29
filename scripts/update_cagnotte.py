"""Met à jour assets/cagnotte.json à partir de la page publique de la cagnotte GoFundMe.

Lancé toutes les 6 heures par .github/workflows/cagnotte.yml.
N'écrit le fichier que si le montant, le nombre de donateurs ou l'objectif change.
"""
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SLUG = "renforcer-la-reussite-scolaire-des-orphelins"
URL = f"https://www.gofundme.com/f/{SLUG}"
OUT = Path(__file__).resolve().parent.parent / "assets" / "cagnotte.json"


def find_fundraiser(node):
    """Cherche l'objet « Fundraiser » de notre cagnotte dans les données de la page."""
    if isinstance(node, dict):
        if node.get("defaultSlug") == SLUG and "currentAmount" in node:
            return node
        children = node.values()
    elif isinstance(node, list):
        children = node
    else:
        return None
    for child in children:
        found = find_fundraiser(child)
        if found:
            return found
    return None


def main():
    request = urllib.request.Request(URL, headers={
        "User-Agent": "Mozilla/5.0 (compatible; CaseGameSite/1.0; +https://casegamecm.com)",
        "Accept-Language": "fr-FR,fr;q=0.9",
    })
    page = urllib.request.urlopen(request, timeout=30).read().decode("utf-8", "replace")

    fundraiser = None
    for script in re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', page, re.S):
        try:
            fundraiser = find_fundraiser(json.loads(script))
        except json.JSONDecodeError:
            continue
        if fundraiser:
            break
    if not fundraiser:
        sys.exit("Cagnotte introuvable dans la page GoFundMe : sa structure a peut-être changé.")

    data = {
        "raised": fundraiser["currentAmount"]["amount"],
        "goal": fundraiser.get("goalAmount", {}).get("amount"),
        "currency": fundraiser["currentAmount"]["currencyCode"],
        "donors": fundraiser.get("donationCount", 0),
    }
    if not data["goal"]:
        sys.exit("Objectif introuvable dans la page GoFundMe.")

    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    if all(old.get(k) == v for k, v in data.items()):
        print("Aucun changement :", data)
        return
    data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Mis à jour :", data)


if __name__ == "__main__":
    main()
