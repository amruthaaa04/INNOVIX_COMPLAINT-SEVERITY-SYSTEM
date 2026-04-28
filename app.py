from flask import Flask, render_template, request

app = Flask(__name__)

import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_text TEXT,
            sentiment REAL,
            severity TEXT,
            priority REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    complaint_text = request.form["complaint"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (complaint_text)
        VALUES (?)
    """, (complaint_text,))

    conn.commit()
    conn.close()

    return "Complaint submitted successfully!"


@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True) 
 
