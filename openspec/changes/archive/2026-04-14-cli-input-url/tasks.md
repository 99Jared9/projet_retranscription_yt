## 1. Initialisation du projet

- [x] 1.1 Créer `pyproject.toml` avec les métadonnées du package, les dépendances (`typer`, `rich`) et le script `yt-rapport = "yt_rapport.main:app"`
- [x] 1.2 Créer la structure de dossiers `src/yt_rapport/` et le fichier `src/yt_rapport/__init__.py`

## 2. Point d'entrée CLI

- [x] 2.1 Créer `src/yt_rapport/main.py` avec l'app Typer et la commande principale acceptant `url: str` en argument positionnel
- [x] 2.2 Implémenter la validation de l'URL YouTube (regex `youtube.com/watch` ou `youtu.be/`) avec sortie en erreur si invalide
- [x] 2.3 Afficher la progression du pipeline via `rich` (début, fin, erreurs)
- [x] 2.4 Ajouter l'orchestration séquentielle des modules pipeline avec stubs (`NotImplementedError`) pour les modules non-encore-implémentés

## 3. Vérification

- [x] 3.1 Installer le package en mode éditable (`uv pip install -e .`) et vérifier que `yt-rapport --help` fonctionne
- [x] 3.2 Tester `yt-rapport https://www.youtube.com/watch?v=dQw4w9WgXcQ` et vérifier la progression affichée
- [x] 3.3 Tester `yt-rapport https://example.com` et vérifier le message d'erreur URL invalide
- [x] 3.4 Tester `yt-rapport` sans argument et vérifier l'affichage de l'aide
