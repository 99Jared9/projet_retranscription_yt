## Context

Le pipeline est fonctionnel de l'URL jusqu'au `.md` local (transcript → analyse → markdown). Il manque la dernière étape : envoyer le fichier `.md` dans un repo GitHub et afficher le lien dans le terminal. Le module `github.py` prévu dans l'architecture n'existe pas encore.

Contraintes connues :
- Pas de clone local — l'API REST GitHub (`PUT /contents/{path}`) suffit
- Authentification par `GITHUB_TOKEN` (scope `repo`)
- `httpx` est déjà dans la stack comme dépendance
- `GITHUB_REPO` au format `owner/repo` défini en variable d'environnement

## Goals / Non-Goals

**Goals:**
- Créer `github.py` avec une fonction `push_file(path, content, message)` qui envoie le `.md` via l'API GitHub REST
- Intégrer l'appel dans `main.py` après `markdown.py`
- Afficher l'URL HTML du fichier créé via `rich` dans le terminal
- Gérer les erreurs HTTP (401, 403, 422) avec des messages clairs

**Non-Goals:**
- Clone git local
- Mise à jour de fichiers existants (le nom inclut la date — collisions peu probables ; le MVP crée seulement)
- Branches, PRs ou tags — commit direct sur la branche par défaut

## Decisions

### PUT /contents/{path} sans clone local
L'endpoint GitHub `PUT /repos/{owner}/{repo}/contents/{path}` crée un fichier en une seule requête HTTP. Pas de dépendance sur git installé, pas de config SSH/HTTPS. Le contenu est encodé en base64 dans le body JSON.

Alternative écartée : `GitPython` ou subprocess git — ajoute une dépendance lourde et requiert un clone local, contraire aux décisions d'architecture.

### httpx synchrone (pas async)
Le pipeline est entièrement séquentiel — pas de concurrence. Utiliser `httpx` en mode synchrone (`httpx.put(...)`) suffit et évite d'introduire `asyncio` pour un seul appel réseau.

Alternative écartée : `requests` — `httpx` est déjà prévu dans la stack ; ajouter `requests` serait redondant.

### Variables d'environnement au démarrage
`main.py` vérifie la présence de `GITHUB_TOKEN` et `GITHUB_REPO` avant de lancer le pipeline. Fail-fast avant tout traitement coûteux (appel API DeepSeek, etc.).

## Risks / Trade-offs

- **Collision de noms de fichiers** → Si deux rapports sont générés le même jour pour la même vidéo, le `PUT` échoue avec 422 (le fichier existe déjà). Mitigation MVP : l'erreur est interceptée et un message clair est affiché. La gestion de l'overwrite (via `sha`) est V1.
- **Expiration du GITHUB_TOKEN** → Erreur 401 interceptée avec message explicite demandant à renouveler le token.
- **Repo inexistant ou mauvaise permission** → Erreur 404/403 interceptée avec message guidant l'utilisateur.
