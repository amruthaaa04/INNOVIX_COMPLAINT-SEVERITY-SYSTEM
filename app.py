from flask import Flask, render_template, request
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

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
    "Gas leak emergency",
    "Fire accident in building",
    "Road is damaged badly",
    "Water leakage problem",
    "Street light not working",
    "Garbage not collected",
    "Bus stop needs cleaning",
    "Park maintenance required"
]

train_labels = [
    "High", "High",
    "Medium", "Medium",
    "Low", "Low",
    "Low", "Low"
] 

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)

model = LogisticRegression()
model.fit(X_train, train_labels)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    complaint_text = request.form["complaint"]

    # NLP Sentiment Analysis
    blob = TextBlob(complaint_text)
    sentiment = blob.sentiment.polarity  # range: -1 to +1

    # ML Severity Prediction
    X_input = vectorizer.transform([complaint_text])
    severity = model.predict(X_input)[0]

    # Store in database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO complaints (complaint_text, sentiment, severity) VALUES (?, ?, ?)",
        (complaint_text, sentiment, severity)
    )
    conn.commit()
    conn.close()

    print("Sentiment:", sentiment)
    print("Severity predicted:", severity)

    return "Complaint submitted successfully!"
@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True) 
 
