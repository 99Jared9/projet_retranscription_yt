## Context

Le pipeline CLI produit actuellement des sous-titres (`transcript.py`) et une analyse DeepSeek (`claude.py`). Il manque le maillon de rendu : transformer la réponse structurée de DeepSeek en fichier `.md` prêt à être poussé sur GitHub.

La réponse DeepSeek contient des points clés avec leurs timestamps en secondes. Ces secondes doivent être converties en liens cliquables `?t=Xs` pointant vers la vidéo YouTube source.

## Goals / Non-Goals

**Goals:**
- Générer un fichier `.md` avec résumé intro + 5-8 points clés
- Chaque point clé contient un lien cliquable `[HH:MM:SS](URL?t=Xs)` vers le moment précis dans la vidéo
- Nom de fichier au format `YYYY-MM-DD-titre.md` (titre = titre de la vidéo, slugifié)
- Module pur : entrée = données structurées + video_id, sortie = contenu `.md` en string

**Non-Goals:**
- Chapitres YT comme guide (V1, hors scope MVP)
- Chunking des vidéos longues (V1)
- Tags sémantiques par point clé (V2)
- Écriture sur disque — `markdown.py` retourne une string, `github.py` s'occupe du push

## Decisions

### Séparation rendu / écriture
`markdown.py` ne touche pas au disque — il retourne le contenu `.md` sous forme de string. `github.py` se charge de l'envoi. Cela simplifie les tests et respecte la séparation des responsabilités déjà établie dans l'architecture.

### Format des timecodes : `?t=Xs` (secondes entières)
Alternatif considéré : `?t=HHhMMmSSs` (format long YouTube). Rejeté — `?t=Xs` est plus court et fonctionne identiquement. Le timestamp affiché au lecteur reste `[HH:MM:SS]` pour la lisibilité humaine.

### Slugification du titre pour le nom de fichier
Algorithme simple : lowercase, remplacement des espaces et caractères spéciaux par `-`, suppression des accents. Pas de dépendance externe — `unicodedata` + regex suffisent.

### Date dans le nom de fichier
`datetime.date.today()` au moment de la génération. Pas de date extraite de la vidéo — trop complexe pour le MVP.

## Risks / Trade-offs

- [Titre vidéo avec caractères exotiques] → Mitigation : slugification défensive avec fallback sur `video-{video_id}` si le slug résultant est vide
- [Timestamps DeepSeek imprécis] → Pas de mitigation au niveau du rendu — c'est la responsabilité du prompt dans `claude.py`
- [Contenu `.md` non valide si réponse DeepSeek malformée] → `markdown.py` fait confiance à la structure retournée par `claude.py` ; la gestion d'erreur reste dans `main.py`
