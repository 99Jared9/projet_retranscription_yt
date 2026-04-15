## 1. Dépendances et structure

- [x] 1.1 Ajouter `youtube-transcript-api` dans `pyproject.toml` et lancer `uv lock`
- [x] 1.2 Créer le fichier `src/yt_rapport/transcript.py` vide

## 2. Types et exceptions

- [x] 2.1 Définir le dataclass `TranscriptResult` avec les champs `entries`, `video_id`, `language`, `chapters`
- [x] 2.2 Définir la hiérarchie d'exceptions : `TranscriptError` (base), `NoTranscriptAvailable`, `VideoNotFound`, `VideoPrivate`

## 3. Extraction du video_id

- [x] 3.1 Implémenter `extract_video_id(url: str) -> str` supportant les formats `youtube.com/watch?v=` et `youtu.be/`
- [x] 3.2 Lever `VideoNotFound` si aucun `video_id` n'est trouvé dans l'URL

## 4. Récupération des sous-titres

- [x] 4.1 Implémenter la sélection de langue : tenter `fr` puis `en` puis première langue disponible via `list_transcripts()`
- [x] 4.2 Mapper les exceptions de `youtube-transcript-api` vers `NoTranscriptAvailable`, `VideoNotFound`, `VideoPrivate`
- [x] 4.3 Retourner les `entries` sous forme de liste de dicts `{text, start, duration}`

## 5. Récupération des chapitres

- [x] 5.1 Tenter de récupérer les chapitres YouTube depuis la réponse `list_transcripts()` — retourner `None` si absent

## 6. Fonction publique et intégration

- [x] 6.1 Implémenter `get_transcript(url: str) -> TranscriptResult` en orchestrant les étapes précédentes
- [x] 6.2 Brancher `get_transcript()` dans `main.py` à la place du placeholder actuel et vérifier l'exécution end-to-end avec une URL réelle
