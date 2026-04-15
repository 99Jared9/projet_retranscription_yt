# yt-rapport

CLI Python qui prend une URL YouTube, extrait les sous-titres, les analyse via DeepSeek, et pousse un rapport `.md` structuré dans un repo GitHub.

```
yt-rapport "https://www.youtube.com/watch?v=..."
```

## Ce que ça fait

1. Extrait les sous-titres de la vidéo via `youtube-transcript-api`
2. Envoie le transcript à DeepSeek qui génère un résumé + 5-8 points clés en français
3. Produit un fichier `YYYY-MM-DD-titre.md` avec des timecodes cliquables (`?t=Xs`)
4. Pousse le fichier directement dans un repo GitHub via l'API REST

## Installation

Prérequis : Python 3.12+ et [uv](https://github.com/astral-sh/uv)

```bash
git clone https://github.com/99Jared9/projet_retranscription_yt.git
cd projet_retranscription_yt
uv pip install -e .
```

## Configuration

Crée un fichier `.env` à la racine :

```
DEEPSEEK_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
GITHUB_REPO=tonpseudo/ma-veille
```

- `DEEPSEEK_API_KEY` — clé API DeepSeek ([platform.deepseek.com](https://platform.deepseek.com))
- `GITHUB_TOKEN` — Personal Access Token GitHub avec la permission `repo`
- `GITHUB_REPO` — repo cible au format `owner/repo`

## Utilisation

```bash
yt-rapport "https://www.youtube.com/watch?v=..."
```

Le terminal affiche la progression et l'URL GitHub du fichier créé à la fin.

## Stack

| Rôle | Outil |
|---|---|
| CLI | Typer |
| Transcripts | youtube-transcript-api |
| Analyse IA | DeepSeek API (`deepseek-chat`) |
| Push GitHub | GitHub REST API + httpx |
| Affichage terminal | rich |
| Packaging | uv |
