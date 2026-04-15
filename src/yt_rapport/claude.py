from __future__ import annotations

import json
import os
from dataclasses import dataclass

import openai

from yt_rapport.transcript import TranscriptResult


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ClaudeError(Exception):
    """Erreur de base pour l'analyse DeepSeek."""


class ClaudeAuthError(ClaudeError):
    """Clé API invalide ou absente."""


class ClaudeRateLimitError(ClaudeError):
    """Limite de taux atteinte."""


class ClaudeAnalysisError(ClaudeError):
    """Réponse inattendue ou non parseable."""


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------


@dataclass
class KeyPoint:
    text: str
    timestamp_seconds: int
    timestamp_label: str


@dataclass
class AnalysisResult:
    summary: str
    key_points: list[KeyPoint]
    video_url: str


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
Tu es un assistant spécialisé dans l'analyse de contenu vidéo.
Tu reçois un transcript YouTube avec des timestamps et tu dois produire un résumé structuré en français.

Tu DOIS répondre UNIQUEMENT avec un objet JSON valide, sans texte supplémentaire avant ou après.
Structure JSON attendue :

{
  "summary": "Résumé introductif de 2 à 4 phrases en français.",
  "key_points": [
    {
      "text": "Description du point clé en français.",
      "timestamp_seconds": 42,
      "timestamp_label": "0m42s"
    }
  ]
}

Règles :
- summary : 2 à 4 phrases résumant l'essentiel de la vidéo
- key_points : entre 5 et 8 points clés représentant les moments les plus importants
- timestamp_seconds : entier, position en secondes dans la vidéo (≥ 0)
- timestamp_label : format "Xm Ys" (ex. "1m23s", "0m05s")
- Tout le contenu (summary et text) doit être rédigé en français
- Aucun texte en dehors du JSON
"""


# ---------------------------------------------------------------------------
# Formatage du transcript
# ---------------------------------------------------------------------------


def _format_transcript(transcript: TranscriptResult) -> str:
    """Convertit les entrées du transcript en texte brut avec timestamps."""
    lines = []
    for entry in transcript.entries:
        seconds = int(entry["start"])
        minutes, secs = divmod(seconds, 60)
        label = f"{minutes}m{secs:02d}s"
        lines.append(f"[{label}] {entry['text']}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Parsing de la réponse
# ---------------------------------------------------------------------------


def _parse_response(raw: str) -> tuple[str, list[KeyPoint]]:
    """Parse le JSON retourné par DeepSeek. Lève ClaudeAnalysisError si invalide."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ClaudeAnalysisError(
            f"Réponse non-JSON reçue de l'API.\nContenu brut :\n{raw}"
        ) from exc

    try:
        summary = str(data["summary"])
        key_points = [
            KeyPoint(
                text=str(kp["text"]),
                timestamp_seconds=int(kp["timestamp_seconds"]),
                timestamp_label=str(kp["timestamp_label"]),
            )
            for kp in data["key_points"]
        ]
    except (KeyError, TypeError, ValueError) as exc:
        raise ClaudeAnalysisError(
            f"Structure JSON inattendue : {exc}\nContenu brut :\n{raw}"
        ) from exc

    return summary, key_points


# ---------------------------------------------------------------------------
# API publique
# ---------------------------------------------------------------------------


def analyse_transcript(transcript: TranscriptResult, video_url: str) -> AnalysisResult:
    """Analyse un transcript YouTube via DeepSeek et retourne résumé + points clés.

    Raises:
        ClaudeAuthError: si DEEPSEEK_API_KEY est absent ou invalide.
        ClaudeRateLimitError: si la limite de taux est atteinte.
        ClaudeAnalysisError: si la réponse ne peut pas être parsée.
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ClaudeAuthError(
            "Variable d'environnement DEEPSEEK_API_KEY absente ou vide."
        )

    client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # Le transcript est placé en premier dans le message utilisateur pour
    # maximiser le prefix caching automatique de DeepSeek.
    transcript_text = _format_transcript(transcript)
    user_message = (
        f"Voici le transcript de la vidéo :\n\n{transcript_text}\n\n"
        "Analyse ce transcript et retourne le JSON demandé."
    )

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            response_format={"type": "json_object"},
        )
    except openai.AuthenticationError as exc:
        raise ClaudeAuthError(f"Clé API DeepSeek invalide : {exc}") from exc
    except openai.RateLimitError as exc:
        raise ClaudeRateLimitError(f"Limite de taux DeepSeek atteinte : {exc}") from exc
    except openai.OpenAIError as exc:
        raise ClaudeAnalysisError(f"Erreur API DeepSeek : {exc}") from exc

    raw = response.choices[0].message.content or ""
    summary, key_points = _parse_response(raw)

    return AnalysisResult(summary=summary, key_points=key_points, video_url=video_url)
