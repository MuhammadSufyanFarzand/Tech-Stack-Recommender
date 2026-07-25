# 🚀 Project 3: Tech Stack Recommender

A production-ready Content-Based Recommendation Engine using **TF-IDF (Term Frequency - Inverse Document Frequency) Vectorization** and **Cosine Similarity Matrix Calculation** in Python.

---

## 📌 Project Overview

The **Tech Stack Recommender** analyzes project requirements, developer skills, or target job roles, maps them into a high-dimensional vector space, and calculates cosine similarity angles against a dataset of tech stack profiles.

It recommends the optimal combination of programming languages, frameworks, databases, and infrastructure tools with percentage match scores and term contribution breakdowns.

---

## 📐 Mathematical Foundations

### 1. Term Frequency (TF)
Measures how frequently a term $t$ occurs in document $d$:

$$\text{TF}(t, d) = 1 + \log(f_{t,d}) \quad \text{for } f_{t,d} > 0$$

### 2. Inverse Document Frequency (IDF)
Measures how rare or informative a term $t$ is across the corpus of $N$ documents:

$$\text{IDF}(t, D) = \log\left(\frac{1 + N}{1 + \text{DF}(t)}\right) + 1$$

### 3. TF-IDF Weight
Calculates the relative significance of term $t$ in document $d$:

$$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

### 4. Cosine Similarity
Calculates the cosine of the angle between query vector $\mathbf{q}$ and tech stack vector $\mathbf{d}$:

$$\text{Cosine Similarity}(\mathbf{q}, \mathbf{d}) = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\|_2 \|\mathbf{d}\|_2} = \frac{\sum_{i=1}^{n} q_i d_i}{\sqrt{\sum_{i=1}^{n} q_i^2} \sqrt{\sum_{i=1}^{n} d_i^2}}$$

---

## 📂 Project Architecture

```
tech-stack-recommender/
│
├── data/
│   └── raw_skills.csv          # Tech stack dataset with roles, languages, frameworks, DBs
│
├── src/
│   ├── __init__.py             # Package exports (SkillIngestor, TFIDFVectorizerModel, CosineSimilarityEngine)
│   ├── ingestion.py            # Data loading, text cleaning, feature document synthesis
│   ├── vectorizer.py           # TF-IDF vectorizer (scikit-learn with pure Python fallback)
│   └── similarity.py           # Cosine similarity matrix calculation and score ranking
│
├── models/
│   ├── tfidf_vectorizer.pkl    # Serialized vectorizer model weights
│   └── .gitkeep
│
├── create_zip.py               # Script to package the entire project into tech-stack-recommender.zip
├── app.py                      # Application runner (Flask REST API + CLI interactive mode)
├── requirements.txt            # Python dependencies
└── README.md                   # Complete documentation
```

---

## ⚙️ Quick Start Guide

### 1. Clone & Install Dependencies
```bash
git clone <your-repo-url>
cd tech-stack-recommender
pip install -r requirements.txt
```

### 2. Interactive CLI Mode
Run the recommender interactively in your terminal:
```bash
python app.py --cli
```

### 3. Launch Flask Web API
Start the HTTP server on port 5000:
```bash
python app.py
```

### 4. Create Downloadable ZIP Archive
Package the full source code into `tech-stack-recommender.zip`:
```bash
python create_zip.py
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check and API metadata |
| `GET` | `/api/stacks` | Retrieve all loaded dataset tech stacks |
| `POST` | `/api/recommend` | Compute TF-IDF Cosine Similarity recommendations for query |
| `POST` | `/api/retrain` | Force model retraining on updated CSV data |

### Example Request (`POST /api/recommend`)
```json
{
  "query": "Building a Python microservices platform with FastAPI, PostgreSQL, Docker, and Kubernetes",
  "top_n": 3
}
```

---

## 🚀 Deployment Options

### Docker Deployment
1. Build image: `docker build -t tech-stack-recommender .`
2. Run container: `docker run -p 5000:5000 tech-stack-recommender`

### Cloud Run / Production Setup
Set entrypoint command in production environment:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
