from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_text TEXT,
        sentiment REAL DEFAULT 0,
        severity TEXT,
        priority REAL,
        duplicate_count INTEGER DEFAULT 1,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# ---------------- MODEL ----------------
train_texts = [
    "Gas leak emergency", "Fire accident", "Hospital no electricity",
    "Road potholes", "Water issue", "Garbage not collected",
    "Street light not working", "Park maintenance"
]

train_labels = ["High","High","High","Medium","Medium","Low","Low","Low"]

vectorizer = TfidfVectorizer(stop_words="english")
X_train = vectorizer.fit_transform(train_texts)

model = LogisticRegression()
model.fit(X_train, train_labels)

# ---------------- DUPLICATE CHECK ----------------
def check_duplicate(new_text):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, complaint_text, duplicate_count, priority FROM complaints")
    existing = cursor.fetchall()

    if not existing:
        return None

    texts = [row[1] for row in existing] + [new_text]
    vectors = vectorizer.transform(texts)

    similarity = cosine_similarity(vectors[-1], vectors[:-1])
    max_sim = float(np.max(similarity))
    index = int(np.argmax(similarity))

    if max_sim > 0.8:
        return existing[index]

    return None

# ---------------- PRIORITY ----------------
def get_priority(severity, sentiment):
    base = 90 if severity == "High" else 60 if severity == "Medium" else 30
    if sentiment < -0.5:
        base += 10
    return min(base, 100)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    complaint_text = request.form["complaint"]

    blob = TextBlob(complaint_text)
    sentiment = blob.sentiment.polarity if blob.sentiment else 0.0

    duplicate = check_duplicate(complaint_text)

    # HANDLE DUPLICATE
    if duplicate:
        comp_id, old_text, count, old_priority = duplicate

        new_count = count + 1
        boosted_priority = min(old_priority + 5, 100)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE complaints
            SET duplicate_count=?, priority=?
            WHERE id=?
        """, (new_count, boosted_priority, comp_id))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "duplicate",
            "count": new_count,
            "priority": boosted_priority
        })

    # NEW COMPLAINT
    X_input = vectorizer.transform([complaint_text])
    severity = model.predict(X_input)[0]
    priority = get_priority(severity, sentiment)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (complaint_text, sentiment, severity, priority)
        VALUES (?, ?, ?, ?)
    """, (complaint_text, sentiment, severity, priority))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "severity": severity,
        "priority": priority
    })

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT complaint_text, sentiment, severity, priority, timestamp, duplicate_count
        FROM complaints ORDER BY priority DESC
    """)
    complaints = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE severity='High'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE severity='Medium'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE severity='Low'")
    low = cursor.fetchone()[0]

    one_hour_ago = datetime.now() - timedelta(hours=1)
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE timestamp >= ?", (one_hour_ago,))
    recent_count = cursor.fetchone()[0]

    top = complaints[0] if complaints else None

    conn.close()

    return render_template("admin.html",
                           complaints=complaints,
                           high=high,
                           medium=medium,
                           low=low,
                           top=top,
                           recent_count=recent_count)

# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)