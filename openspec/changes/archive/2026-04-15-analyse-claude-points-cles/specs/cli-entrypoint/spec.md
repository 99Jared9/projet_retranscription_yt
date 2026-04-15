## MODIFIED Requirements

### Requirement: Afficher la progression dans le terminal
Le système SHALL utiliser `rich` pour afficher l'état d'avancement du pipeline dans le terminal.

#### Scenario: Pipeline démarré
- **WHEN** le pipeline commence à s'exécuter
- **THEN** le terminal affiche un message indiquant le traitement de l'URL

#### Scenario: Étape d'analyse Claude en cours
- **WHEN** `main.py` appelle `analyse_transcript()` après l'extraction du transcript
- **THEN** le terminal affiche un message indiquant que l'analyse Claude est en cours (ex. "Analyse en cours...")

#### Scenario: Pipeline terminé avec succès
- **WHEN** tous les modules du pipeline s'exécutent sans erreur
- **THEN** le terminal affiche l'URL GitHub du fichier créé

#### Scenario: Erreur dans le pipeline
- **WHEN** un module du pipeline lève une exception (y compris `ClaudeAuthError`, `ClaudeRateLimitError`, `ClaudeAnalysisError`)
- **THEN** le système affiche un message d'erreur lisible via `rich` (style rouge) et quitte avec un code non-zéro
