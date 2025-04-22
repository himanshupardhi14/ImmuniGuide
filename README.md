# 💉 ImmuniGuide — Intelligent Vaccine Recommendation System

Welcome to **ImmuniGuide**, an AI-powered vaccine recommendation web application that helps parents and caregivers determine what vaccines are applicable for children based on their age. It uses clustering, encoders, and **Google's Gemini LLM** to generate intelligent and human-friendly health guidance.

---

##  Features

✅ Predicts applicable vaccines based on child’s age  
✅ Calculates when the next vaccine is due  
✅ Uses machine learning and clustering for accuracy  
✅ Uses **Gemini LLM** to generate medical-style summaries  
✅ Clean, simple web interface with Django forms  
✅ Result page shows recommendations and detailed explanation  

---

##  Powered By

- [Django](https://www.djangoproject.com/)
- [Pandas](https://pandas.pydata.org/)
- [Joblib](https://joblib.readthedocs.io/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
-  Pre-trained ML model & encoders

---

##  Project Structure
```plaintext
ImmuniGuide/                    
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation

├── models/                         # Dataset and ML models
│   ├── vaccine_doses.csv
│   ├── vaccine_clustering_model.pkl
│   ├── vaccine_encoder.pkl
│   └── dose_encoder.pkl

├── ImmuniGuide/                   # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py

├── recommender/                  # Main app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                  # Age input form
│   ├── utils.py                  # ML model + Gemini LLM logic
│   ├── views.py                  # Logic for input/output pages
│   ├── urls.py                   # App-specific routing
│   ├── models.py                 # (Optional: for DB models)

│   ├── templates/
│   │   └── recommender/
│   │       ├── index.html        # Home form page
│   │       └── result.html       # Recommendation result page
```
---

##  Setup & Installation

### 1. Clone the Repo

```bash
git clone https://github.com/himanshupardhi14/ImmuniGuide.git
cd ImmuniGuide
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Add Your Gemini API Key
genai.configure(api_key="YOUR_API_KEY")

### 🖥️ Running the Server
```bash
python manage.py runserver
```
---

##  Example Usage

1:-Enter your child’s age and select the unit (weeks, months, years)

2:-Click Submit

3:-See recommended vaccines + when the next dose is due

4:-Read a detailed explanation powered by Gemini AI

---
### 🖥️ Demo Screenshot

![Vaccine Recommender Screenshot](assets/screenshot.png)

    

