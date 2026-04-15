## Context

Le module `transcript.py` existe et expose `get_transcript(url) -> TranscriptResult`. Le pipeline dans `main.py` appelle déjà ce module. Il faut maintenant ajouter `claude.py` comme étape suivante : prendre le `TranscriptResult`, l'envoyer à l'API DeepSeek, et retourner un résultat structuré (résumé + points clés).

Contraintes issues de l'architecture :
- Modèle : `deepseek-chat`
- SDK : `anthropic` Python (pas de LangChain)
- Context caching activé sur les transcripts longs (décision d'architecture)
- Output toujours en français

## Goals / Non-Goals

**Goals:**
- Module `claude.py` avec une fonction principale `analyse_transcript(transcript: TranscriptResult, video_url: str) -> AnalysisResult`
- Context caching (prefix caching automatique DeepSeek) sur le bloc transcript
- Résultat structuré : résumé intro + 5 à 8 points clés avec timestamps (secondes)
- Gestion d'erreur typée pour les échecs API (auth, rate limit, réseau)
- Intégration dans l'orchestration de `main.py`

**Non-Goals:**
- Chunking des transcripts très longs (V1)
- Utilisation des chapitres comme guide d'analyse (V1)
- Streaming de la réponse Claude
- Retry automatique avec backoff

## Decisions

### Décision 1 : Structure de la réponse Claude — JSON parsé vs texte libre

**Choix : demander à Claude de répondre en JSON structuré via un prompt strict.**

Le prompt instruite DeepSeek à retourner un objet JSON avec les champs `summary` (string) et `key_points` (liste d'objets `{text, timestamp_seconds, timestamp_label}`). Ce JSON est parsé par `claude.py` et retourné comme dataclass `AnalysisResult`.

Alternative écartée : texte Markdown libre parsé par regex — fragile, couplé au format de sortie, difficile à faire évoluer.

### Décision 2 : Context caching DeepSeek

**Choix : structurer le message pour que le transcript soit en tête du contenu utilisateur, afin de maximiser les hits du prefix caching automatique de DeepSeek.**

DeepSeek applique le context caching automatiquement sur les préfixes stables — le transcript, envoyé en premier dans le message, est la partie la plus longue et la plus coûteuse. En cas de retry, le préfixe est déjà caché.

Alternative écartée : mettre le transcript après les instructions — le prefix caching ne peut pas s'appliquer si le préfixe change entre appels.

### Décision 3 : Type de retour — dataclass vs dict

**Choix : dataclass `AnalysisResult`** pour la cohérence avec `TranscriptResult` et la lisibilité dans `main.py`.

```python
@dataclass
class KeyPoint:
    text: str
    timestamp_seconds: int
    timestamp_label: str  # ex. "1m23s"

@dataclass
class AnalysisResult:
    summary: str
    key_points: list[KeyPoint]
    video_url: str
```

## Risks / Trade-offs

- **[Risque] Réponse Claude non-JSON valide** → Le prompt inclut des instructions strictes + un exemple. Si le parsing échoue, `ClaudeAnalysisError` est levée avec le contenu brut pour debug.
- **[Risque] Transcript très long dépasse la fenêtre de contexte** → Non traité au MVP (chunking V1). Pour l'instant, le transcript est envoyé en entier ; la plupart des vidéos courantes rentrent dans 200k tokens.
- **[Trade-off] Context caching DeepSeek = prefix caching automatique** → Efficace pour les retries immédiats sur un même transcript. Sans garantie de durée de cache côté serveur. Acceptable pour le cas d'usage MVP.
