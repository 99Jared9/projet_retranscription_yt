# Architecture — Outil de rapport YouTube

## Stack technique

| Rôle | Choix |
|---|---|
| Langage | Python 3.12+ |
| Packaging | uv (`pyproject.toml` + `uv.lock`) |
| CLI | Typer |
| Transcripts YouTube | youtube-transcript-api |
| Analyse IA | DeepSeek API (`deepseek-chat`) |
| Push GitHub | GitHub REST API (`httpx` + `GITHUB_TOKEN`) |
| Affichage terminal | rich |

---

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

---

## Responsabilités des modules

### `main.py`
Point d'entrée CLI via Typer. Reçoit l'URL en argument, orchestre l'appel des modules dans l'ordre, affiche le lien GitHub final via `rich`.

### `transcript.py`
Appelle `youtube-transcript-api` pour extraire les sous-titres et les chapitres YT si présents. Retourne le transcript brut avec timestamps et la liste des chapitres (ou `None`).

### `claude.py`
Construit le prompt à partir du transcript et des chapitres, appelle l'API DeepSeek avec `deepseek-chat`, retourne les points clés structurés avec timestamps. Utilise le context caching pour les transcripts longs.

### `markdown.py`
Transforme la réponse Claude en fichier `.md` :
- Nom de fichier : `YYYY-MM-DD-titre.md`
- Timecodes au format `?t=Xs` dans les URLs YouTube
- Résumé intro + points clés (5-8)

### `github.py`
Appelle l'endpoint `PUT /repos/{owner}/{repo}/contents/{path}` de l'API GitHub REST via `httpx` pour créer le fichier directement dans le repo `ma-veille`. Pas de clone local — le contenu est envoyé encodé en base64. Retourne l'URL HTML du fichier créé.

---

## Flux d'exécution

```
URL YouTube
    │
    ▼
transcript.py ──► sous-titres + chapitres
    │
    ▼
claude.py ──► points clés + résumé (fr)
    │
    ▼
markdown.py ──► fichier YYYY-MM-DD-titre.md
    │
    ▼
github.py ──► commit + push → URL du fichier
    │
    ▼
Terminal (rich) ──► lien cliquable
```

---

## Décisions de conception

**Context caching activé dès le MVP** — les transcripts longs sont coûteux en tokens ; le context caching DeepSeek réduit la latence et le coût sur les appels répétés (ex. retry après erreur).

**GitHub REST API plutôt que git CLI** — `PUT /contents/{path}` crée un fichier directement sans cloner le repo localement. Aucune dépendance sur git installé, aucune config SSH/HTTPS à gérer. Le `GITHUB_TOKEN` suffit, comme le MCP GitHub.

**Typer plutôt qu'argparse** — type hints Python suffisent à définir l'interface CLI ; pas de code de parsing à écrire. Extensible au batch (V2) sans refonte.

**Pas de LangChain** — aucune valeur ajoutée pour un pipeline linéaire sans mémoire cross-vidéos (hors périmètre). L'API DeepSeek directement donne un contrôle total sur le prompt.

---

## Configuration requise (variables d'environnement)

```
DEEPSEEK_API_KEY    # clé API DeepSeek
GITHUB_TOKEN        # token GitHub (scope repo)
GITHUB_REPO         # repo cible au format owner/repo (ex. monpseudo/ma-veille)
```
