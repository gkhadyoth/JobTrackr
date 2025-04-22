from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "job_applications.db"

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            url TEXT,
            username TEXT,
            password TEXT,
            pay TEXT,
            status TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect(DB)
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    conn.close()
    return render_template("index.html", jobs=jobs)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = [request.form[key] for key in ["title", "company", "url", "username", "password", "pay", "status", "notes"]]
        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO jobs (title, company, url, username, password, pay, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<int:job_id>", methods=["GET", "POST"])
def edit(job_id):
    conn = sqlite3.connect(DB)
    if request.method == "POST":
        data = [request.form[key] for key in ["title", "company", "url", "username", "password", "pay", "status", "notes"]]
        data.append(job_id)
        conn.execute("""
            UPDATE jobs SET title=?, company=?, url=?, username=?, password=?, pay=?, status=?, notes=? WHERE id=?
        """, data)
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    job = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    conn.close()
    return render_template("edit.html", job=job)
    
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
