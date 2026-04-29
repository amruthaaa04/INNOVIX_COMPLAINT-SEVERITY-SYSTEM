# 🚀 Intelligent Complaint Severity & 

---

## 📌 Problem Statement

Public service authorities receive a large number of citizen complaints daily. However, existing systems lack intelligent prioritization, leading to delays in resolving critical issues.

This project builds an **intelligent decision-support system** that:

* Analyzes complaint text
* Predicts severity
* Detects duplicate issues
* Prioritizes complaints for faster response

---

## 💡 Solution Overview

We developed a **web-based intelligent complaint management system** where:

👤 Users submit complaints
🧠 System analyzes using NLP + ML
🔁 Detects duplicate complaints
📊 Assigns priority dynamically
🧑‍💼 Admin dashboard supports decision-making

---

## ⚙️ Key Features

* 🧠 NLP-based complaint analysis
* 📊 Severity prediction (High / Medium / Low)
* 🔁 Duplicate detection using TF-IDF + Cosine Similarity
* ⚡ Priority boosting for repeated complaints
* 📋 Admin dashboard with insights
* 🤖 AI-based action recommendations
* 📤 Export reports (CSV)

---

## 🧱 Tech Stack

| Layer               | Technology                         |
| ------------------- | ---------------------------------- |
| Frontend            | HTML, CSS, JavaScript              |
| Backend             | Python (Flask)                     |
| NLP                 | TextBlob                           |
| Machine Learning    | Logistic Regression (Scikit-learn) |
| Duplicate Detection | TF-IDF + Cosine Similarity         |
| Database            | SQLite                             |

---

## 🧪 System Workflow

```text
User submits complaint
        ↓
NLP analyzes text
        ↓
ML predicts severity
        ↓
Duplicate detection runs
        ↓
Priority assigned
        ↓
Stored in database
        ↓
Admin dashboard displays insights
```

---

## 📸 Screenshots

### 🏠 User Complaint Form

<img width="707" height="593" alt="Screenshot 2026-04-29 064836" src="https://github.com/user-attachments/assets/22e15a8c-3ed6-4f37-bff4-64f790df3bab" />


### 📊 Admin Dashboard

<img width="1809" height="914" alt="Screenshot 2026-04-29 064805" src="https://github.com/user-attachments/assets/4267248c-ae5c-4c85-a6bf-2d5ea3ecd8ac" />


### 📋 Complaint Table with Insights

<img width="850" height="571" alt="Screenshot 2026-04-29 064812" src="https://github.com/user-attachments/assets/fe5d829e-a0d2-4e9c-807a-a4d16cf779a1" />


---

## ▶️ How to Run

### 1. Clone Repository

```
git clone https://github.com/amruthaaa04/INNOVIX_COMPLAINT-SEVERITY-SYSTEM.git
cd INNOVIX_COMPLAINT-SEVERITY-SYSTEM
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Run Application

```
python app.py
```

### 4. Open Browser

```
http://127.0.0.1:5000/
```

---

## 📊 Admin Capabilities

* View all complaints
* Monitor severity & priority
* Identify frequent issues
* Update complaint status
* Export reports

---

## 🎯 Impact

* ⏱ Faster resolution of critical issues
* 📉 Reduced redundancy via duplicate detection
* 📊 Data-driven decision-making
* 🏛 Improved public service efficiency

---

## 🔮 Future Enhancements

* 📍 Location-based clustering
* 📱 Mobile-friendly UI
* 🌐 Cloud deployment
* 🔔 Real-time notifications
* 📊 

---

## 📢 Final Note

This project demonstrates how **NLP + Machine Learning** can transform traditional complaint systems into intelligent, efficient, and scalable decision-support platforms.
