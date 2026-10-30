"""Génère les pages du site à partir des sources dans legal/ et pages/.

Usage : python build.py   (depuis la racine du dépôt)

Chaque source *.part.html commence par un en-tête « clé: valeur », une ligne vide,
puis le contenu HTML de la page :

    path: watersoft-douala/          chemin publié (dossier → index.html, ou fichier .html)
    title: Watersoft à Douala        titre de la page (<title> et fil d'Ariane)
    description: …                   meta description
    crumb: Watersoft                 libellé court dans le fil d'Ariane (facultatif)
    type: page | article | legal     « article » ajoute le schéma Article et la date
    category: resultats              rubrique d'un article : resultats, reussites, bilans, dons, guides
    date: 2026-10-30                 date de publication (articles)
    image: video/watersoft-poster.jpg image de partage (facultatif)
    faq: oui                         ajoute le schéma FAQPage à partir des <details class="faq-item">
"""
import html
import json
import re
from datetime import date, datetime
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
  <link rel="alternate" type="application/rss+xml" title="Blog Case Game" href="{root}blog/feed.xml">
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


CATEGORIES = {
    # clé : (nom, chemin de la page de rubrique, description)
    "resultats": ("Résultats des tournois", "blog/resultats-tournois/",
                  "Résultats des tournois de jeux vidéo Case Game à Douala : vainqueurs, scores, classements et photos de chaque tournoi."),
    "reussites": ("Réussites de la semaine", "blog/reussites/",
                  "Les réussites de la semaine chez Case Game : progrès des élèves, missions solidaires, joueurs à l'honneur et bonnes nouvelles."),
    "bilans": ("Bilans et objectifs du mois", "blog/bilans/",
               "Chaque mois, les grandes actions de Case Game et de l'Association Case Game, et nos objectifs pour le mois suivant."),
    "dons": ("Dons et cadeaux", "blog/dons-et-cadeaux/",
             "Transparence sur les dons reçus par l'Association Case Game et les cadeaux remis aux enfants et aux joueurs."),
    "guides": ("Guides", "blog/guides/",
               "Nos guides pour jouer, sortir et progresser à Douala : prix, bons plans, esport au Cameroun et idées de sorties."),
}
MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
          "septembre", "octobre", "novembre", "décembre"]
HOME_START, HOME_END = "<!-- ACTUS:DEBUT -->", "<!-- ACTUS:FIN -->"


def date_fr(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {MONTHS[m - 1]} {y}"


def post_card(meta, root, heading="h2"):
    name = CATEGORIES[meta["category"]][0]
    img = meta.get("image")
    thumb = f'<img src="{root}{img}" alt="" loading="lazy" width="320" height="240">' if img else ""
    return (f'<li>\n  <a class="post-card{" has-thumb" if img else ""}" href="{root}{meta["path"]}">\n'
            f'    {thumb}\n    <div>\n'
            f'      <span class="post-meta"><span class="post-cat">{html.escape(name)}</span> · '
            f'<time datetime="{meta["date"]}">{date_fr(meta["date"])}</time></span>\n'
            f'      <{heading}>{html.escape(meta["title"])}</{heading}>\n'
            f'      <p>{html.escape(meta["description"])}</p>\n'
            f'    </div>\n  </a>\n</li>')


def category_chips(articles, root, current=None):
    counts = {k: sum(1 for m, _ in articles if m["category"] == k) for k in CATEGORIES}
    chips = [f'<a class="chip{" active" if current is None else ""}" href="{root}blog/">Tout ({len(articles)})</a>']
    for key, (name, path, _) in CATEGORIES.items():
        label = f"{html.escape(name)} ({counts[key]})"
        if counts[key]:
            chips.append(f'<a class="chip{" active" if key == current else ""}" href="{root}{path}">{label}</a>')
        else:
            chips.append(f'<span class="chip empty" title="Bientôt">{label}</span>')
    return '<nav class="chips" aria-label="Rubriques du blog">\n    ' + "\n    ".join(chips) + "\n  </nav>"


def listing_page(articles, path, title, description, crumb, intro, current=None):
    posts = [m for m, _ in articles if current is None or m["category"] == current]
    cards = "\n".join(post_card(m, "{root}") for m in posts)
    content = f"""<div class="prose" style="max-width:900px">
  <p class="label">Blog</p>
  <h1 style="font-size:clamp(38px,5.6vw,72px);text-transform:uppercase">{html.escape(title)}</h1>
  <p class="byline" style="font-size:18px">{html.escape(intro)}</p>
  {category_chips(articles, "{root}", current)}
  <ul class="post-list">
{cards}
  </ul>
  <p class="feed-link"><a href="{{root}}blog/feed.xml">S'abonner au flux RSS du blog</a></p>
</div>"""
    meta = {"path": path, "title": title, "description": description, "crumb": crumb, "type": "listing"}
    return meta, content


def related_block(meta, articles):
    same = [m for m, _ in articles if m["category"] == meta["category"] and m["path"] != meta["path"]][:3]
    name, cat_path, _ = CATEGORIES[meta["category"]]
    items = "\n".join(f'    <li><a href="{{root}}{m["path"]}">{html.escape(m["title"])}</a> · {date_fr(m["date"])}</li>' for m in same)
    listing = f"\n  <ul>\n{items}\n  </ul>" if same else ""
    return f"""

<aside class="related prose">
  <h2>{"Dans la même rubrique" if same else "Continuer la lecture"}</h2>{listing}
  <p><a href="{{root}}{cat_path}">Rubrique « {html.escape(name)} »</a> · <a href="{{root}}blog/">Tout le blog</a></p>
</aside>"""


def render(meta, content):
    path = meta["path"]
    root = "../" * depth(path) or "./"
    url = SITE + path
    kind = meta.get("type", "page")
    image = SITE + meta.get("image", "og-image.jpg")

    # Fil d'Ariane : Accueil › (Blog › Rubrique ›) Page
    crumbs = [("Accueil", SITE)]
    if kind == "article":
        name, cat_path, _ = CATEGORIES[meta["category"]]
        crumbs += [("Blog", SITE + "blog/"), (name, SITE + cat_path)]
    elif kind == "listing" and path != "blog/":
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
            "articleSection": CATEGORIES[meta["category"]][0],
            "inLanguage": "fr",
            "image": image,
            "mainEntityOfPage": url,
            "author": {"@type": "Organization", "name": "Case Game", "url": SITE},
            "publisher": {"@id": SITE + "#salle"},
        })
    elif kind == "listing":
        graph.append({"@type": "CollectionPage", "@id": url, "url": url, "name": meta["title"],
                      "description": meta["description"], "inLanguage": "fr", "isPartOf": {"@id": SITE + "#site"}})
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
        full_title=html.escape(meta["title"] if "Case Game" in meta["title"] or len(meta["title"]) > 50 else meta["title"] + " – Case Game"),
        description=html.escape(meta["description"]),
        url=url, root=root, image=image, jsonld=jsonld, crumbs_html=crumbs_html, content=body,
        og_type="article" if kind == "article" else "website",
        main_class="legal-page" if kind == "legal" else "content-page",
    )
    out = output_path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8", newline="\n")
    print("écrit", out.relative_to(ROOT))


def write_feed(articles):
    items = "".join(f"""
    <item>
      <title>{html.escape(m["title"])}</title>
      <link>{SITE}{m["path"]}</link>
      <guid>{SITE}{m["path"]}</guid>
      <category>{html.escape(CATEGORIES[m["category"]][0])}</category>
      <pubDate>{datetime.strptime(m["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 08:00:00 +0100")}</pubDate>
      <description>{html.escape(m["description"])}</description>
    </item>""" for m, _ in articles[:30])
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Blog Case Game – gaming, esport et actualités à Douala</title>
    <link>{SITE}blog/</link>
    <atom:link href="{SITE}blog/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Résultats des tournois, réussites de la semaine, bilans du mois, dons et cadeaux, guides : l'actualité de Case Game à New Bell, Douala.</description>
    <language>fr</language>{items}
  </channel>
</rss>
"""
    (ROOT / "blog" / "feed.xml").write_text(feed, encoding="utf-8", newline="\n")
    print("écrit blog/feed.xml")


def update_home(articles):
    """Insère les 3 derniers articles dans la section « Actualités » de l'accueil."""
    home = ROOT / "index.html"
    s = home.read_text(encoding="utf-8")
    if HOME_START not in s:
        return
    cards = "\n".join(post_card(m, "", heading="h3") for m, _ in articles[:3])
    cards = "\n".join("          " + l for l in cards.split("\n"))
    a, b = s.index(HOME_START) + len(HOME_START), s.index(HOME_END)
    home.write_text(s[:a] + "\n" + cards + "\n          " + s[b:], encoding="utf-8", newline="\n")
    print("mis à jour index.html (actualités)")


def write_sitemap(entries):
    rows = "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{d}</lastmod></url>\n" for p, d in entries)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + rows + "</urlset>\n", encoding="utf-8", newline="\n")
    print("écrit sitemap.xml")


def build():
    today = date.today().isoformat()
    sources = [parse(p) for p in all_sources()]
    articles = sorted([(m, c) for m, c in sources if m.get("type") == "article"],
                      key=lambda mc: mc[0]["date"], reverse=True)
    for m, _ in articles:
        assert m.get("category") in CATEGORIES, f"Rubrique inconnue pour {m['path']} : {m.get('category')}"

    pages = []
    for meta, content in sources:
        if meta.get("type") == "article":
            content = content + related_block(meta, articles)
        pages.append((meta, content))

    pages.append(listing_page(
        articles, "blog/", "Le blog Case Game",
        "Blog Case Game : résultats des tournois, réussites de la semaine, bilans du mois, dons et cadeaux, et guides gaming à Douala.",
        "Blog",
        "Résultats des tournois, réussites de la semaine, bilans du mois, dons et cadeaux, et nos guides : toute l'actualité de Case Game à New Bell, Douala."))
    for key, (name, path, desc) in CATEGORIES.items():
        if any(m["category"] == key for m, _ in articles):
            pages.append(listing_page(articles, path, name, desc, name, desc, current=key))

    for meta, content in pages:
        render(meta, content)
    write_feed(articles)
    update_home(articles)
    write_sitemap([("", today), ("en/", today)]
                  + [(m["path"], m.get("updated", m.get("date", today))) for m, _ in pages])


if __name__ == "__main__":
    build()
