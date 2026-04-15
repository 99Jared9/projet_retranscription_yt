# Roadmap — Outil de rapport YouTube

## MVP — ça marche, c'est tout

- **Input URL en ligne de commande** — on passe le lien en argument, pas d'interface
- **Récupération des sous-titres YT** — via youtube-transcript-api · erreur propre si pas de CC
- **Analyse DeepSeek + points clés** — prompt simple · 5-8 points · résumé intro · toujours en français
- **Timecodes cliquables dans le .md** — format `?t=Xs` dans l'URL · liens directs vers la vidéo
- **Push GitHub automatique** — fichier `YYYY-MM-DD-titre.md` · commit + push repo ma-veille

---

## V1 — confort d'utilisation

- **Chapitres YT comme guide d'analyse** — si présents, Claude les utilise pour mieux structurer temporellement
- **Gestion des vidéos très longues** — chunking du transcript · synthèse finale cohérente
- **Lien GitHub renvoyé dans le terminal** — URL directe vers le fichier créé, copiable en 1 clic
- **Gestion des erreurs robuste** — vidéo privée, URL invalide, rate limit API · messages clairs

---

## V2 — puissance

- **Tags sémantiques par point clé** — concept · exemple · outil · alerte · citation
- **Batch de liens** — passer une liste de URLs, générer N rapports d'un coup
- **Export Notion / Obsidian** — intégration PKM via API ou format compatible

---

## Hors-périmètre

- **Mémoire cross-vidéos** — décidé ensemble · trop complexe pour la valeur apportée
- **Interface graphique** — Claude Code = CLI · pas besoin d'UI
- **Fallback Whisper (audio brut)** — hors scope · sous-titres YT suffisent pour le cas d'usage
- **GitHub Pages avec index visuel** — repo simple .md suffit · overhead HTML inutile