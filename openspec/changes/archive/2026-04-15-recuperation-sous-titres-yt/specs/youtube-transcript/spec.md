## ADDED Requirements

### Requirement: Extraction des sous-titres avec timestamps
Le module `transcript.py` SHALL exposer une fonction `get_transcript(url: str) -> TranscriptResult` qui extrait les sous-titres d'une vidéo YouTube et les retourne avec leurs timestamps.

`TranscriptResult` est un dataclass contenant :
- `entries: list[dict]` — chaque entrée a les champs `text`, `start` (float, secondes), `duration` (float)
- `video_id: str` — l'identifiant extrait de l'URL
- `language: str` — code langue des sous-titres sélectionnés
- `chapters: list[dict] | None` — chapitres YouTube si disponibles, sinon `None`

#### Scenario: Vidéo avec sous-titres français
- **WHEN** l'URL pointe vers une vidéo YouTube publique avec des sous-titres en français
- **THEN** `get_transcript()` retourne un `TranscriptResult` avec `entries` non vides et `language == "fr"`

#### Scenario: Vidéo avec sous-titres uniquement en anglais
- **WHEN** l'URL pointe vers une vidéo YouTube publique sans sous-titres français mais avec sous-titres anglais
- **THEN** `get_transcript()` retourne un `TranscriptResult` avec `language == "en"`

#### Scenario: Vidéo avec sous-titres dans une autre langue uniquement
- **WHEN** l'URL pointe vers une vidéo YouTube sans fr ni en, mais avec des sous-titres dans une autre langue
- **THEN** `get_transcript()` retourne un `TranscriptResult` avec la première langue disponible

---

### Requirement: Extraction de l'identifiant vidéo depuis l'URL
Le module SHALL extraire le `video_id` depuis les formats d'URL YouTube standards.

Formats supportés :
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&t=123s`

#### Scenario: URL format long standard
- **WHEN** l'URL est au format `youtube.com/watch?v=XXXX`
- **THEN** `video_id` extrait est `XXXX`

#### Scenario: URL format court
- **WHEN** l'URL est au format `youtu.be/XXXX`
- **THEN** `video_id` extrait est `XXXX`

---

### Requirement: Gestion des erreurs explicites
Le module SHALL lever des exceptions typées pour chaque cas d'erreur prévisible, toutes héritant de `TranscriptError`.

Exceptions définies :
- `NoTranscriptAvailable` — la vidéo existe mais n'a pas de sous-titres
- `VideoNotFound` — la vidéo n'existe pas ou l'URL est invalide
- `VideoPrivate` — la vidéo est privée ou non accessible

#### Scenario: Vidéo sans sous-titres
- **WHEN** la vidéo existe mais n'a aucun sous-titre disponible
- **THEN** `NoTranscriptAvailable` est levée avec un message indiquant l'URL

#### Scenario: Vidéo privée
- **WHEN** la vidéo est privée ou a été supprimée
- **THEN** `VideoPrivate` ou `VideoNotFound` est levée selon le cas

#### Scenario: URL YouTube invalide
- **WHEN** l'URL ne contient pas de `video_id` reconnaissable
- **THEN** `VideoNotFound` est levée avant toute tentative réseau

---

### Requirement: Récupération des chapitres YouTube
Le module SHALL tenter de récupérer les chapitres YouTube et les inclure dans `TranscriptResult.chapters` si disponibles.

#### Scenario: Vidéo avec chapitres
- **WHEN** la vidéo a des chapitres YouTube définis
- **THEN** `TranscriptResult.chapters` est une liste non vide avec au minimum les champs `title` et `start_time`

#### Scenario: Vidéo sans chapitres
- **WHEN** la vidéo n'a pas de chapitres YouTube
- **THEN** `TranscriptResult.chapters` est `None`
