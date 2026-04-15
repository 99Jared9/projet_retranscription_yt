## ADDED Requirements

### Requirement: Analyser un transcript et retourner points clés + résumé
Le module `claude.py` SHALL exposer une fonction `analyse_transcript(transcript: TranscriptResult, video_url: str) -> AnalysisResult` qui appelle l'API DeepSeek et retourne un résumé introductif et 5 à 8 points clés en français avec timestamps.

`AnalysisResult` est un dataclass contenant :
- `summary: str` — résumé introductif de la vidéo en français (2-4 phrases)
- `key_points: list[KeyPoint]` — 5 à 8 points clés
- `video_url: str` — URL originale de la vidéo

`KeyPoint` est un dataclass contenant :
- `text: str` — description du point clé en français
- `timestamp_seconds: int` — timestamp en secondes dans la vidéo
- `timestamp_label: str` — label lisible, ex. `"1m23s"`

#### Scenario: Transcript valide analysé avec succès
- **WHEN** `analyse_transcript()` reçoit un `TranscriptResult` avec des entrées non vides
- **THEN** la fonction retourne un `AnalysisResult` avec `summary` non vide et entre 5 et 8 `key_points`

#### Scenario: Résultat toujours en français
- **WHEN** le transcript est dans n'importe quelle langue (fr, en, autre)
- **THEN** `summary` et chaque `key_point.text` sont rédigés en français

#### Scenario: Timestamps présents et valides
- **WHEN** le `AnalysisResult` est retourné
- **THEN** chaque `key_point.timestamp_seconds` est un entier ≥ 0 correspondant à un moment du transcript

---

### Requirement: Activation du prompt caching sur le transcript
Le module SHALL structurer les messages pour maximiser le prefix caching automatique de DeepSeek en plaçant le transcript en premier dans le contenu utilisateur.

#### Scenario: Appel API avec transcript long
- **WHEN** `analyse_transcript()` est appelé avec un transcript de plus de 1024 tokens
- **THEN** le transcript est placé en premier dans le message utilisateur pour maximiser les hits du prefix caching DeepSeek

---

### Requirement: Réponse Claude en JSON structuré
Le module SHALL demander à Claude de retourner un JSON avec les champs `summary` (string) et `key_points` (liste d'objets `{text, timestamp_seconds, timestamp_label}`), et SHALL parser ce JSON pour construire l'`AnalysisResult`.

#### Scenario: JSON valide retourné par Claude
- **WHEN** Claude retourne une réponse JSON conforme au schéma attendu
- **THEN** `analyse_transcript()` parse le JSON et retourne un `AnalysisResult` valide

#### Scenario: JSON invalide retourné par Claude
- **WHEN** Claude retourne une réponse non parseable comme JSON valide
- **THEN** `ClaudeAnalysisError` est levée avec le contenu brut de la réponse inclus dans le message

---

### Requirement: Gestion des erreurs API typées
Le module SHALL lever des exceptions typées pour les échecs API, toutes héritant de `ClaudeError`.

Exceptions définies :
- `ClaudeAuthError` — clé API invalide ou absente
- `ClaudeRateLimitError` — limite de taux atteinte
- `ClaudeAnalysisError` — réponse inattendue ou non parseable

#### Scenario: Clé API manquante
- **WHEN** la variable d'environnement `DEEPSEEK_API_KEY` est absente ou invalide
- **THEN** `ClaudeAuthError` est levée avec un message indiquant la variable manquante

#### Scenario: Rate limit atteint
- **WHEN** l'API DeepSeek retourne une erreur de rate limit (429)
- **THEN** `ClaudeRateLimitError` est levée avec un message clair
