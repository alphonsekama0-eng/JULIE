# Recensement des catholiques de l'UAM

Petite application web locale (formulaire + base de données) pour enregistrer les catholiques de l'UAM et afficher la liste après chaque inscription.

## Prérequis

- Python 3.10+ (recommandé)

## Installation

Dans ce dossier, ouvre un terminal et exécute :

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer l'application

```bash
python app.py
```

Puis ouvre dans ton navigateur :

- `http://127.0.0.1:5000/` (formulaire)
- `http://127.0.0.1:5000/liste` (liste)

## Démarrage en 1 clic (recommandé)

Double-clique sur `start.bat` puis ouvre (si ça ne s’ouvre pas tout seul) :

- `http://127.0.0.1:5000/`

## Ouvrir depuis un téléphone / autre PC (même Wi‑Fi)

1) Lance le serveur en mode réseau :

```bash
set FLASK_HOST=0.0.0.0
python app.py
```

2) Sur le PC qui héberge, récupère ton IP (ex: `192.168.1.10`) puis sur le téléphone ouvre :

- `http://TON_IP:5000/`

## Mot de passe gérant (protection de la liste)

- La page ` /liste ` demande une connexion gérant.
- Mot de passe par défaut : **`uam123`**
- Pour le changer (recommandé), avant de lancer :

```bash
set MANAGER_PASSWORD=TON_MOT_DE_PASSE
python app.py
```

## Données

- En local (sans `DATABASE_URL`), la base est un fichier : `data/recensement.sqlite3`.

## Lien public (Render)

Tu peux obtenir un lien public du style `https://recensement-uam.onrender.com`.

### Étapes rapides

1. Crée un compte GitHub (si tu n’en as pas).
2. Mets ce projet dans un dépôt GitHub.
3. Crée un compte sur [Render](https://render.com/) et connecte ton GitHub.
4. Clique sur **New +** -> **Blueprint** et sélectionne le dépôt.
5. Render lit automatiquement `render.yaml`.
6. Dans les variables d’environnement Render, définis `MANAGER_PASSWORD` (obligatoire).
7. Déploie : tu recevras ton lien public.

### Important

- En version gratuite, l’app peut se mettre en veille (premier chargement un peu lent).
- Avec la version PostgreSQL, les inscriptions sont persistantes dans la base.

