"""Génère les pages légales à partir de legal/*.part.html.

Usage : python legal/_build.py  (depuis la racine du dépôt)
Chaque fichier .part.html commence par une ligne « titre|description »,
suivie du contenu HTML de la page.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} – Case Game</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="https://casegamecm.com/{slug}.html">
  <meta name="theme-color" content="#07080a">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="stylesheet" href="assets/site.css">
</head>
<body>
  <a class="skip" href="#contenu">Aller au contenu</a>

  <svg width="0" height="0" style="position:absolute" aria-hidden="true">
    <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></symbol>
    <symbol id="i-chat" viewBox="0 0 24 24"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22z"/></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></symbol>
  </svg>

  <header class="top">
    <div class="wrap top-inner">
      <a class="brand" href="./" aria-label="Case Game, retour à l'accueil">
        <img src="icon-512.png" alt="" width="44" height="44">
        <span>CASE <b>GAME</b></span>
      </a>
      <button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu">
        <svg class="i"><use href="#i-menu"/></svg>
      </button>
      <nav class="menu" id="menu" aria-label="Navigation principale">
        <a href="./#tarifs">Tarifs</a>
        <a href="./#tournois">Tournois</a>
        <a href="./#association">Association</a>
        <a href="./#infos">Infos pratiques</a>
        <a class="btn solid" href="https://wa.me/237686844407" target="_blank" rel="noopener">
          <svg class="i"><use href="#i-chat"/></svg> Réserver
        </a>
      </nav>
    </div>
  </header>

  <main id="contenu" class="legal-page">
    <div class="wrap">
      <a class="back" href="./"><svg class="i"><use href="#i-arrow"/></svg> Retour à l'accueil</a>
{content}
    </div>
  </main>

  <div class="band" aria-hidden="true"></div>
  <footer>
    <div class="wrap foot">
      <div>
        <a class="brand" href="./"><img src="icon-512.png" alt="" width="44" height="44"><span>CASE <b>GAME</b></span></a>
        <p style="margin-top:14px">Case Game SAS – salle de jeux vidéo, New Bell, Douala. Association Case Game – association à but non lucratif déclarée sous le n° 000879/RDA/J06/SAAJP/BAPP.</p>
      </div>
      <nav aria-label="Informations légales">
        <ul class="legal">
          <li><a href="mentions-legales.html">Mentions légales</a></li>
          <li><a href="confidentialite.html">Confidentialité</a></li>
          <li><a href="cookies.html">Cookies</a></li>
          <li><a href="cgu.html">CGU & règlement des tournois</a></li>
          <li><a href="remboursement.html">Remboursement</a></li>
        </ul>
      </nav>
    </div>
  </footer>

  <script src="assets/site.js" defer></script>
</body>
</html>
"""

for part in sorted((ROOT / "legal").glob("*.part.html")):
    slug = part.name.removesuffix(".part.html")
    first, content = part.read_text(encoding="utf-8").split("\n", 1)
    title, description = first.split("|", 1)
    content = "\n".join("      " + line if line else "" for line in content.rstrip().split("\n"))
    page = TEMPLATE.format(title=title, description=description, slug=slug, content=content)
    (ROOT / f"{slug}.html").write_text(page, encoding="utf-8", newline="\n")
    print("écrit", f"{slug}.html")
