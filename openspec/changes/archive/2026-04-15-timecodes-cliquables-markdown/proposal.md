## Why

Le rapport `.md` généré doit permettre de naviguer directement vers les moments clés de la vidéo depuis le fichier. Sans timecodes cliquables, l'utilisateur doit chercher manuellement dans la vidéo — ce qui annule l'intérêt du résumé.

## What Changes

- Création du module `markdown.py` qui transforme la réponse DeepSeek en fichier `.md` structuré
- Chaque point clé inclut un lien cliquable vers la vidéo au format `[HH:MM:SS](https://youtube.com/watch?v=VIDEO_ID?t=Xs)`
- Le fichier généré suit la convention de nommage `YYYY-MM-DD-titre.md`
- Le résumé introductif est placé en tête de fichier, suivi des 5-8 points clés avec leurs timecodes

## Capabilities

### New Capabilities

- `markdown-generation`: Génération du fichier `.md` à partir de la réponse structurée DeepSeek — résumé intro + points clés avec timecodes cliquables au format `?t=Xs`

### Modified Capabilities

<!-- Aucune spec existante à modifier — premier module de rendu -->

## Impact

- Nouveau fichier `src/yt_rapport/markdown.py`
- Consomme la sortie de `claude.py` (points clés avec timestamps en secondes)
- Produit un fichier `.md` consommé par `github.py` pour le push
- Dépendance sur l'`video_id` extrait de l'URL YouTube (disponible dans `main.py`)
