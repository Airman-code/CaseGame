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
- `legal/*.part.html` et `pages/**/*.part.html` – sources des pages légales, des pages thématiques
  (tournois, Watersoft, soutien scolaire, association) et du blog ; `python build.py` génère les pages HTML.
  Pour un nouvel article : copier un fichier de `pages/blog/`, changer l'en-tête et le contenu, l'ajouter
  à `pages/blog/index.part.html` et à `sitemap.xml`, puis lancer `python build.py`.
- `llms.txt`, `sitemap.xml`, `robots.txt` – référencement (Google, Bing, assistants IA)

## Mettre à jour la cagnotte

Automatique : `.github/workflows/cagnotte.yml` lance `scripts/update_cagnotte.py` toutes les 6 heures.
Le script lit la page publique GoFundMe et met à jour `assets/cagnotte.json` (montant, objectif, donateurs) ;
la barre des pages FR et EN se met à jour toute seule. Lancement manuel : onglet Actions de GitHub → « Mise à jour de la cagnotte » → Run workflow.

## Publier

Toute modification poussée sur la branche `main` est mise en ligne automatiquement par GitHub Pages.
