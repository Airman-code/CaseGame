# Modèles d'articles du blog

Ces fichiers ne sont pas publiés. Pour créer un article :

1. Copier le modèle voulu dans `pages/blog/` avec un nom court
   (ex. `pages/blog/tournoi-hebdo-2026-11-08.part.html`).
2. Remplir l'en-tête (`path`, `title`, `description`, `date`, `image`) et remplacer tout ce qui est entre [crochets].
3. Mettre les photos dans `blog/photos/` (format paysage, 1200 px de large suffit).
4. Lancer `python build.py` puis publier sur `main`.

La page Blog, les rubriques, le flux RSS, le sitemap et les « Actualités » de l'accueil se mettent à jour tout seuls.

Rubriques possibles (`category:`) : `resultats`, `reussites`, `bilans`, `dons`, `guides`.

Règles :
- Photos de mineurs : uniquement avec l'accord écrit des parents ou du tuteur.
- Dons : ne citer le nom d'un donateur qu'avec son accord ; sinon « un donateur de la diaspora ».
- Montants et résultats : uniquement des chiffres vérifiés.
