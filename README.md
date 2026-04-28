# INNOVIX_COMPLAINT-SEVERITY-SYSTEM
Problem Statement :
Public service authorities receive a large number of citizen complaints daily, but current systems lack intelligent prioritization, causing delays in resolving critical issues. We aim to build an intelligent decision-support system that analyzes complaint text, predicts severity, detects duplicate issues, and prioritizes complaints to help authorities respond faster and more effectively

Explanation : Our project is an intelligent public complaint management system. Citizens submit complaints through a web platform. The system uses NLP to understand the complaint text, ML to predict severity, detects duplicate complaints from the same area, and ranks them by priority for authorities. This supports faster and more informed decision-making.”

Layer	                Tech
Frontend              HTML, CSS, JavaScript
Backend	              Python (Flask)
NLP	                  TextBlob
ML	                  Rule-based + Logistic     Regression
Duplicate Detection	  TF-IDF + Cosine Similarity
Database	            SQLite
	
Solution 
We are building a web-based intelligent decision-support system where users can submit complaints online. The system uses Natural Language Processing (NLP) and intelligent logic to analyze complaints and assist administrators in prioritizing them effectively.

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


