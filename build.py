"""Génère les pages du site à partir des sources dans legal/ et pages/.

Usage : python build.py   (depuis la racine du dépôt)

Chaque source *.part.html commence par un en-tête « clé: valeur », une ligne vide,
puis le contenu HTML de la page :

    path: watersoft-douala/          chemin publié (dossier → index.html, ou fichier .html)
    title: Watersoft à Douala        titre de la page (<title> et fil d'Ariane)
    description: …                   meta description
    crumb: Watersoft                 libellé court dans le fil d'Ariane (facultatif)
    type: page | article | legal     « article » ajoute le schéma Article et la date
    date: 2026-10-30                 date de publication (articles)
    image: video/watersoft-poster.jpg image de partage (facultatif)
    faq: oui                         ajoute le schéma FAQPage à partir des <details class="faq-item">
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://casegamecm.com/"

TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#07080a">
  <link rel="icon" type="image/png" sizes="32x32" href="{root}favicon-32.png">
  <link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Case Game">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary_large_image">
{jsonld}  <link rel="preload" href="{root}fonts/chakra-petch-700.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
  <a class="skip" href="#contenu">Aller au contenu</a>

  <svg width="0" height="0" style="position:absolute" aria-hidden="true">
    <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></symbol>
    <symbol id="i-chat" viewBox="0 0 24 24"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22z"/></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></symbol>
    <symbol id="i-heart" viewBox="0 0 24 24"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></symbol>
  </svg>

  <header class="top">
    <div class="wrap top-inner">
      <a class="brand" href="{root}" aria-label="Case Game, retour à l'accueil">
        <img src="{root}icon-512.png" alt="" width="44" height="44">
        <span>CASE <b>GAME</b></span>
      </a>
      <button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu">
        <svg class="i"><use href="#i-menu"/></svg>
      </button>
      <nav class="menu" id="menu" aria-label="Navigation principale">
        <a href="{root}#tarifs">Tarifs</a>
        <a href="{root}tournois-jeux-video-douala/">Tournois</a>
        <a href="{root}association/">Association</a>
        <a href="{root}blog/">Blog</a>
        <a href="{root}#infos">Infos pratiques</a>
        <a class="btn ghost don" href="{root}association/#campagne"><svg class="i"><use href="#i-heart"/></svg> Faire un don</a>
        <a class="btn solid" href="https://wa.me/237686844407" target="_blank" rel="noopener">
          <svg class="i"><use href="#i-chat"/></svg> Réserver
        </a>
      </nav>
    </div>
  </header>

  <main id="contenu" class="{main_class}">
    <div class="wrap">
      <nav class="crumbs" aria-label="Fil d'Ariane">
{crumbs_html}
      </nav>
{content}
    </div>
  </main>

  <div class="band" aria-hidden="true"></div>
  <footer>
    <div class="wrap foot">
      <div>
        <a class="brand" href="{root}"><img src="{root}icon-512.png" alt="" width="44" height="44"><span>CASE <b>GAME</b></span></a>
        <p style="margin-top:14px">Case Game SAS – salle de jeux vidéo, New Bell, Douala. Association Case Game – association à but non lucratif déclarée sous le n° 000879/RDA/J06/SAAJP/BAPP.</p>
      </div>
      <nav aria-label="Découvrir">
        <ul class="legal">
          <li><a href="{root}tournois-jeux-video-douala/">Tournois</a></li>
          <li><a href="{root}watersoft-douala/">Watersoft</a></li>
          <li><a href="{root}soutien-scolaire-new-bell/">Soutien scolaire</a></li>
          <li><a href="{root}association/">Association</a></li>
          <li><a href="{root}blog/">Blog</a></li>
        </ul>
      </nav>
      <nav aria-label="Informations légales">
        <ul class="legal">
          <li><a href="{root}mentions-legales.html">Mentions légales</a></li>
          <li><a href="{root}confidentialite.html">Confidentialité</a></li>
          <li><a href="{root}cookies.html">Cookies</a></li>
          <li><a href="{root}cgu.html">CGU & règlement des tournois</a></li>
          <li><a href="{root}remboursement.html">Remboursement</a></li>
        </ul>
      </nav>
    </div>
  </footer>

  <a class="wa" href="https://wa.me/237686844407" target="_blank" rel="noopener" aria-label="Écrire à Case Game sur WhatsApp">
    <svg class="i"><use href="#i-chat"/></svg><span>WhatsApp</span>
  </a>

  <script src="{root}assets/site.js" defer></script>
</body>
</html>
"""


def parse(part):
    head, content = part.read_text(encoding="utf-8").split("\n\n", 1)
    meta = dict(line.split(": ", 1) for line in head.strip().split("\n"))
    return meta, content.rstrip()


def all_sources():
    return sorted(list((ROOT / "legal").glob("*.part.html")) + list((ROOT / "pages").rglob("*.part.html")))


def output_path(path):
    return ROOT / (path + "index.html" if path.endswith("/") else path)


def depth(path):
    return path.rstrip("/").count("/") + (1 if path.endswith("/") else 0)


def faq_schema(content, url):
    items = re.findall(r'<details class="faq-item">\s*<summary><h3>(.*?)</h3></summary>\s*<p>(.*?)</p>', content, re.S)
    clean = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    return {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [{"@type": "Question", "name": clean(q),
                        "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in items],
    }


def build():
    sources = [(p, *parse(p)) for p in all_sources()]
    articles = []
    for part, meta, content in sources:
        path = meta["path"]
        root = "../" * depth(path) or "./"
        url = SITE + path
        kind = meta.get("type", "page")
        image = SITE + meta.get("image", "og-image.jpg")

        # Fil d'Ariane : Accueil › (Blog ›) Page
        crumbs = [("Accueil", SITE)]
        if kind == "article":
            crumbs.append(("Blog", SITE + "blog/"))
        crumbs.append((meta.get("crumb", meta["title"]), url))
        crumbs_html = "\n".join(
            f'        <a href="{root}{c_url[len(SITE):]}">{html.escape(name)}</a>' if i < len(crumbs) - 1
            else f'        <span aria-current="page">{html.escape(name)}</span>'
            for i, (name, c_url) in enumerate(crumbs))

        graph = [{
            "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                                for i, (n, u) in enumerate(crumbs)],
        }]
        if kind == "article":
            graph.append({
                "@type": "BlogPosting",
                "@id": url + "#article",
                "headline": meta["title"],
                "description": meta["description"],
                "datePublished": meta["date"],
                "dateModified": meta.get("updated", meta["date"]),
                "inLanguage": "fr",
                "image": image,
                "mainEntityOfPage": url,
                "author": {"@type": "Organization", "name": "Case Game", "url": SITE},
                "publisher": {"@id": SITE + "#salle"},
            })
            articles.append((meta, content))
        elif kind != "legal":
            graph.append({"@type": "WebPage", "@id": url, "url": url, "name": meta["title"],
                          "description": meta["description"], "inLanguage": "fr",
                          "about": {"@id": SITE + "#salle"}, "isPartOf": {"@id": SITE + "#site"}})
        if meta.get("faq") == "oui":
            graph.append(faq_schema(content, url))

        ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
        jsonld = '  <script type="application/ld+json">\n' + "\n".join("  " + l for l in ld.split("\n")) + "\n  </script>\n"

        body = content.replace("{root}", root)
        body = "\n".join("      " + line if line else "" for line in body.split("\n"))
        page = TEMPLATE.format(
            title=html.escape(meta["title"]),
            full_title=html.escape(meta["title"] if "Case Game" in meta["title"] else meta["title"] + " – Case Game"),
            description=html.escape(meta["description"]),
            url=url, root=root, image=image, jsonld=jsonld, crumbs_html=crumbs_html, content=body,
            og_type="article" if kind == "article" else "website",
            main_class="legal-page" if kind == "legal" else "content-page",
        )
        out = output_path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8", newline="\n")
        print("écrit", out.relative_to(ROOT))
    return sources


if __name__ == "__main__":
    build()
