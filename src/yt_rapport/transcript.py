from __future__ import annotations

import re
from dataclasses import dataclass

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)

_api = YouTubeTranscriptApi()


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class TranscriptError(Exception):
    """Erreur de base pour la récupération des sous-titres."""


class NoTranscriptAvailable(TranscriptError):
    """La vidéo existe mais n'a pas de sous-titres disponibles."""


class VideoNotFound(TranscriptError):
    """L'URL ne contient pas de video_id valide ou la vidéo n'existe pas."""


class VideoPrivate(TranscriptError):
    """La vidéo est privée ou inaccessible."""


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------


@dataclass
class TranscriptResult:
    entries: list[dict]        # [{text: str, start: float, duration: float}, ...]
    video_id: str
    language: str
    chapters: list[dict] | None


# ---------------------------------------------------------------------------
# Extraction du video_id
# ---------------------------------------------------------------------------

_VIDEO_ID_RE = re.compile(
    r"(?:youtube\.com/watch\?(?:[^&]*&)*v=|youtu\.be/)([A-Za-z0-9_-]{11})"
)


def _extract_video_id(url: str) -> str:
    match = _VIDEO_ID_RE.search(url)
    if not match:
        raise VideoNotFound(f"Impossible d'extraire un video_id depuis l'URL : {url}")
    return match.group(1)


# ---------------------------------------------------------------------------
# Récupération des sous-titres
# ---------------------------------------------------------------------------

_PREFERRED_LANGS = ("fr", "en")


def _to_entry(snippet: object) -> dict:
    """Convertit un FetchedTranscriptSnippet en dict uniforme."""
    return {"text": snippet.text, "start": snippet.start, "duration": snippet.duration}  # type: ignore[attr-defined]


def _fetch_entries_and_lang(video_id: str) -> tuple[list[dict], str]:
    """Retourne (entries, language_code). Priorité : fr → en → première langue dispo."""
    try:
        transcript_list = _api.list(video_id)
    except VideoUnavailable as exc:
        raise VideoPrivate(f"La vidéo {video_id} est privée ou introuvable.") from exc
    except TranscriptsDisabled as exc:
        raise NoTranscriptAvailable(
            f"Les sous-titres sont désactivés pour la vidéo {video_id}."
        ) from exc
    except Exception as exc:
        raise TranscriptError(f"Erreur lors du listage des sous-titres : {exc}") from exc

    # Tenter fr puis en
    for lang in _PREFERRED_LANGS:
        try:
            transcript = transcript_list.find_transcript([lang])
            entries = [_to_entry(e) for e in transcript.fetch()]
            return entries, transcript.language_code
        except NoTranscriptFound:
            continue

    # Fallback : première langue disponible
    try:
        transcript = next(iter(transcript_list))
        entries = [_to_entry(e) for e in transcript.fetch()]
        return entries, transcript.language_code
    except StopIteration:
        raise NoTranscriptAvailable(
            f"Aucun sous-titre disponible pour la vidéo {video_id}."
        )


# ---------------------------------------------------------------------------
# API publique
# ---------------------------------------------------------------------------


def get_transcript(url: str) -> TranscriptResult:
    """Extrait les sous-titres YouTube et retourne un TranscriptResult.

    Raises:
        VideoNotFound: si l'URL ne contient pas de video_id reconnaissable.
        VideoPrivate: si la vidéo est privée ou supprimée.
        NoTranscriptAvailable: si la vidéo n'a pas de sous-titres.
        TranscriptError: pour toute autre erreur de récupération.
    """
    video_id = _extract_video_id(url)
    entries, language = _fetch_entries_and_lang(video_id)

    return TranscriptResult(
        entries=entries,
        video_id=video_id,
        language=language,
        chapters=None,  # youtube-transcript-api n'expose pas les chapitres
    )
