### Requirement: Envoyer le fichier .md vers GitHub via l'API REST
Le système SHALL envoyer le contenu du fichier `.md` vers le repo GitHub cible en utilisant l'endpoint `PUT /repos/{owner}/{repo}/contents/{path}` avec le contenu encodé en base64 et authentifié par `GITHUB_TOKEN`.

#### Scenario: Push réussi
- **WHEN** `push_file(filename, content, commit_message)` est appelé avec un token valide et un repo accessible
- **THEN** le fichier est créé dans le repo et la fonction retourne l'URL HTML du fichier créé

#### Scenario: Token manquant ou invalide
- **WHEN** `GITHUB_TOKEN` est absent ou l'API retourne 401
- **THEN** le système lève une `GitHubAuthError` avec un message demandant de vérifier le token

#### Scenario: Repo introuvable ou accès refusé
- **WHEN** l'API retourne 404 ou 403
- **THEN** le système lève une `GitHubRepoError` avec un message indiquant que le repo `GITHUB_REPO` est introuvable ou inaccessible

#### Scenario: Fichier déjà existant
- **WHEN** l'API retourne 422 (le fichier existe déjà à ce chemin)
- **THEN** le système lève une `GitHubConflictError` avec un message indiquant que le fichier existe déjà

### Requirement: Construire le chemin et le message de commit automatiquement
Le système SHALL construire le chemin du fichier dans le repo (`YYYY-MM-DD-titre.md`) et le message de commit à partir du nom de fichier, sans intervention de l'utilisateur.

#### Scenario: Nom de fichier valide fourni
- **WHEN** `push_file` reçoit un `filename` au format `YYYY-MM-DD-titre.md`
- **THEN** le fichier est créé à la racine du repo avec ce nom exact et un message de commit du type `"feat: YYYY-MM-DD-titre"`

### Requirement: Lire la configuration depuis les variables d'environnement
Le module SHALL lire `GITHUB_TOKEN` et `GITHUB_REPO` depuis les variables d'environnement. Le pipeline SHALL échouer immédiatement si l'une d'elles est absente.

#### Scenario: Variables d'environnement présentes
- **WHEN** `GITHUB_TOKEN` et `GITHUB_REPO` sont définies
- **THEN** le module s'initialise sans erreur

#### Scenario: Variable d'environnement manquante
- **WHEN** `GITHUB_TOKEN` ou `GITHUB_REPO` est absente au démarrage de `main.py`
- **THEN** le système affiche un message d'erreur explicite via `rich` et quitte avec un code non-zéro avant tout appel réseau
