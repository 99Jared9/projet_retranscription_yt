## Why

Le pipeline d'extraction YouTube est fonctionnel jusqu'à la génération du `.md` local, mais sans push automatique vers GitHub, l'utilisateur doit pousser manuellement chaque rapport — ce qui annule le gain de temps du CLI. Cette étape complète le MVP en rendant le pipeline entièrement automatisé.

## What Changes

- Ajout du module `github.py` qui envoie le fichier `.md` généré vers un repo GitHub via l'API REST GitHub
- L'appel `PUT /repos/{owner}/{repo}/contents/{path}` crée le fichier directement en base64 — aucun clone local, aucune dépendance git
- `main.py` orchestre l'appel à `github.py` après `markdown.py` et affiche l'URL du fichier créé via `rich`
- Ajout de la variable d'environnement `GITHUB_REPO` au format `owner/repo`

## Capabilities

### New Capabilities
- `github-push`: Envoi du fichier `.md` vers un repo GitHub via `PUT /repos/{owner}/{repo}/contents/{path}` avec authentification par `GITHUB_TOKEN`, encodage base64 du contenu, et retour de l'URL HTML du fichier créé

### Modified Capabilities
- `main-orchestration`: Ajout de l'étape `github.py` à la fin du pipeline et affichage du lien GitHub dans le terminal

## Impact

- Nouveau module : `src/yt_rapport/github.py`
- Modification : `src/yt_rapport/main.py` (appel github.py + affichage rich du lien)
- Dépendance : `httpx` (déjà prévu dans la stack)
- Variables d'environnement requises : `GITHUB_TOKEN`, `GITHUB_REPO`
