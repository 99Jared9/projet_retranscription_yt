## ADDED Requirements

### Requirement: Accepter une URL YouTube en argument positionnel
La commande `yt-rapport` SHALL accepter une URL YouTube comme seul argument positionnel obligatoire.

#### Scenario: URL fournie en argument
- **WHEN** l'utilisateur exécute `yt-rapport <url>`
- **THEN** le système accepte l'URL et démarre le pipeline

#### Scenario: Aucun argument fourni
- **WHEN** l'utilisateur exécute `yt-rapport` sans argument
- **THEN** le système affiche un message d'erreur et le texte d'aide, puis quitte avec un code non-zéro

### Requirement: Valider le format de l'URL YouTube
Le système SHALL vérifier que l'URL passée correspond à un format YouTube reconnu (`youtube.com/watch` ou `youtu.be/`) avant de lancer le pipeline.

#### Scenario: URL YouTube valide
- **WHEN** l'URL contient `youtube.com/watch` ou `youtu.be/`
- **THEN** le pipeline est lancé normalement

#### Scenario: URL non-YouTube
- **WHEN** l'URL ne correspond à aucun format YouTube reconnu
- **THEN** le système affiche un message d'erreur clair via `rich` et quitte avec un code non-zéro sans appeler le pipeline

### Requirement: Afficher la progression dans le terminal
Le système SHALL utiliser `rich` pour afficher l'état d'avancement du pipeline dans le terminal.

#### Scenario: Pipeline démarré
- **WHEN** le pipeline commence à s'exécuter
- **THEN** le terminal affiche un message indiquant le traitement de l'URL

#### Scenario: Étape d'analyse en cours
- **WHEN** `main.py` appelle `analyse_transcript()` après l'extraction du transcript
- **THEN** le terminal affiche un message indiquant que l'analyse est en cours (ex. "Analyse en cours...")

#### Scenario: Pipeline terminé avec succès
- **WHEN** tous les modules du pipeline s'exécutent sans erreur
- **THEN** le terminal affiche l'URL GitHub du fichier créé

#### Scenario: Erreur dans le pipeline
- **WHEN** un module du pipeline lève une exception (y compris `ClaudeAuthError`, `ClaudeRateLimitError`, `ClaudeAnalysisError`)
- **THEN** le système affiche un message d'erreur lisible via `rich` (style rouge) et quitte avec un code non-zéro

### Requirement: Exposer une commande installable via uv
Le package SHALL déclarer un script `yt-rapport` dans `pyproject.toml` pointant vers le `app` Typer de `main.py`.

#### Scenario: Installation du package
- **WHEN** l'utilisateur installe le package via `uv pip install -e .`
- **THEN** la commande `yt-rapport` est disponible dans le PATH de l'environnement

#### Scenario: Aide disponible
- **WHEN** l'utilisateur exécute `yt-rapport --help`
- **THEN** le terminal affiche la description de la commande et la liste des arguments
