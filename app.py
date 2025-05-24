from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from datetime import datetime
from functools import wraps
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = 'abc123'
DB_NAME = 'lab_app.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def require_login():
    allowed_routes = ['login', 'static']
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()
        if user:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Sai tên đăng nhập hoặc mật khẩu.")
    return render_template("login.html")

@app.route("/")
def index():
    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM log_entries ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("index.html", logs=logs)

@app.route("/dashboard")
def dashboard():
    # Placeholder stats
    total_clusters = 0
    total_hours = 0
    avg_productivity = 0
    top_staff = []
    return render_template("dashboard.html", total_clusters=total_clusters,
                           total_hours=total_hours,
                           avg_productivity=avg_productivity,
                           top_staff=top_staff)

if __name__ == "__main__":
    app.run(debug=True)
