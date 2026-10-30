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
    fr: watersoft-douala/            (pages anglaises) chemin de la page française jumelle

Version anglaise : chaque page ou article français a sa traduction dans pages/en/,
avec un chemin qui commence par « en/ » et la clé « fr: ». Le script relie les deux
(liens hreflang et bouton FR/EN) et signale toute page française sans traduction.
"""
import html
import json
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://casegamecm.com/"

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">
{hreflang}  <meta name="theme-color" content="#07080a">
  <link rel="icon" type="image/png" sizes="32x32" href="{root}favicon-32.png">
  <link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Case Game">
  <meta property="og:locale" content="{og_locale}">
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
  <a class="skip" href="#contenu">{skip}</a>

  <svg width="0" height="0" style="position:absolute" aria-hidden="true">
    <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></symbol>
    <symbol id="i-chat" viewBox="0 0 24 24"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22z"/></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></symbol>
    <symbol id="i-heart" viewBox="0 0 24 24"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></symbol>
  </svg>

  <header class="top">
    <div class="wrap top-inner">
      <a class="brand" href="{home}" aria-label="{t[brand]}">
        <img src="{root}icon-512.png" alt="" width="44" height="44">
        <span>CASE <b>GAME</b></span>
      </a>
      <button class="burger" aria-expanded="false" aria-controls="menu" aria-label="{t[menu]}">
        <svg class="i"><use href="#i-menu"/></svg>
      </button>
      <nav class="menu" id="menu" aria-label="{t[nav]}">
        {mega}
{nav_links}
        {switch}
        <a class="btn ghost don" href="{home}{t[donate_href]}"><svg class="i"><use href="#i-heart"/></svg> {t[donate]}</a>
        <a class="btn solid" href="https://wa.me/237686844407" target="_blank" rel="noopener">
          <svg class="i"><use href="#i-chat"/></svg> {t[book]}
        </a>
      </nav>
    </div>
  </header>

  <main id="contenu" class="{main_class}">
    <div class="wrap">
      <nav class="crumbs" aria-label="{t[crumbs]}">
{crumbs_html}
      </nav>
{content}
    </div>
  </main>

  <div class="band" aria-hidden="true"></div>
  <footer>
    <div class="wrap foot">
      <div>
        <a class="brand" href="{home}"><img src="{root}icon-512.png" alt="" width="44" height="44"><span>CASE <b>GAME</b></span></a>
        <p style="margin-top:14px">{t[footer]}</p>
      </div>
      <nav aria-label="{t[discover]}">
        <ul class="legal">
{discover_links}
        </ul>
      </nav>
      <nav aria-label="{t[legal]}">
        <ul class="legal">
{legal_links}
        </ul>
      </nav>
    </div>
  </footer>

  <a class="wa" href="https://wa.me/237686844407" target="_blank" rel="noopener" aria-label="{t[wa]}">
    <svg class="i"><use href="#i-chat"/></svg><span>WhatsApp</span>
  </a>

  <script src="{root}assets/site.js" defer></script>
</body>
</html>
"""


# Textes de la mise en page, par langue. Les liens sont relatifs à la racine du site.
L10N = {
    "fr": {
        "home": "", "og_locale": "fr_FR", "skip": "Aller au contenu",
        "brand": "Case Game, retour à l'accueil", "menu": "Ouvrir le menu", "nav": "Navigation principale",
        "nav_links": [("#tarifs", "Tarifs"), ("association/", "Association"), ("blog/", "Blog"), ("#infos", "Infos pratiques")],
        "donate_href": "association/#campagne", "donate": "Faire un don", "book": "Réserver",
        "crumbs": "Fil d'Ariane", "crumb_home": "Accueil",
        "footer": "Case Game SAS – salle de jeux vidéo, New Bell, Douala. Association Case Game – association à but non lucratif déclarée sous le n° 000879/RDA/J06/SAAJP/BAPP.",
        "discover": "Découvrir",
        "discover_links": [("activites/", "Activités"), ("tournois-jeux-video-douala/", "Tournois"), ("watersoft-douala/", "Watersoft"),
                           ("jeux-de-societe-douala/", "Jeux de société"), ("soutien-scolaire-new-bell/", "Soutien scolaire"),
                           ("association/", "Association"), ("blog/", "Blog")],
        "legal": "Informations légales",
        "legal_links": [("mentions-legales.html", "Mentions légales"), ("confidentialite.html", "Confidentialité"), ("cookies.html", "Cookies"),
                        ("cgu.html", "CGU & règlement des tournois"), ("remboursement.html", "Remboursement")],
        "wa": "Écrire à Case Game sur WhatsApp",
        "switch": ("EN", "en", "English version"),
        "activities": "Activités", "activities_path": "activites/", "all_activities": "Voir toutes les activités →",
        "groups": {"jouer": "Jouer et se challenger", "grandir": "Apprendre et agir"},
    },
    "en": {
        "home": "en/", "og_locale": "en_GB", "skip": "Skip to content",
        "brand": "Case Game, back to home", "menu": "Open menu", "nav": "Main navigation",
        "nav_links": [("en/#tarifs", "Prices"), ("en/association/", "Association"), ("en/blog/", "Blog"), ("en/#infos", "Visit us")],
        "donate_href": "association/#campagne", "donate": "Donate", "book": "Book",
        "crumbs": "Breadcrumb", "crumb_home": "Home",
        "footer": "Case Game SAS – video game venue, New Bell, Douala. Association Case Game – non-profit association registered under no. 000879/RDA/J06/SAAJP/BAPP.",
        "discover": "Explore",
        "discover_links": [("en/activities/", "Activities"), ("en/video-game-tournaments-douala/", "Tournaments"), ("en/watersoft-douala/", "Watersoft"),
                           ("en/board-games-douala/", "Board games"), ("en/tutoring-new-bell/", "Tutoring"),
                           ("en/association/", "Association"), ("en/blog/", "Blog")],
        "legal": "Legal information",
        "legal_links": [("mentions-legales.html", "Legal notice (FR)"), ("confidentialite.html", "Privacy (FR)"), ("cookies.html", "Cookies (FR)"),
                        ("cgu.html", "Terms & tournament rules (FR)"), ("remboursement.html", "Refunds (FR)")],
        "wa": "Message Case Game on WhatsApp",
        "switch": ("FR", "fr", "Version française"),
        "activities": "Activities", "activities_path": "en/activities/", "all_activities": "See all activities →",
        "groups": {"jouer": "Play and compete", "grandir": "Learn and take action"},
    },
}


def lang_of(path):
    return "en" if path.startswith("en/") else "fr"


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
               "Les guides Case Game pour jouer, sortir et progresser à Douala : prix des consoles, bons plans, esport au Cameroun et idées de sorties pour les jeunes."),
}
CATEGORIES_EN = {
    "resultats": ("Tournament results", "en/blog/tournament-results/",
                  "Results of Case Game's video game tournaments in Douala: winners, scores, rankings and photos from every tournament."),
    "reussites": ("Wins of the week", "en/blog/wins-of-the-week/",
                  "This week's wins at Case Game: students' progress, community missions, players in the spotlight and good news."),
    "bilans": ("Monthly reviews and goals", "en/blog/monthly-reviews/",
               "Every month, the main actions of Case Game and the Association Case Game, and our goals for the month ahead."),
    "dons": ("Donations and gifts", "en/blog/donations-and-gifts/",
             "Full transparency on the donations received by the Association Case Game and the gifts given to children and players."),
    "guides": ("Guides", "en/blog/guides/",
               "Case Game guides to playing, going out and improving in Douala: console prices, tips, esports in Cameroon and ideas for young people."),
}
CATS = {"fr": CATEGORIES, "en": CATEGORIES_EN}
MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
          "septembre", "octobre", "novembre", "décembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August",
             "September", "October", "November", "December"]
HOME_START, HOME_END = "<!-- ACTUS:DEBUT -->", "<!-- ACTUS:FIN -->"


def date_fr(iso, lang="fr"):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {(MONTHS_EN if lang == 'en' else MONTHS)[m - 1]} {y}"


def post_card(meta, root, heading="h2"):
    lang = lang_of(meta["path"])
    name = CATS[lang][meta["category"]][0]
    img = meta.get("image")
    if img and (ROOT / img).with_suffix(".webp").exists():
        img = str(Path(img).with_suffix(".webp")).replace("\\", "/")
    thumb = f'<img src="{root}{img}" alt="" loading="lazy" width="320" height="240">' if img else ""
    return (f'<li>\n  <a class="post-card{" has-thumb" if img else ""}" href="{root}{meta["path"]}">\n'
            f'    {thumb}\n    <div>\n'
            f'      <span class="post-meta"><span class="post-cat">{html.escape(name)}</span> · '
            f'<time datetime="{meta["date"]}">{date_fr(meta["date"], lang)}</time></span>\n'
            f'      <{heading}>{html.escape(meta["title"])}</{heading}>\n'
            f'      <p>{html.escape(meta["description"])}</p>\n'
            f'    </div>\n  </a>\n</li>')


def category_chips(articles, root, current=None, lang="fr"):
    en = lang == "en"
    counts = {k: sum(1 for m, _ in articles if m["category"] == k) for k in CATEGORIES}
    blog = "en/blog/" if en else "blog/"
    chips = [f'<a class="chip{" active" if current is None else ""}" href="{root}{blog}">{"All" if en else "Tout"} ({len(articles)})</a>']
    for key, (name, path, _) in CATS[lang].items():
        label = f"{html.escape(name)} ({counts[key]})"
        if counts[key]:
            chips.append(f'<a class="chip{" active" if key == current else ""}" href="{root}{path}">{label}</a>')
        else:
            chips.append(f'<span class="chip empty" title="{"Coming soon" if en else "Bientôt"}">{label}</span>')
    aria = "Blog sections" if en else "Rubriques du blog"
    return f'<nav class="chips" aria-label="{aria}">\n    ' + "\n    ".join(chips) + "\n  </nav>"


def listing_page(articles, path, title, description, crumb, intro, current=None):
    lang = lang_of(path)
    posts = [m for m, _ in articles if current is None or m["category"] == current]
    cards = "\n".join(post_card(m, "{root}") for m in posts)
    feed = "" if lang == "en" else '\n  <p class="feed-link"><a href="{root}blog/feed.xml">S\'abonner au flux RSS du blog</a></p>'
    content = f"""<div class="prose" style="max-width:900px">
  <p class="label">Blog</p>
  <h1 style="font-size:clamp(38px,5.6vw,72px);text-transform:uppercase">{html.escape(title)}</h1>
  <p class="byline" style="font-size:18px">{html.escape(intro)}</p>
  {category_chips(articles, "{root}", current, lang)}
  <ul class="post-list">
{cards}
  </ul>{feed}
</div>"""
    if lang == "en":
        seo_title = ("Case Game blog: tournaments, news and guides in Douala" if current is None
                     else f"{title} – Case Game blog, Douala")
    else:
        seo_title = ("Blog Case Game : tournois, actualités et guides à Douala" if current is None
                     else f"{title} – Blog Case Game Douala")
    meta = {"path": path, "title": title, "description": description, "crumb": crumb, "type": "listing", "seo_title": seo_title}
    return meta, content


def related_block(meta, articles):
    lang = lang_of(meta["path"])
    en = lang == "en"
    same = [m for m, _ in articles if m["category"] == meta["category"] and m["path"] != meta["path"]][:3]
    name, cat_path, _ = CATS[lang][meta["category"]]
    items = "\n".join(f'    <li><a href="{{root}}{m["path"]}">{html.escape(m["title"])}</a> · {date_fr(m["date"], lang)}</li>' for m in same)
    listing = f"\n  <ul>\n{items}\n  </ul>" if same else ""
    if en:
        heading = "More in this section" if same else "Keep reading"
        links = f'<a href="{{root}}{cat_path}">“{html.escape(name)}” section</a> · <a href="{{root}}en/blog/">The whole blog</a>'
    else:
        heading = "Dans la même rubrique" if same else "Continuer la lecture"
        links = f'<a href="{{root}}{cat_path}">Rubrique « {html.escape(name)} »</a> · <a href="{{root}}blog/">Tout le blog</a>'
    return f"""

<aside class="related prose">
  <h2>{heading}</h2>{listing}
  <p>{links}</p>
</aside>"""


def render(meta, content, twins):
    path = meta["path"]
    lang = lang_of(path)
    t = L10N[lang]
    root = "../" * depth(path) or "./"
    home = root + t["home"]
    blog = t["home"] + "blog/"
    url = SITE + path
    kind = meta.get("type", "page")
    image = SITE + meta.get("image", "og-image.jpg")

    # Version dans l'autre langue (hreflang et bouton FR/EN)
    twin = twins.get(path)
    if twin:
        fr_path, en_path = (path, twin) if lang == "fr" else (twin, path)
        hreflang = (f'  <link rel="alternate" hreflang="fr" href="{SITE}{fr_path}">\n'
                    f'  <link rel="alternate" hreflang="en" href="{SITE}{en_path}">\n'
                    f'  <link rel="alternate" hreflang="x-default" href="{SITE}{fr_path}">\n')
    else:
        hreflang = ""
    label, other, aria = t["switch"]
    switch_href = root + (twin if twin else L10N[other]["home"])
    switch = f'<a class="lang" href="{switch_href}" hreflang="{other}" lang="{other}" aria-label="{aria}">{label}</a>'

    # Fil d'Ariane : Accueil › (Blog › Rubrique ›) Page
    crumbs = [(t["crumb_home"], SITE + t["home"])]
    if kind == "article":
        name, cat_path, _ = CATS[lang][meta["category"]]
        crumbs += [("Blog", SITE + blog), (name, SITE + cat_path)]
    elif kind == "listing" and path != blog:
        crumbs.append(("Blog", SITE + blog))
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
            "articleSection": CATS[lang][meta["category"]][0],
            "inLanguage": lang,
            "image": image,
            "mainEntityOfPage": url,
            "author": {"@type": "Organization", "name": "Case Game", "url": SITE},
            "publisher": {"@id": SITE + "#salle"},
        })
    elif kind == "listing":
        graph.append({"@type": "CollectionPage", "@id": url, "url": url, "name": meta["title"],
                      "description": meta["description"], "inLanguage": lang, "isPartOf": {"@id": SITE + "#site"}})
    elif kind != "legal":
        graph.append({"@type": "WebPage", "@id": url, "url": url, "name": meta["title"],
                      "description": meta["description"], "inLanguage": lang,
                      "about": {"@id": SITE + "#salle"}, "isPartOf": {"@id": SITE + "#site"}})
    if meta.get("faq") == "oui":
        graph.append(faq_schema(content, url))

    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    jsonld = '  <script type="application/ld+json">\n' + "\n".join("  " + l for l in ld.split("\n")) + "\n  </script>\n"

    legal_attr = ' hreflang="fr"' if lang == "en" else ""
    body = content.replace("{root}", root)
    body = "\n".join("      " + line if line else "" for line in body.split("\n"))
    page = TEMPLATE.format(
        title=html.escape(meta["title"]),
        full_title=html.escape(meta.get("seo_title") or (meta["title"] if "Case Game" in meta["title"] or len(meta["title"]) > 50 else meta["title"] + " – Case Game")),
        description=html.escape(meta["description"]),
        url=url, root=root, image=image, jsonld=jsonld, crumbs_html=crumbs_html, content=body,
        mega=mega_menu(root, lang),
        og_type="article" if kind == "article" else "website",
        main_class="legal-page" if kind == "legal" else "content-page",
        lang=lang, og_locale=t["og_locale"], skip=t["skip"], t=t, home=home, hreflang=hreflang, switch=switch,
        nav_links="\n".join(f'        <a href="{root}{h}">{n}</a>' for h, n in t["nav_links"]),
        discover_links="\n".join(f'          <li><a href="{root}{h}">{n}</a></li>' for h, n in t["discover_links"]),
        legal_links="\n".join(f'          <li><a href="{root}{h}"{legal_attr}>{n}</a></li>' for h, n in t["legal_links"]),
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


ICONS = {
    "dice": '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="1.2"/><circle cx="16" cy="16" r="1.2"/><circle cx="12" cy="12" r="1.2"/><circle cx="16" cy="8" r="1.2"/><circle cx="8" cy="16" r="1.2"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    "coin": '<circle cx="12" cy="12" r="9"/><path d="M14.5 9.5a2.5 2.5 0 1 0 0 5H12v-2.5"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>',
    "cup": '<path d="M17 8h1a4 4 0 1 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"/><path d="M6 2v2M10 2v2M14 2v2"/>',
}

# Activités : une seule liste pour le menu « Activités » et la page /activites/
ACTIVITIES = [
    {"id": "salle", "group": "jouer", "title": "Salle de jeux vidéo", "short": "PS4, Xbox, Wii · dès 350 FCFA",
     "text": "Plus de 10 consoles PlayStation, Xbox et Nintendo, de 30 minutes à 3 heures, seul ou entre amis. Paiement en FCFA ou en Games Points.",
     "href": "#tarifs", "img": "Carroussel_7.webp", "alt": "Des jeunes jouent sur les consoles de la salle Case Game",
     "en": {"title": "Video game room", "short": "PS4, Xbox, Wii · from 350 FCFA", "text": "Over 10 PlayStation, Xbox and Nintendo consoles, from 30 minutes to 3 hours, alone or with friends. Pay in FCFA or in Games Points.", "href": "en/#tarifs", "alt": "Young people playing on the consoles at Case Game"}},
    {"id": "tournois", "group": "jouer", "title": "Tournois", "short": "Chaque semaine · dès 200 FCFA",
     "text": "Un tournoi chaque semaine, une Ligue Wii gratuite et un tournoi mensuel 18+ avec 30 000 FCFA à gagner. Classement 100 % sportif.",
     "href": "tournois-jeux-video-douala/", "img": "events_img.webp", "alt": "Des élèves consultent le tableau d'un tournoi",
     "en": {"title": "Tournaments", "short": "Every week · from 200 FCFA", "text": "A tournament every week, a free Wii League and a monthly 18+ tournament with 30,000 FCFA to win. Rankings based on results only.", "href": "en/video-game-tournaments-douala/", "alt": "Students look at a tournament board"}},
    {"id": "watersoft", "group": "jouer", "title": "Watersoft", "short": "Tir à billes d'eau · dès 8 ans",
     "text": "Le jeu de tir stratégique en équipe à billes d'eau, encadré par l'équipe, protections fournies. 300 FCFA la partie.",
     "href": "watersoft-douala/", "img": "Carroussel_2.webp", "alt": "Un joueur vise pendant une partie de Watersoft chez Case Game",
     "en": {"title": "Watersoft", "short": "Water-bead shooting · from age 8", "text": "The team tactical shooting game with water beads, supervised by our staff, protective gear provided. 300 FCFA per game.", "href": "en/watersoft-douala/", "alt": "A player takes aim during a Watersoft game at Case Game"}},
    {"id": "jeux-de-societe", "group": "jouer", "title": "Jeux de société", "short": "Monopoly, Scrabble, échecs · 100 FCFA/h",
     "text": "Monopoly, Scrabble, échecs et jeux de cartes (Belote, Uno…) pour la stratégie, la réflexion et la convivialité. 100 FCFA l'heure, et le gagnant repart avec du temps de jeu vidéo offert.",
     "href": "jeux-de-societe-douala/", "img": "images/jeux-de-societe.webp", "alt": "Une partie de Ludo entre enfants (photo Ab Pixels, Pexels)",
     "en": {"title": "Board games", "short": "Monopoly, Scrabble, chess · 100 FCFA/h", "text": "Monopoly, Scrabble, chess and card games (Belote, Uno…) for strategy, thinking and fun together. 100 FCFA per hour, and the winner gets free video game time.", "href": "en/board-games-douala/", "alt": "Children playing Ludo (photo Ab Pixels, Pexels)"}},
    {"id": "defis", "group": "jouer", "title": "Défis et mini-défis", "short": "Gagne des Games Points gratuitement",
     "text": "4 mini-défis par jour (100 GP) et 3 grands défis par semaine (300 GP) : micro-trottoir, petit bac, cache-cache à l'aveugle, quiz… sans rien acheter.",
     "href": "activites/#defis", "icon": "target",
     "en": {"title": "Challenges and mini-challenges", "short": "Earn Games Points for free", "text": "4 mini-challenges a day (100 GP) and 3 big challenges a week (300 GP): street interviews, word games, blindfolded hide-and-seek, quizzes… without buying anything.", "href": "en/activities/#defis"}},
    {"id": "soutien", "group": "grandir", "title": "Soutien scolaire", "short": "Du CP à la Terminale · dès 5 000 FCFA/mois",
     "text": "Aide aux devoirs, livrets d'exercices et suivi régulier, avec des Games Points pour récompenser l'effort. Trois formules.",
     "href": "soutien-scolaire-new-bell/", "img": "Carroussel_4.webp", "alt": "Un élève reçoit un ticket de Games Points",
     "en": {"title": "Tutoring", "short": "Primary to final year · from 5,000 FCFA/month", "text": "Homework help, exercise booklets and regular follow-up, with Games Points to reward effort. Three plans.", "href": "en/tutoring-new-bell/", "alt": "A student receives a Games Points ticket"}},
    {"id": "ateliers", "group": "grandir", "title": "Ateliers éducatifs", "short": "Gratuits",
     "text": "Présentations et ateliers de discussion sur l'histoire africaine, la géographie, l'environnement, l'art et la citoyenneté.",
     "href": "association/#actions", "img": "Carroussel_11.webp", "alt": "Des jeunes lors d'une journée de l'Association Case Game",
     "en": {"title": "Educational workshops", "short": "Free", "text": "Talks and discussion workshops on African history, geography, the environment, art and citizenship.", "href": "en/association/#actions", "alt": "Young people at an Association Case Game day"}},
    {"id": "gamer-solidaire", "group": "grandir", "title": "Gamer Solidaire et Vert", "short": "Missions pour le quartier",
     "text": "Des missions utiles pour New Bell (aide aux habitants, nettoyage, recyclage) proposées par les jeunes et récompensées en Games Points.",
     "href": "association/#actions", "img": "images/gamer-solidaire-vert.webp", "alt": "Logo du programme Gamer Solidaire et Vert",
     "en": {"title": "Gamer Solidaire et Vert", "short": "Missions for the neighbourhood", "text": "Useful missions for New Bell (helping residents, clean-ups, recycling) suggested by young people and rewarded with Games Points.", "href": "en/association/#actions", "alt": "Logo of the Gamer Solidaire et Vert programme"}},
    {"id": "orphelins", "group": "grandir", "title": "Journées avec les orphelins", "short": "Orphelinat L'Arche de Mummy",
     "text": "Des journées de jeux, d'ateliers et de partage avec les 50 enfants de l'orphelinat L'Arche de Mummy, soutenus par notre campagne de dons.",
     "href": "association/#campagne", "img": "Carroussel_13.webp", "alt": "Des enfants partagent un repas lors d'une journée solidaire",
     "en": {"title": "Days with orphans", "short": "L'Arche de Mummy orphanage", "text": "Days of games, workshops and sharing with the 50 children of L'Arche de Mummy orphanage, supported by our fundraising campaign.", "href": "en/association/#campagne", "alt": "Children share a meal during a solidarity day"}},
]


def activity_visual(a, root, size):
    if a.get("img"):
        return f'<img src="{root}{a["img"]}" alt="" loading="lazy" width="{size}" height="{size}">'
    return f'<span class="act-icon" aria-hidden="true"><svg class="i" viewBox="0 0 24 24">{ICONS[a["icon"]]}</svg></span>'


def loc(a, lang):
    """Textes d'une activité dans la langue demandée (image et icône communes)."""
    return {**a, **a["en"]} if lang == "en" else a


def mega_menu(root, lang="fr"):
    t = L10N[lang]
    cols = []
    for key, label in t["groups"].items():
        items = "\n".join(
            f'            <li><a href="{root}{a["href"]}">{activity_visual(a, root, 56)}'
            f'<span><b>{html.escape(a["title"])}</b><small>{html.escape(a["short"])}</small></span></a></li>'
            for a in (loc(x, lang) for x in ACTIVITIES) if a["group"] == key)
        cols.append(f'          <div>\n            <p class="mega-title">{label}</p>\n            <ul>\n{items}\n            </ul>\n          </div>')
    return (f'<div class="has-mega">\n'
            f'        <a class="mega-trigger" href="{root}{t["activities_path"]}" aria-expanded="false" aria-controls="mega-activites">{t["activities"]} <span class="caret" aria-hidden="true"></span></a>\n'
            f'        <div class="mega" id="mega-activites">\n' + "\n".join(cols) +
            f'\n          <a class="mega-all" href="{root}{t["activities_path"]}">{t["all_activities"]}</a>\n        </div>\n      </div>')


ACTIVITIES_PAGE = {
    "fr": {"path": "activites/", "more": "En savoir plus", "label": "Activités · New Bell, Douala", "h1": "Nos activités",
           "intro": "Jeux vidéo, tournois, Watersoft, jeux de société, défis, soutien scolaire et actions solidaires : tout ce qu'on fait chez Case Game, à New Bell (Douala).",
           "q": "Une question sur une activité ?", "q_text": "Horaires, âge minimum, groupes ou anniversaires : écris-nous sur WhatsApp.", "q_btn": "Nous écrire",
           "title": "Nos activités à Douala – Case Game",
           "description": "Toutes les activités de Case Game à New Bell, Douala : jeux vidéo, tournois, Watersoft, jeux de société, défis, soutien scolaire et actions solidaires.",
           "crumb": "Activités"},
    "en": {"path": "en/activities/", "more": "Find out more", "label": "Activities · New Bell, Douala", "h1": "Our activities",
           "intro": "Video games, tournaments, Watersoft, board games, challenges, tutoring and community action: everything we do at Case Game, in New Bell (Douala).",
           "q": "A question about an activity?", "q_text": "Opening hours, minimum age, groups or birthday parties: message us on WhatsApp.", "q_btn": "Message us",
           "title": "Things to do at Case Game in Douala",
           "description": "All Case Game activities in New Bell, Douala: video games, tournaments, Watersoft, board games, challenges, tutoring and community action for young people.",
           "crumb": "Activities"},
}


def activities_page(lang="fr"):
    p = ACTIVITIES_PAGE[lang]
    blocks = []
    for key, label in L10N[lang]["groups"].items():
        cards = "\n".join(
            f"""    <article class="act-card" id="{a["id"]}">
      {activity_visual(a, "{root}", 400).replace('alt=""', f'alt="{html.escape(a.get("alt", ""))}"')}
      <div>
        <p class="post-cat">{html.escape(a["short"])}</p>
        <h3>{html.escape(a["title"])}</h3>
        <p>{html.escape(a["text"])}</p>
        {"" if a["href"].startswith(p["path"]) else f'<a class="more" href="{{root}}{a["href"]}">{p["more"]} <svg class="i"><use href="#i-arrow"/></svg></a>'}
      </div>
    </article>""" for a in (loc(x, lang) for x in ACTIVITIES) if a["group"] == key)
        blocks.append(f'  <h2>{label}</h2>\n  <div class="act-grid">\n{cards}\n  </div>')
    content = f"""<div class="prose" style="max-width:1100px">
  <p class="label">{p["label"]}</p>
  <h1 style="font-size:clamp(38px,5.6vw,72px);text-transform:uppercase">{p["h1"]}</h1>
  <p class="byline" style="font-size:18px">{p["intro"]}</p>
""" + "\n".join(blocks) + f"""
  <div class="callout">
    <div>
      <b>{p["q"]}</b>
      <p>{p["q_text"]}</p>
    </div>
    <a class="btn solid" href="https://wa.me/237686844407" target="_blank" rel="noopener"><svg class="i"><use href="#i-chat"/></svg> {p["q_btn"]}</a>
  </div>
</div>"""
    meta = {"path": p["path"], "title": p["title"], "description": p["description"],
            "crumb": p["crumb"], "image": "Carroussel_7.jpg"}
    return meta, content


def update_home_menu():
    a_mark, b_mark = "<!-- MENU-ACTIVITES:DEBUT -->", "<!-- MENU-ACTIVITES:FIN -->"
    for file, root, lang in (("index.html", "", "fr"), ("en/index.html", "../", "en")):
        home = ROOT / file
        s = home.read_text(encoding="utf-8")
        if a_mark not in s:
            continue
        a, b = s.index(a_mark) + len(a_mark), s.index(b_mark)
        home.write_text(s[:a] + "\n      " + mega_menu(root, lang) + "\n      " + s[b:], encoding="utf-8", newline="\n")
        print(f"mis à jour {file} (menu Activités)")


BLOG = {
    "fr": ("blog/", "Le blog Case Game",
           "Blog Case Game : résultats des tournois, réussites de la semaine, bilans du mois, dons et cadeaux, et guides gaming à Douala.",
           "Résultats des tournois, réussites de la semaine, bilans du mois, dons et cadeaux, et nos guides : toute l'actualité de Case Game à New Bell, Douala."),
    "en": ("en/blog/", "The Case Game blog",
           "Case Game blog: tournament results, wins of the week, monthly reviews, donations and gifts, and gaming guides for young people in Douala.",
           "Tournament results, wins of the week, monthly reviews, donations and gifts, and our guides: all the news from Case Game in New Bell, Douala."),
}


def build():
    today = date.today().isoformat()
    sources = [parse(p) for p in all_sources()]
    for m, _ in sources:
        if m.get("type") == "article":
            assert m.get("category") in CATEGORIES, f"Rubrique inconnue pour {m['path']} : {m.get('category')}"

    pages = []
    for lang in ("fr", "en"):
        here = [(m, c) for m, c in sources if lang_of(m["path"]) == lang]
        articles = sorted([(m, c) for m, c in here if m.get("type") == "article"],
                          key=lambda mc: mc[0]["date"], reverse=True)
        for meta, content in here:
            if meta.get("type") == "article":
                content = content + related_block(meta, articles)
            pages.append((meta, content))
        path, title, desc, intro = BLOG[lang]
        pages.append(listing_page(articles, path, title, desc, "Blog", intro))
        for key, (name, cat_path, cat_desc) in CATS[lang].items():
            if any(m["category"] == key for m, _ in articles):
                pages.append(listing_page(articles, cat_path, name, cat_desc, name, cat_desc, current=key))
        pages.append(activities_page(lang))
        if lang == "fr":
            fr_articles = articles

    # Paires FR/EN : déclarées dans les sources anglaises (clé « fr: »), plus les pages générées
    built = {m["path"] for m, _ in pages}
    twins = {"blog/": "en/blog/", "activites/": "en/activities/"}
    twins.update({CATEGORIES[k][1]: CATEGORIES_EN[k][1] for k in CATEGORIES})
    twins.update({m["fr"]: m["path"] for m, _ in sources if m.get("fr")})
    twins = {fr: en for fr, en in twins.items() if fr in built and en in built}
    twins.update({en: fr for fr, en in list(twins.items())})

    for meta, content in pages:
        render(meta, content, twins)
    update_home_menu()
    write_feed(fr_articles)
    update_home(fr_articles)
    write_sitemap([("", today), ("en/", today)]
                  + [(m["path"], m.get("updated", m.get("date", today))) for m, _ in pages])

    for m, _ in pages:
        if lang_of(m["path"]) == "fr" and m.get("type") != "legal" and m["path"] not in twins:
            print(f"ATTENTION : pas de version anglaise pour {m['path']} (à créer dans pages/en/)")


if __name__ == "__main__":
    build()
