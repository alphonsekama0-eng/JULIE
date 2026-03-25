@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Creation de l'environnement Python...
  python -m venv .venv
)

call ".venv\Scripts\activate.bat"

echo Installation des dependances...
python -m pip install -r requirements.txt

echo.
echo Lancement du site...
start "" "http://127.0.0.1:5000/"
python app.py

