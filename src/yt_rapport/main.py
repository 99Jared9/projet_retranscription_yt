import typer
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

from yt_rapport.claude import (
    AnalysisResult,
    ClaudeError,
    analyse_transcript,
)
from yt_rapport.transcript import (
    NoTranscriptAvailable,
    TranscriptError,
    TranscriptResult,
    VideoNotFound,
    VideoPrivate,
    get_transcript,
)

app = typer.Typer(help="Extrait et analyse le contenu d'une vidéo YouTube, puis pousse un rapport vers GitHub.")
console = Console()


@app.command()
def rapport(url: str = typer.Argument(..., help="URL de la vidéo YouTube à analyser")):
    """Génère un rapport Markdown à partir d'une vidéo YouTube et le pousse sur GitHub."""
    console.print(f"[bold]Traitement de :[/bold] {url}")

    try:
        console.print("  [dim]1/4[/dim] Récupération des sous-titres...")
        transcript = _get_transcript(url)

        console.print("  [dim]2/4[/dim] Analyse en cours...")
        analysis = _analyze(transcript, url)

        console.print("  [dim]3/4[/dim] Génération du Markdown...")
        markdown = _build_markdown(url, analysis)

        console.print("  [dim]4/4[/dim] Push vers GitHub...")
        github_url = _push_to_github(markdown)
    except (VideoNotFound, VideoPrivate, NoTranscriptAvailable, TranscriptError) as exc:
        console.print(f"[red]Erreur :[/red] {exc}")
        raise typer.Exit(code=1)
    except ClaudeError as exc:
        console.print(f"[red]Erreur d'analyse :[/red] {exc}")
        raise typer.Exit(code=1)
    except Exception as exc:
        console.print(f"[red]Erreur inattendue :[/red] {exc}")
        raise typer.Exit(code=1)

    console.print(f"\n[green]Rapport publié :[/green] {github_url}")


def _get_transcript(url: str) -> TranscriptResult:
    return get_transcript(url)


def _analyze(transcript: TranscriptResult, url: str) -> AnalysisResult:
    return analyse_transcript(transcript, url)


def _build_markdown(url: str, analysis: dict) -> str:
    raise NotImplementedError("markdown.py non encore implémenté")


def _push_to_github(markdown: str) -> str:
    raise NotImplementedError("github.py non encore implémenté")
