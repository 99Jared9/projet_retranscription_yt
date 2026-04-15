## Why

Le pipeline dispose déjà d'un module d'extraction de transcript (`transcript.py`). Il faut maintenant transformer ce transcript brut en contenu structuré et exploitable : un résumé intro et 5 à 8 points clés avec timecodes, toujours en français. C'est le cœur analytique du MVP sans lequel aucun rapport ne peut être généré.

## What Changes

- Ajout du module `claude.py` — construit le prompt à partir du transcript, appelle l'API DeepSeek avec `deepseek-chat`, retourne les points clés structurés avec timestamps
- Activation du **prompt caching** sur le bloc transcript pour réduire coût et latence sur les retries
- Le module expose une fonction principale `analyse_transcript(transcript, video_url)` utilisée par `main.py`

## Capabilities

### New Capabilities

- `claude-analysis`: Appel à l'API DeepSeek pour analyser un transcript YouTube et produire un résumé + points clés structurés en français avec timestamps

### Modified Capabilities

- `cli-entrypoint`: Intégration de l'étape d'analyse dans le pipeline d'orchestration de `main.py`

## Impact

- Nouveau fichier : `src/yt_rapport/claude.py`
- Dépendance : `anthropic` SDK (déjà dans `pyproject.toml` selon l'architecture)
- Variable d'environnement requise : `DEEPSEEK_API_KEY`
- `main.py` est mis à jour pour appeler `analyse_transcript()` après `get_transcript()`
