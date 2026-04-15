## Requirements

### Requirement: Génération du fichier markdown structuré
Le module `markdown.py` SHALL exposer une fonction `generate_markdown(video_id, title, summary, key_points)` qui retourne le contenu complet d'un fichier `.md` en string, sans écriture sur disque.

#### Scenario: Génération avec points clés et timecodes
- **WHEN** `generate_markdown` est appelé avec un `video_id`, un `title`, un `summary` et une liste de `key_points` (chacun avec `text` et `timestamp_seconds`)
- **THEN** la string retournée contient le résumé en tête, suivi de chaque point clé avec un lien cliquable au format `[HH:MM:SS](https://www.youtube.com/watch?v={video_id}&t={timestamp_seconds}s)`

#### Scenario: Liste de points clés vide
- **WHEN** `generate_markdown` est appelé avec une liste `key_points` vide
- **THEN** la fonction retourne quand même un `.md` valide avec uniquement le résumé

### Requirement: Convention de nommage du fichier de sortie
Le module SHALL exposer une fonction `generate_filename(title)` qui retourne un nom de fichier au format `YYYY-MM-DD-{slug}.md`, où `{slug}` est le titre slugifié (lowercase, accents supprimés, espaces et caractères non-alphanumériques remplacés par `-`).

#### Scenario: Titre normal
- **WHEN** `generate_filename("DeepSeek : la révolution IA")` est appelé
- **THEN** la fonction retourne `"2026-04-15-deepseek-la-revolution-ia.md"` (date du jour réelle)

#### Scenario: Titre vide ou slug vide après nettoyage
- **WHEN** le titre ne contient que des caractères non-slugifiables
- **THEN** la fonction retourne `"YYYY-MM-DD-video.md"` comme fallback

### Requirement: Format des timecodes cliquables
Chaque timecode dans le `.md` SHALL utiliser le format `?t=Xs` (secondes entières) dans l'URL et afficher `[HH:MM:SS]` comme texte du lien pour la lisibilité humaine.

#### Scenario: Conversion secondes → affichage HH:MM:SS
- **WHEN** un point clé a `timestamp_seconds = 3725`
- **THEN** le lien généré est `[01:02:05](https://www.youtube.com/watch?v={video_id}&t=3725s)`

#### Scenario: Timestamp inférieur à une heure
- **WHEN** un point clé a `timestamp_seconds = 90`
- **THEN** le lien généré est `[00:01:30](https://www.youtube.com/watch?v={video_id}&t=90s)`
