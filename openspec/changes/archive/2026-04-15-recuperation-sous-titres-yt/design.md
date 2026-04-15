## Context

Le projet est un CLI Python (`yt-rapport`) dont le pipeline est : URL → transcript → Claude → Markdown → GitHub. Le module `transcript.py` est le premier maillon réel : il transforme une URL YouTube en données structurées (texte + timestamps) consommables par `claude.py`.

La librairie `youtube-transcript-api` est déjà identifiée comme dépendance dans l'architecture. Elle appelle les endpoints YouTube sans clé API, mais reste soumise aux restrictions de YouTube (vidéos privées, sans CC, geo-bloquées).

## Goals / Non-Goals

**Goals:**
- Extraire les sous-titres d'une vidéo YouTube avec leurs timestamps
- Sélectionner automatiquement la meilleure langue disponible (fr > en > première disponible)
- Récupérer les chapitres YouTube si présents
- Lever des exceptions typées et explicites pour chaque cas d'erreur prévisible

**Non-Goals:**
- Fallback Whisper (transcription audio) — hors scope définitif
- Utilisation des chapitres pour structurer l'analyse (V1, pas MVP)
- Chunking des transcripts très longs (V1)
- Cache local des transcripts

## Decisions

### `get_transcript()` retourne un dataclass, pas un dict

**Décision** : utiliser un `dataclass` `TranscriptResult(entries, video_id, language, chapters)` plutôt qu'un dict.

**Pourquoi** : les modules consommateurs (`claude.py`, `main.py`) bénéficient de l'autocomplétion et d'un contrat explicite. Un dict silencieux casse à l'accès ; un dataclass casse tôt avec un message clair.

**Alternative écartée** : retourner un tuple `(entries, chapters)` — pas assez explicite sur ce que contient chaque champ.

---

### Sélection de langue : fr → en → première disponible

**Décision** : tenter dans l'ordre `["fr", "en"]`, puis fallback sur la première langue trouvée via `list_transcripts()`.

**Pourquoi** : les rapports sont toujours en français, mais beaucoup de vidéos pertinentes sont en anglais. Claude traduit dans tous les cas — la langue source n'impacte pas la qualité de l'output.

**Alternative écartée** : forcer uniquement `fr` — trop restrictif pour un outil de veille internationale.

---

### Exceptions typées dans `transcript.py`

**Décision** : définir `TranscriptError` (base), `NoTranscriptAvailable`, `VideoNotFound`, `VideoPrivate` dans ce module.

**Pourquoi** : `main.py` peut afficher des messages d'erreur clairs et distincts via `rich` sans avoir à parser les messages d'exception de la librairie tierce. Isole le code de gestion d'erreur des détails d'implémentation de `youtube-transcript-api`.

**Alternative écartée** : laisser remonter les exceptions brutes de la librairie — couplage fort avec l'API interne d'une dépendance externe.

---

### Chapitres récupérés mais non utilisés en MVP

**Décision** : récupérer les chapitres via `list_transcripts()` si disponibles, les inclure dans `TranscriptResult.chapters`, mais `main.py` ne les passe pas à `claude.py` pour l'instant.

**Pourquoi** : le code de récupération est trivial à ce stade. Ne pas le faire maintenant forcerait un second appel réseau en V1.

## Risks / Trade-offs

- **Rate limiting YouTube** → Pas de retry automatique en MVP. Une erreur réseau remonte proprement. Mitigation V1 : retry avec backoff.
- **Sous-titres auto-générés vs manuels** → La qualité varie. `youtube-transcript-api` expose `is_generated` mais on ne filtre pas — Claude gère la qualité variable du texte.
- **Vidéos sans sous-titres** → `NoTranscriptAvailable` levée immédiatement avec message explicite. Pas de fallback.
