from flask import Flask, render_template, request
from textblob import TextBlob
import sqlite3

app = Flask(__name__)

# Initialize Database
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

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Submit Complaint (WITH NLP + OUTPUT)
@app.route("/submit", methods=["POST"])
def submit():
    complaint_text = request.form["complaint"]

    # NLP Sentiment Analysis
    blob = TextBlob(complaint_text)
    sentiment = blob.sentiment.polarity  # -1 to +1

    print("Sentiment score:", sentiment)  # terminal output

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (complaint_text, sentiment)
        VALUES (?, ?)
    """, (complaint_text, sentiment))

    conn.commit()
    conn.close()

    # IMPORTANT: show sentiment in browser
    return f"Complaint submitted! Sentiment score: {sentiment}"

# Admin Page
@app.route("/admin")
def admin():
    return render_template("admin.html")

# Run App
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
