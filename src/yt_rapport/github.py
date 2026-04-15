import base64
import os

import httpx


class GitHubAuthError(Exception):
    pass


class GitHubRepoError(Exception):
    pass


class GitHubConflictError(Exception):
    pass


def push_file(filename: str, content: str) -> str:
    """Envoie le fichier vers GitHub via PUT /repos/{owner}/{repo}/contents/{filename}.

    Retourne l'URL HTML du fichier créé.
    """
    token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPO"]

    encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
    stem = filename.removesuffix(".md")
    commit_message = f"feat: {stem}"

    response = httpx.put(
        f"https://api.github.com/repos/{repo}/contents/{filename}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={"message": commit_message, "content": encoded},
    )

    if response.status_code == 401:
        raise GitHubAuthError(
            "Token GitHub invalide ou expiré. Vérifiez la variable GITHUB_TOKEN."
        )
    if response.status_code in (403, 404):
        raise GitHubRepoError(
            f"Repo '{repo}' introuvable ou accès refusé. "
            "Vérifiez GITHUB_REPO et les permissions du token."
        )
    if response.status_code == 422:
        raise GitHubConflictError(
            f"Le fichier '{filename}' existe déjà dans le repo '{repo}'."
        )

    response.raise_for_status()
    return response.json()["content"]["html_url"]
