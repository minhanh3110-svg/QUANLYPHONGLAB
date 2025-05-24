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
        ngay = request.form["ngay"]
        soluong = request.form["soluong"]
        user = session.get("username", "unknown")

        conn = get_db_connection()
        conn.execute("INSERT INTO log_entries (phong, ngay, soluong, username) VALUES (?, ?, ?, ?)",
                     ("phong_caymo", ngay, soluong, user))
        conn.commit()
        conn.close()
        flash("Đã lưu phòng cấy mô", "success")
        return redirect(url_for("phong_caymo"))

    return render_template("form_phong_caymo.html")
# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Sai tên đăng nhập hoặc mật khẩu'
    return render_template('login.html')

# Bắt buộc đăng nhập cho mọi route
@app.before_request
def require_login():
    allowed_routes = ['login', 'static']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))

# ===================== CÁC PHÒNG ========================

@app.route('/phong-caymo', methods=['GET', 'POST'])
def phong_caymo():
    if request.method == 'POST':
        ngay = request.form['ngay']
        noi_dung = request.form['noi_dung']
        nguoi_nhap = session['username']

        conn = get_db_connection()
        conn.execute("INSERT INTO caymo_logs (ngay, noi_dung, nguoi_nhap) VALUES (?, ?, ?)", (ngay, noi_dung, nguoi_nhap))
        conn.commit()
        conn.close()
        return redirect(url_for('phong_caymo'))
    return render_template('phong_caymo.html')

@app.route('/phong-sang', methods=['GET', 'POST'])
def phong_sang():
    if request.method == 'POST':
        ngay = request.form['ngay']
        noi_dung = request.form['noi_dung']
        nguoi_nhap = session['username']

        conn = get_db_connection()
        conn.execute("INSERT INTO phongsang_logs (ngay, noi_dung, nguoi_nhap) VALUES (?, ?, ?)", (ngay, noi_dung, nguoi_nhap))
        conn.commit()
        conn.close()
        return redirect(url_for('phong_sang'))
    return render_template('phong_sang.html')

@app.route('/phong-moi-truong', methods=['GET', 'POST'])
def phong_moitruong():
    if request.method == 'POST':
        ngay = request.form['ngay']
        noi_dung = request.form['noi_dung']
        nguoi_nhap = session['username']

        conn = get_db_connection()
        conn.execute("INSERT INTO moitruong_logs (ngay, noi_dung, nguoi_nhap) VALUES (?, ?, ?)", (ngay, noi_dung, nguoi_nhap))
        conn.commit()
        conn.close()
        return redirect(url_for('phong_moitruong'))
    return render_template('phong_moitruong.html')

# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
