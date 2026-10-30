# Case Game – site casegamecm.com

Site vitrine de Case Game SAS (salle de jeux vidéo, New Bell, Douala, Cameroun) et de l'Association Case Game.
Réponds toujours en français, simplement : le propriétaire n'est pas développeur.

## Sessions dans le cloud (depuis le téléphone)
- Le client lance souvent Claude depuis son téléphone (claude.ai/code, dépôt `Airman-code/CaseGame`).
- Dans ce cas : pas d'accès à son Chrome (Google, Facebook, Bing…) ; tout se fait par le dépôt.
  Travailler sur `main`, `git pull` avant, `python build.py`, vérifier, puis pousser sur `main` après accord du client
  (si la session a créé une branche, la fusionner dans `main`, sinon rien n'est en ligne).
- Ce dossier `.claude/` est dans le dépôt (public) mais n'est pas servi par le site. Ne jamais y mettre de mot de passe.

## Fonctionnement technique
- Site statique hébergé sur GitHub Pages (dépôt `Airman-code/CaseGame`, branche `main`), domaine OVH `casegamecm.com`.
- Tout push sur `main` est en ligne en 1 à 2 minutes. Toujours `git pull` avant de pousser
  (un robot GitHub met à jour `assets/cagnotte.json` toutes les 6 h).
- Git est configuré pour le compte Airman-code dans ce dossier ; le push fonctionne directement.
- `python build.py` régénère : pages thématiques et légales (sources dans `pages/` et `legal/`),
  blog (page, rubriques, RSS), menu et page Activités (liste `ACTIVITIES` dans build.py),
  « Actualités » de l'accueil et `sitemap.xml`. Ne jamais modifier à la main les .html générés.
- `index.html` (accueil FR) et `en/index.html` (accueil EN) sont écrits à la main
  (sauf les zones entre les commentaires `ACTUS` et `MENU-ACTIVITES`).
- Styles : `assets/site.css` ; scripts : `assets/site.js`.
- Prévisualiser : `python -m http.server 8080` dans ce dossier (config `site` dans `.claude/launch.json`).
- Avant de publier : vérifier sur ordinateur et mobile (375 px), puis relancer un test SEO
  (titres 30–65 car., descriptions 120–160 car., un seul h1, liens internes OK).
- Sauvegarde de version : tag git `avant-ameliorations`.

## Charte et règles de contenu
- Charte noir et blanc uniquement (pas de jaune), logo Case Game noir sur blanc.
- Polices auto-hébergées (Chakra Petch, Manrope), aucune ressource Google chargée sans clic.
- Aucun cookie : la carte Google Maps ne se charge qu'au clic. Garder ce principe (RGPD + loi camerounaise n° 2024/017).
- Pas d'images générées par IA. Vraies photos de Case Game en priorité ; sinon Pexels (licence vérifiée, crédit dans les mentions légales).
- Photos en WebP redimensionné (max 1200 px). Vidéos : `preload="none"`.
- Mineurs : photos seulement avec accord des parents (le client a les accords pour les photos actuelles).
- Ne jamais inventer de faits (prix, résultats, jeux proposés, ex. pas de tournoi Tekken). Demander si doute.
- Prix en FCFA TTC. Watersoft : billes d'eau, dès 8 ans. Jeux de société : 100 FCFA l'heure, carnet de 5 à 500 FCFA.
- Adresse : Hôtel Fatime Babylone, rue du Roi Njoya, New Bell, Douala. Tél./WhatsApp : +237 6 86 84 44 07.
- Note Google affichée à la main (5,0 – 4 avis) : à mettre à jour quand le client donne de nouveaux chiffres.

## Blog
- Rubriques : resultats, reussites, bilans, dons, guides. Modèles dans `modeles-blog/`.
- Le client envoie les infos (résultats, réussites, dons…) ; écrire l'article dans `pages/blog/`, lancer `build.py`, publier.
- Donateurs nommés seulement avec leur accord ; chiffres vérifiés uniquement.

## Comptes et outils (le client se connecte lui-même)
- Google Search Console et fiche Google Maps : 4e compte Google ouvert dans Chrome (`authuser=3`).
- Bing Webmaster Tools : site vérifié (fichier `BingSiteAuth.xml`, ne pas supprimer). Idem `googlec9c123980e7ae12f.html`.
- Cagnotte GoFundMe : https://www.gofundme.com/f/renforcer-la-reussite-scolaire-des-orphelins (barre automatique).
- Documents du client : dossier OneDrive « Activites Case Game » (fiches de protocole par activité).

## À faire / en attente
- Vidéo de la page Jeux de société (lien YouTube à recevoir).
- Vraies photos pour « Défis et mini-défis » (icône en attendant).
- Remonter la vidéo de présentation (ancien numéro 693 46 52 85 incrusté).
- Côté client : consentement dans les Google Forms, assurance RC, liens du site sur les réseaux, avis Google.
- Google : catégories « Club de jeux de société » et « Service de soutien scolaire » envoyées le 30/10/2026 (examen jusqu'à 7 jours). Une fois publiées : resynchroniser Bing Places (importé de Google, catégories non modifiables côté Bing).
- Adresse à harmoniser : fiche Google « Rue Mi Njoya, en bas de la résidence Tchameni », Facebook « Av. de l'Indépendance, rond-point Shell », site « Hôtel Fatime Babylone, rue du Roi Njoya ». Demander au client la bonne. Yandex affiche l'ancien numéro 693 46 52 85.
- Annuaires : kit prêt dans `.claude/fiche-annuaires.md` (non servi par le site : Jekyll ignore les dossiers en point) : infos, descriptions FR/EN, liste des sites, message Petit Futé, tableau de suivi. Le client crée les comptes ; mettre la fiche à jour si infos changent.
