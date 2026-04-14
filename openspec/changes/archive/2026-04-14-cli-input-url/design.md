## Context

Le projet part de zéro : aucun code n'existe encore. Ce change pose la première brique — le point d'entrée CLI — sans lequel aucun autre module ne peut être invoqué. Les autres modules (`transcript`, `claude`, `markdown`, `github`) seront des stubs ou absents à ce stade ; `main.py` les appellera en séquence une fois qu'ils existeront.

Stack décidée dans `CLAUDE.md` : Python 3.12+, `uv`, `typer`, `rich`. Packaging via `pyproject.toml`.

## Goals / Non-Goals

**Goals:**
- Exposer la commande `yt-rapport <url>` installable via `uv`
- Valider que l'argument est une URL YouTube syntaxiquement valide avant de lancer le pipeline
- Afficher progression et erreurs dans le terminal via `rich`
- Orchestrer l'appel séquentiel des modules pipeline (même si ceux-ci sont des stubs)

**Non-Goals:**
- Implémentation des modules `transcript`, `claude`, `markdown`, `github` (autres changes)
- Mode batch / liste d'URLs (V2 du PRD)
- Interface interactive ou prompt de confirmation

## Decisions

### Typer comme framework CLI

Typer génère automatiquement `--help`, gère les types Python nativement et est extensible au batch (V2) sans refonte. Alternative écartée : `argparse` (verbeux, pas de typage natif) et `click` (Typer en est une surcouche, autant aller directement).

### Validation URL côté CLI (avant pipeline)

La validation se fait dans `main.py` avec une regex simple (`youtube.com/watch?v=` ou `youtu.be/`). Cela évite de déclencher des appels réseau coûteux pour une URL manifestement invalide. Les cas limites (URL valide mais vidéo privée) sont gérés dans `transcript.py`, hors scope de ce change.

### `rich` pour l'affichage terminal

Cohérent avec `CLAUDE.md`. Un `Console` partagé affiche la progression via `console.print` et les erreurs via `console.print(..., style="red")`. Pas de spinner complexe dans ce change — juste les messages essentiels.

### Stubs pour les modules non-encore-implémentés

`main.py` importe et appelle les modules pipeline. Pour que le CLI soit testable dès maintenant, les modules absents lèvent `NotImplementedError` ou retournent des valeurs fictives. Cela ne bloque pas le test du parsing d'arguments.

## Risks / Trade-offs

- **Regex URL trop stricte** → Rejette des URLs valides (ex. URLs avec paramètres supplémentaires) → Mitigation : regex permissive qui accepte tout `youtube.com` ou `youtu.be`, la vraie validation étant dans `transcript.py`
- **Dépendance à l'ordre d'implémentation des autres modules** → `main.py` ne peut pas être testé de bout en bout sans les autres modules → Mitigation : stubs ou mocks dans les tests unitaires du CLI
