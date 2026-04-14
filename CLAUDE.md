# CLAUDE.md — Outil de rapport YouTube

## Objectif

CLI Python qui prend une URL YouTube, extrait les sous-titres, les analyse via Claude, et pousse un rapport `.md` structuré dans un repo GitHub.

## Stack technique

| Rôle | Choix |
|---|---|
| Langage | Python 3.12+ |
| Packaging | uv (`pyproject.toml` + `uv.lock`) |
| CLI | Typer |
| Transcripts YouTube | youtube-transcript-api |
| Analyse IA | Anthropic SDK (`claude-sonnet-4-6`) |
| Push GitHub | GitHub REST API (`httpx` + `GITHUB_TOKEN`) |
| Affichage terminal | rich |

## Structure du projet

```
yt-rapport/
├── pyproject.toml
├── uv.lock
└── src/
    └── yt_rapport/
        ├── __init__.py
        ├── main.py         # entry point Typer — parsing args, orchestration
        ├── transcript.py   # récupération et nettoyage des sous-titres YT
        ├── claude.py       # appels Anthropic SDK, construction du prompt
        ├── markdown.py     # génération du .md avec timecodes cliquables
        └── github.py       # commit + push vers le repo ma-veille
```

## Variables d'environnement requises

```
ANTHROPIC_API_KEY   # clé API Anthropic
GITHUB_TOKEN        # token GitHub (scope repo)
GITHUB_REPO         # repo cible au format owner/repo (ex. monpseudo/ma-veille)
```

## Comportement attendu (MVP)

- Input : URL YouTube en argument CLI
- Extraction des sous-titres via `youtube-transcript-api` — erreur propre si pas de CC
- Analyse Claude : résumé intro + 5-8 points clés, **toujours en français**
- Timecodes cliquables au format `?t=Xs` dans le `.md`
- Push GitHub via `PUT /repos/{owner}/{repo}/contents/{path}` — pas de clone local
- Nom de fichier : `YYYY-MM-DD-titre.md`
- URL du fichier créé affichée dans le terminal via `rich`

## Décisions de conception à respecter

- **Prompt caching activé** — passer le transcript dans un bloc `cache_control` pour réduire coût et latence sur les retries
- **GitHub REST API** (pas git CLI) — `PUT /contents/{path}` + base64, aucune dépendance locale
- **Pas de LangChain** — SDK Anthropic directement, pipeline linéaire sans mémoire cross-vidéos
- **Typer** pour le CLI — extensible au batch (V2) sans refonte

## Périmètre MVP — ce qui est hors scope

- Chapitres YT comme guide d'analyse (V1)
- Chunking des vidéos très longues (V1)
- Tags sémantiques, batch de liens, export Notion/Obsidian (V2)
- Interface graphique, fallback Whisper, mémoire cross-vidéos (jamais)
