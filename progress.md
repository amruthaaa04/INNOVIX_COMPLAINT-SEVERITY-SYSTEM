# Progress Log

## Day 1(CHECKPOINT 1)

### Completed:
- Repository setup
- Team members added

### In Progress:
- Frontend Implementation 

### Next Steps:
- Build classifier
- NLP processing 

## Day 1(CHECKPOINT 2)
Progress Implemented So Far:
step 1: Project Setup
•	Created Flask project structure 
•	Set up virtual environment 
•	Installed required libraries 
•	Created basic routes for home page and admin dashboard
Step 2: Complaint Submission
•	Built a web form for users to submit complaints 
•	Implemented POST request handling using Flask 
•	Verified successful form submission

Step 3: Database Integration
•	Integrated SQLite database 
•	Created complaints table 
•	Stored complaint text persistently in the database  

How to Run the Project
1.	Install dependencies:
pip install -r requirements.txt
2.	Run the Flask app:
python app.py
3.	Open browser and go to: 
o	http://127.0.0.1:5000/ (Complaint Submission) 
o	http://127.0.0.1:5000/admin (Admin Dashboard) 

 Upcoming Features
•	Rule-based severity prediction 
•	Duplicate complaint detection using text similarity 
•	Priority ranking mechanism 
•	Admin dashboard with sorted complaints   

CHECKPOINT 3 PROGRESS: 
NLP Sentiment Analysis
Implemented using TextBlob
Extracts sentiment polarity from complaint text
Polarity range:
-1 → Very negative
0 → Neutral
+1 → Positive
Sentiment score is stored in the database for analysis and future prioritization
 Machine Learning Severity Prediction
Text complaints are converted into numerical form using TF-IDF Vectorization
A Logistic Regression classifier predicts complaint severity:
Low
Medium
High
A small labeled dataset is used for training as part of the hackathon prototype
 Note: Currently, severity is predicted using ML only.
Hybrid (rule-based + ML) severity correction will be added in upcoming checkpoints.  

CHECKPOINT 4 PROGRESS:  
Developed a ML model and trained it to detect the severity of the complaint and trained it using TF-IDF and sentiment analysis is done suing NLP .
Also implemnted priority tracking of the complaints on the basis of their priority and also implemented duplicate complaint detection to avoid dupliactes and improve the efficiency of the system.
