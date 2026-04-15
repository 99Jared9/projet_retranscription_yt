## 1. Dépendances et configuration

- [x] 1.1 Vérifier que `httpx` est dans `pyproject.toml` (l'ajouter si absent)
- [x] 1.2 Définir les exceptions custom `GitHubAuthError`, `GitHubRepoError`, `GitHubConflictError` dans `github.py`

## 2. Module github.py

- [x] 2.1 Créer `src/yt_rapport/github.py` avec la fonction `push_file(filename: str, content: str) -> str`
- [x] 2.2 Implémenter la lecture de `GITHUB_TOKEN` et `GITHUB_REPO` depuis `os.environ`
- [x] 2.3 Implémenter l'encodage base64 du contenu et l'appel `PUT /repos/{owner}/{repo}/contents/{filename}` via `httpx`
- [x] 2.4 Construire le message de commit automatiquement à partir du nom de fichier (`"feat: {stem}"`)
- [x] 2.5 Retourner l'URL HTML du fichier créé depuis la réponse JSON (`response["content"]["html_url"]`)
- [x] 2.6 Intercepter les codes HTTP 401, 403/404, 422 et lever les exceptions correspondantes avec messages explicites

## 3. Intégration dans main.py

- [x] 3.1 Ajouter la vérification de `GITHUB_TOKEN` et `GITHUB_REPO` en début de `main()` — fail-fast avant tout appel réseau
- [x] 3.2 Appeler `push_file()` après la génération du `.md` par `markdown.py`
- [x] 3.3 Afficher l'URL retournée via `rich` (style lien cliquable)
- [x] 3.4 Intercepter `GitHubAuthError`, `GitHubRepoError`, `GitHubConflictError` dans le bloc de gestion d'erreurs de `main.py` avec messages en rouge
