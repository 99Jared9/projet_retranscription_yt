from __future__ import annotations

import re
import unicodedata
from datetime import date

from yt_rapport.claude import AnalysisResult, KeyPoint


def seconds_to_hms(seconds: int) -> str:
    """Convertit un nombre de secondes en chaîne HH:MM:SS."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def generate_filename(title: str) -> str:
    """Retourne un nom de fichier au format YYYY-MM-DD-{slug}.md."""
    today = date.today().strftime("%Y-%m-%d")
    normalized = unicodedata.normalize("NFD", title)
    ascii_title = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")
    if not slug:
        slug = "video"
    return f"{today}-{slug}.md"


def generate_markdown(
    video_id: str,
    title: str,
    summary: str,
    key_points: list[KeyPoint],
) -> str:
    """Génère le contenu d'un fichier .md structuré avec timecodes cliquables."""
    lines: list[str] = [f"# {title}", "", summary, ""]

    if key_points:
        lines.append("## Points clés")
        lines.append("")
        for kp in key_points:
            hms = seconds_to_hms(kp.timestamp_seconds)
            url = f"https://www.youtube.com/watch?v={video_id}&t={kp.timestamp_seconds}s"
            lines.append(f"- [{hms}]({url}) {kp.text}")
        lines.append("")

    return "\n".join(lines)
