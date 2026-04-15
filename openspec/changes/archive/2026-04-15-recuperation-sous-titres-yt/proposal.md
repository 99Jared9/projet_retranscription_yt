## Why

Le pipeline CLI a un point d'entrée (`main.py`) mais aucune capacité à récupérer des données. Sans les sous-titres YouTube, aucune analyse Claude ni génération de rapport n'est possible — c'est le premier maillon du pipeline.

## What Changes

- Implémentation du module `transcript.py` : extraction des sous-titres via `youtube-transcript-api`
- Sélection automatique de la langue (français en priorité, anglais en fallback)
- Retour du transcript brut avec timestamps `(text, start, duration)` pour les timecodes
- Retour des chapitres YouTube si présents (None sinon) — préparation V1, non utilisé en MVP
- Erreurs propres et explicites : vidéo sans CC, vidéo privée/introuvable, URL invalide

## Capabilities

### New Capabilities

- `youtube-transcript`: Extraction des sous-titres d'une vidéo YouTube avec timestamps et chapitres optionnels

### Modified Capabilities

<!-- Aucune spec existante à modifier -->

## Impact

- **Nouveau fichier** : `src/yt_rapport/transcript.py`
- **Dépendance** : `youtube-transcript-api` (à ajouter dans `pyproject.toml`)
- **Consommé par** : `main.py` (orchestration) puis `claude.py` (analyse)
- **Aucun appel réseau externe** autre que YouTube — pas d'impact sur les autres modules pour ce changement
