# Case Game – site web

Site vitrine de **Case Game**, salle de jeux vidéo et d'esport à New Bell, Douala (Cameroun), et de l'**Association Case Game**.

En ligne : https://casegamecm.com (hébergé sur GitHub Pages, domaine chez OVH).

## Structure

- `index.html` – page d'accueil (français)
- `en/index.html` – page d'accueil (anglais)
- `assets/site.css`, `assets/site.js` – styles et scripts communs
- `fonts/` – polices auto-hébergées (Chakra Petch, Manrope, licence OFL)
- `equipe/` – portraits de l'équipe
- `video/` – vidéo de présentation compressée
- `legal/*.part.html` – contenu des pages légales ; `python legal/_build.py` régénère
  `mentions-legales.html`, `confidentialite.html`, `cookies.html`, `cgu.html` et `remboursement.html`
- `llms.txt`, `sitemap.xml`, `robots.txt` – référencement (Google, Bing, assistants IA)

## Mettre à jour la cagnotte

Dans `index.html`, modifier `data-raised` (montant en €) et `data-donors` sur l'élément `id="goal"`.
La barre de progression s'affiche dès que le montant est supérieur à 0.

## Publier

Toute modification poussée sur la branche `main` est mise en ligne automatiquement par GitHub Pages.
