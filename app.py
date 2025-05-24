from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecret"
DB_NAME = "lab_app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM log_entries ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("index.html", logs=logs)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        conn.close()
        if user:
            session["username"] = username
            session["role"] = user["role"]
            return redirect(url_for("index"))
        else:
            flash("Sai tên đăng nhập hoặc mật khẩu")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/chart")
def chart():
    return render_template("chart.html")

@app.route("/weekly_stats")
def weekly_stats():
    return render_template("weekly_stats.html")
    @app.route("/phong-caymo", methods=["GET", "POST"])
def phong_caymo():
    if request.method == "POST":
        # xử lý dữ liệu tại đây
        ten_mau = request.form.get("ten_mau")
        so_luong = request.form.get("so_luong")
        nguoi_nhap = session.get("username", "Ẩn danh")

        # Ví dụ: lưu vào database (bạn cần thay phần này bằng hàm lưu thực tế)
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO log_entries (phong, ten_mau, so_luong, nguoi_nhap) VALUES (?, ?, ?, ?)",
            ("phong_caymo", ten_mau, so_luong, nguoi_nhap)
        )
        conn.commit()
        conn.close()

        flash("Đã lưu thành công!", "success")
        return redirect(url_for("phong_caymo"))

    return render_template("form_phong_caymo.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
