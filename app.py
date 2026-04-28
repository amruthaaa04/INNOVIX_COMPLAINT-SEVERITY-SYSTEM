from flask import Flask, render_template, request
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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

train_texts = [
    # ---------------- HIGH ----------------
    "Gas leak in apartment building emergency",
    "Fire broke out in school laboratory",
    "Hospital has no electricity during surgery",
    "Severe accident on highway injured people",
    "School building collapsed partially",
    "No drinking water in entire village for days",
    "Women are being harassed near bus stop at night",
    "Street is unsafe due to criminal activity",
    "Chain snatching incidents increasing in locality",
    "No CCTV cameras in crime prone area",
    "Gas leakage smell from factory",
    "Fire in slum area no fire brigade arrived",
    "Hospital refusing emergency treatment",
    "Chemical waste dumped into lake",
    "Severe air pollution from burning waste",
    "Flood water entering houses",

    # ---------------- MEDIUM ----------------
    "No proper education due to low funding in school",
    "Road is full of potholes and damaged",
    "Sewage water overflowing on street",
    "Water supply is irregular in our area",
    "Bus service is delayed every day",
    "School classrooms are in bad condition",
    "Teacher shortage affecting studies",
    "Students not getting learning materials",
    "No job opportunities in local area",
    "Skill development programs not available",
    "Government job application process delayed",
    "Air pollution due to construction work",
    "Factory releasing smoke affecting residents",
    "Noise pollution from loudspeakers at night",
    "River water contaminated by sewage",
    "Public transport frequency is very low",

    # ---------------- LOW ----------------
    "Street light not working in my street",
    "Garbage not collected for two days",
    "Park maintenance is needed",
    "Cleaning of street required",
    "Broken bench in public park",
    "Tree trimming required near road",
    "Grass not maintained in park",
    "Playground equipment damaged",
    "Streetlight not working in lane",
    "Public dustbins are overflowing",
    "Painting of walls required in locality",
    "Small drainage blockage causing smell",
    "Minor road repair needed",
    "Broken signboard in street",
    "Need cleaning in park area",
    "Street sweeping not done"
]

train_labels = [
    # HIGH (16)
    "High","High","High","High","High","High","High","High",
    "High","High","High","High","High","High","High","High",

    # MEDIUM (16)
    "Medium","Medium","Medium","Medium","Medium","Medium","Medium","Medium",
    "Medium","Medium","Medium","Medium","Medium","Medium","Medium","Medium",

    # LOW (16)
    "Low","Low","Low","Low","Low","Low","Low","Low",
    "Low","Low","Low","Low","Low","Low","Low","Low"
]
critical_keywords = [
    "emergency", "fire", "accident", "hospital",
    "death", "injury", "gas leak", "collapse"
] 
education_keywords = [
    "school", "education", "teacher", "funding"
]
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,2)
)
X_train = vectorizer.fit_transform(train_texts)

model = LogisticRegression()
model.fit(X_train, train_labels)  

def is_duplicate(new_text):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT complaint_text FROM complaints")
    existing = cursor.fetchall()
    conn.close()

    if not existing:
        return False

    all_texts = [row[0] for row in existing]
    all_texts.append(new_text)

    vectors = vectorizer.transform(all_texts)

    similarity = cosine_similarity(vectors[-1], vectors[:-1])

    max_sim = float(np.max(similarity))

    if max_sim > 0.8:
        return True

    return False

def get_priority(severity, sentiment):
    base = 0

    if severity == "High":
        base = 90
    elif severity == "Medium":
        base = 60
    else:
        base = 30

    # sentiment adjustment
    if sentiment < -0.5:
        base += 10

    return min(base, 100)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    complaint_text = request.form["complaint"]

    # sentiment
    blob = TextBlob(complaint_text)
    sentiment = blob.sentiment.polarity 

    if sentiment > 0:
        sentiment_label = "Positive"
    elif sentiment < 0:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    # duplicate check FIRST
    if is_duplicate(complaint_text):
        return "Duplicate complaint detected. Already exists in system."

    # ML prediction
    X_input = vectorizer.transform([complaint_text])
    severity = model.predict(X_input)[0]

    # priority
    priority = get_priority(severity, sentiment)

    # store in DB ONCE
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO complaints (complaint_text, sentiment, severity, priority) VALUES (?, ?, ?, ?)",
        (complaint_text, sentiment, severity, priority)
    )

    conn.commit()
    conn.close()

    return f"Predicted Severity: {severity}, Sentiment: {sentiment_label}, Priority: {priority}"

@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True) 
 
