## Why

L'outil doit être utilisable en ligne de commande : l'utilisateur passe une URL YouTube en argument et obtient un rapport sans friction. Sans cette fonctionnalité, rien d'autre dans le pipeline ne peut être déclenché.

## What Changes

- Création du point d'entrée CLI `yt-rapport` via Typer
- Acceptance et validation d'une URL YouTube en argument positionnel
- Orchestration du pipeline (transcript → analyse → markdown → push GitHub) depuis `main.py`
- Affichage des erreurs propres dans le terminal via `rich` si l'URL est invalide

## Capabilities

### New Capabilities

- `cli-entrypoint`: Point d'entrée Typer exposant la commande `yt-rapport <url>` — valide l'URL, orchestre le pipeline, affiche progression et résultat dans le terminal

### Modified Capabilities

<!-- Aucune spec existante à modifier -->

## Impact

- Nouveau fichier `src/yt_rapport/main.py` (entry point Typer)
- `pyproject.toml` : déclaration du script `yt-rapport = "yt_rapport.main:app"`
- Dépendances ajoutées : `typer`, `rich`
- Les autres modules (`transcript.py`, `claude.py`, `markdown.py`, `github.py`) sont appelés depuis `main.py` mais ne sont pas créés dans ce change
