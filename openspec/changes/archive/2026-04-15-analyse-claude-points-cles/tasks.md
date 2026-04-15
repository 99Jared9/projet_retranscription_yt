## 1. Structures de données

- [x] 1.1 Définir le dataclass `KeyPoint` avec les champs `text`, `timestamp_seconds`, `timestamp_label`
- [x] 1.2 Définir le dataclass `AnalysisResult` avec les champs `summary`, `key_points`, `video_url`
- [x] 1.3 Définir la hiérarchie d'exceptions : `ClaudeError`, `ClaudeAuthError`, `ClaudeRateLimitError`, `ClaudeAnalysisError`

## 2. Prompt et appel API

- [x] 2.1 Écrire le prompt système qui demande une analyse en français avec JSON structuré (`summary` + `key_points`)
- [x] 2.2 Implémenter la construction du message `user` avec le transcript en texte brut
- [x] 2.3 Structurer le message pour placer le transcript en premier (prefix caching automatique DeepSeek)
- [x] 2.4 Appeler `client.chat.completions.create()` avec le modèle `deepseek-chat`

## 3. Parsing et gestion d'erreurs

- [x] 3.1 Parser le JSON retourné par Claude et construire l'`AnalysisResult`
- [x] 3.2 Gérer le cas où le JSON est invalide → lever `ClaudeAnalysisError` avec le contenu brut
- [x] 3.3 Intercepter les erreurs DeepSeek/OpenAI SDK (`AuthenticationError`, `RateLimitError`) et les convertir en exceptions typées

## 4. Intégration dans le pipeline

- [x] 4.1 Importer et appeler `analyse_transcript()` dans `main.py` après `get_transcript()`
- [x] 4.2 Ajouter un message `rich` "Analyse en cours..." avant l'appel Claude
- [x] 4.3 Gérer les exceptions `ClaudeError` dans `main.py` et afficher un message d'erreur rouge via `rich`
