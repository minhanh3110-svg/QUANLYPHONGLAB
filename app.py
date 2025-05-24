from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret"

def get_db_connection():
    conn = sqlite3.connect("lab_app.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html", log=None, staff=session.get("username", ""))

@app.route("/chart")
def chart():
    return render_template("chart.html", labels=[], datasets=[])

@app.route("/weekly_stats")
def weekly_stats():
    return render_template("weekly_stats.html", stats=[])

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", total_clusters=0, total_hours=0, avg_productivity=0, top_staff=[])from functools import wraps

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'username' not in session or session.get('role') not in roles:
                return redirect('/login')
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        conn.close()
        if user:
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect("/")
        else:
            error = "Sai tên đăng nhập hoặc mật khẩu"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")