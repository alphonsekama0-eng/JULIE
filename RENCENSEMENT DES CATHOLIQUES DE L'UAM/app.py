from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import Flask, flash, redirect, render_template, request, session, url_for


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "recensement.sqlite3"


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")
MANAGER_PASSWORD = os.environ.get("MANAGER_PASSWORD", "uam123")


def get_db_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS catholiques (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              prenom TEXT NOT NULL,
              nom TEXT NOT NULL,
              age INTEGER,
              sexe TEXT,
              filiere TEXT,
              niveau TEXT,
              telephone TEXT,
              email TEXT,
              residence TEXT,
              paroisse TEXT,
              groupe TEXT,
              date_inscription TEXT NOT NULL
            );
            """
        )


def _to_int(value: str | None) -> int | None:
    if value is None:
        return None
    v = value.strip()
    if v == "":
        return None
    try:
        return int(v)
    except ValueError:
        return None


@dataclass(frozen=True)
class Inscription:
    prenom: str
    nom: str
    age: int | None
    sexe: str
    filiere: str
    niveau: str
    telephone: str
    email: str
    residence: str
    paroisse: str
    groupe: str


def parse_inscription(form: dict[str, Any]) -> Inscription:
    def s(key: str) -> str:
        return str(form.get(key, "")).strip()

    return Inscription(
        prenom=s("prenom"),
        nom=s("nom"),
        age=_to_int(s("age")),
        sexe=s("sexe"),
        filiere=s("filiere"),
        niveau=s("niveau"),
        telephone=s("telephone"),
        email=s("email"),
        residence=s("residence"),
        paroisse=s("paroisse"),
        groupe=s("groupe"),
    )


def validate(i: Inscription) -> list[str]:
    errors: list[str] = []
    if not i.prenom:
        errors.append("Le prénom est obligatoire.")
    if not i.nom:
        errors.append("Le nom est obligatoire.")
    if i.age is not None and (i.age < 0 or i.age > 120):
        errors.append("L'âge semble incorrect.")
    return errors


@app.get("/")
def index():
    init_db()
    return render_template("index.html")


@app.post("/inscrire")
def inscrire():
    init_db()
    inscription = parse_inscription(request.form)
    errors = validate(inscription)
    if errors:
        for e in errors:
            flash(e, "error")
        return render_template("index.html", form=request.form), 400

    now_iso = datetime.now().isoformat(timespec="seconds")
    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO catholiques (
              prenom, nom, age, sexe, filiere, niveau, telephone, email, residence,
              paroisse, groupe, date_inscription
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                inscription.prenom,
                inscription.nom,
                inscription.age,
                inscription.sexe,
                inscription.filiere,
                inscription.niveau,
                inscription.telephone,
                inscription.email,
                inscription.residence,
                inscription.paroisse,
                inscription.groupe,
                now_iso,
            ),
        )

    flash("Inscription enregistrée avec succès.", "success")
    return redirect(url_for("liste"))


@app.get("/liste")
def liste():
    if not session.get("manager_logged_in"):
        return redirect(url_for("login", next=url_for("liste")))
    init_db()
    with get_db_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, prenom, nom, age, sexe, filiere, niveau, telephone, email,
                   residence, paroisse, groupe, date_inscription
            FROM catholiques
            ORDER BY id DESC
            """
        ).fetchall()

    return render_template("liste.html", rows=rows)


@app.get("/login")
def login():
    next_url = request.args.get("next") or url_for("liste")
    return render_template("login.html", next_url=next_url)


@app.post("/login")
def login_post():
    next_url = request.form.get("next_url") or url_for("liste")
    password = str(request.form.get("password", ""))
    if password != MANAGER_PASSWORD:
        flash("Mot de passe incorrect.", "error")
        return render_template("login.html", next_url=next_url), 401

    session["manager_logged_in"] = True
    flash("Connexion gérant réussie.", "success")
    return redirect(next_url)


@app.post("/logout")
def logout():
    session.pop("manager_logged_in", None)
    flash("Déconnexion effectuée.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    # Pour un accès depuis un autre appareil (même Wi‑Fi), mets:
    # set FLASK_HOST=0.0.0.0
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host=host, port=port, debug=debug)

