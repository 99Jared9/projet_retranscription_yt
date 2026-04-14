import re
import sys

import typer
from rich.console import Console

app = typer.Typer(help="Extrait et analyse le contenu d'une vidéo YouTube, puis pousse un rapport vers GitHub.")
console = Console()

_YT_URL_RE = re.compile(r"(youtube\.com/watch|youtu\.be/)")


def _validate_url(url: str) -> None:
    if not _YT_URL_RE.search(url):
        console.print(f"[red]Erreur :[/red] URL YouTube invalide : {url}")
        console.print("Format attendu : https://www.youtube.com/watch?v=... ou https://youtu.be/...")
        raise typer.Exit(code=1)


@app.command()
def rapport(url: str = typer.Argument(..., help="URL de la vidéo YouTube à analyser")):
    """Génère un rapport Markdown à partir d'une vidéo YouTube et le pousse sur GitHub."""
    _validate_url(url)

    console.print(f"[bold]Traitement de :[/bold] {url}")

    try:
        console.print("  [dim]1/4[/dim] Récupération des sous-titres...")
        transcript = _get_transcript(url)

        console.print("  [dim]2/4[/dim] Analyse via Claude...")
        analysis = _analyze(transcript)

        console.print("  [dim]3/4[/dim] Génération du Markdown...")
        markdown = _build_markdown(url, analysis)

        console.print("  [dim]4/4[/dim] Push vers GitHub...")
        github_url = _push_to_github(markdown)
    except Exception as exc:
        console.print(f"[red]Erreur :[/red] {exc}")
        raise typer.Exit(code=1)

    console.print(f"\n[green]Rapport publié :[/green] {github_url}")


def _get_transcript(url: str) -> str:
    raise NotImplementedError("transcript.py non encore implémenté")


def _analyze(transcript: str) -> dict:
    raise NotImplementedError("claude.py non encore implémenté")


def _build_markdown(url: str, analysis: dict) -> str:
    raise NotImplementedError("markdown.py non encore implémenté")


def _push_to_github(markdown: str) -> str:
    raise NotImplementedError("github.py non encore implémenté")
