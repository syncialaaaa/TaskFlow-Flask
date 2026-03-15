# TaskFlow (Flask To-Do) - Local

Application Flask de gestion de listes et de taches, avec authentification utilisateur.

## Prerequis

- Python 3.13+

## Installation locale

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Variables d'environnement (local)

Exemple rapide:

```powershell
$env:SECRET_KEY = "change-me-with-a-long-random-value"
$env:DATABASE_URL = "sqlite:///task_manager.db"
$env:SESSION_COOKIE_SECURE = "0"
$env:FLASK_DEBUG = "1"
```

Un modele est fourni dans `.env.example`.

## Base de donnees locale

Avant le premier lancement:

```powershell
$env:FLASK_APP = "todolist.py"
.\.venv\Scripts\python.exe -m flask db upgrade
```

## Lancer l'application

```powershell
.\.venv\Scripts\python.exe todolist.py
```

Application disponible sur `http://127.0.0.1:3000`.

## Migrations

Creer une migration apres modification des modeles:

```powershell
$env:FLASK_APP = "todolist.py"
.\.venv\Scripts\python.exe -m flask db migrate -m "description"
.\.venv\Scripts\python.exe -m flask db upgrade
```
