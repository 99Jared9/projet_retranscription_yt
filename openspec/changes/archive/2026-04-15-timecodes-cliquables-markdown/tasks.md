## 1. Création du module markdown.py

- [x] 1.1 Créer `src/yt_rapport/markdown.py` avec la fonction `generate_filename(title) -> str` qui retourne `YYYY-MM-DD-{slug}.md`
- [x] 1.2 Implémenter la slugification dans `generate_filename` : lowercase, suppression des accents via `unicodedata`, remplacement des caractères non-alphanumériques par `-`, fallback sur `"video"` si slug vide
- [x] 1.3 Implémenter la fonction helper `seconds_to_hms(seconds: int) -> str` qui retourne `"HH:MM:SS"`
- [x] 1.4 Implémenter `generate_markdown(video_id, title, summary, key_points) -> str` qui assemble le contenu `.md` : titre H1, résumé intro, liste des points clés avec timecodes cliquables

## 2. Format des timecodes

- [x] 2.1 Chaque point clé génère un lien au format `[HH:MM:SS](https://www.youtube.com/watch?v={video_id}&t={timestamp_seconds}s)`
- [x] 2.2 Vérifier que le cas `timestamp_seconds = 0` génère un lien valide `[00:00:00](...&t=0s)`

## 3. Intégration dans main.py

- [x] 3.1 Importer `generate_markdown` et `generate_filename` depuis `markdown.py` dans `main.py`
- [x] 3.2 Appeler `generate_markdown` après `claude.py` et passer le résultat à `github.py`
- [x] 3.3 Passer `generate_filename(title)` comme nom de fichier cible à `github.py`

## 4. Vérification manuelle

- [ ] 4.1 Tester avec une URL YouTube réelle et vérifier que le `.md` généré contient des liens cliquables fonctionnels
- [ ] 4.2 Vérifier que le nom de fichier généré respecte le format `YYYY-MM-DD-titre.md`
