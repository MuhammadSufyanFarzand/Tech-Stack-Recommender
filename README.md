# 🚀 Tech Stack Recommender

> **A Machine Learning-powered recommendation system developed during my Machine Learning Internship at Decode Lab.** The application analyzes a user's technical skills and recommends the most suitable technology stacks using Natural Language Processing (NLP), TF-IDF Vectorization, and Cosine Similarity.

---

# 📌 Project Overview

Choosing the right technology stack can be overwhelming for students and developers. This project simplifies the decision-making process by analyzing a user's existing skills and recommending the most relevant technology stacks.

Developed during my **Machine Learning Internship at Decode Lab**, this project demonstrates how Machine Learning and Natural Language Processing can be applied to build an intelligent recommendation system.

The recommendation engine converts user skills into numerical vectors using **TF-IDF Vectorization**, compares them with predefined technology stacks using **Cosine Similarity**, and returns the most relevant recommendations along with similarity scores.

---

# 🎯 Objectives

- Build an intelligent recommendation system.
- Learn practical NLP techniques.
- Apply Machine Learning to real-world problems.
- Recommend technology stacks based on user skills.
- Develop a modular and scalable Python application.

---

# ✨ Features

- 🔍 Skill-based technology stack recommendation
- 🤖 Machine Learning recommendation engine
- 📊 TF-IDF Vectorization
- 📈 Cosine Similarity matching
- 📂 CSV dataset support
- ⚡ Fast recommendation generation
- 🖥️ Streamlit web interface
- 📦 Automatic project ZIP generator
- 🧩 Modular project architecture
- 📄 Easy to extend with new technology stacks

---

# 🛠️ Technologies Used

## Programming Language

- Python

## Machine Learning

- Scikit-learn

## NLP

- TF-IDF Vectorization
- Cosine Similarity

## Libraries

- Pandas
- NumPy
- Scikit-learn
- Streamlit

---

# 📁 Project Structure

```text
tech-stack-recommender/
│
├── data/
│   └── raw_skills.csv
│
├── src/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── vectorizer.py
│   └── similarity.py
│
├── models/
│   └── (Generated model files)
│
├── create_zip.py
├── app.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/tech-stack-recommender.git
```

## Navigate to Project

```bash
cd tech-stack-recommender
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

After running the command, the application will automatically open in your web browser.

---

# 📊 Dataset

The recommendation engine uses a CSV dataset containing technology stacks and their associated technical skills.

Example Dataset:

| Technology Stack | Skills |
|------------------|--------|
| MERN Stack | React, Node.js, Express, MongoDB |
| Django | Python, Django, PostgreSQL |
| Data Science | Python, Pandas, NumPy, Scikit-learn |
| Machine Learning | Python, TensorFlow, PyTorch |
| DevOps | Docker, Kubernetes, Linux |

---

# 🧠 Machine Learning Workflow

1. Load dataset
2. Clean and preprocess data
3. Convert skills into TF-IDF vectors
4. Build feature matrix
5. Calculate cosine similarity
6. Compare user skills with available stacks
7. Rank recommendations
8. Display top matching technology stacks

---

# 📌 Example

### Input Skills

```
Python
Pandas
NumPy
Scikit-learn
```

### Recommended Technology Stacks

```
✅ Data Science
Similarity Score: 97%

✅ Machine Learning
Similarity Score: 93%

✅ Artificial Intelligence
Similarity Score: 89%
```

---

# 📈 Future Improvements

- Deep Learning recommendation engine
- Personalized learning roadmap
- User authentication
- Database integration
- Skill gap analysis
- REST API development
- Docker support
- Cloud deployment
- Multiple recommendation algorithms

---

# 🎓 Internship Project

This project was developed as part of my **Machine Learning Internship at Decode Lab**.

The project focuses on applying Machine Learning and Natural Language Processing techniques to build an intelligent recommendation system that helps users discover the most suitable technology stacks based on their existing technical skills.

During this internship, I gained practical experience in:

- Data preprocessing
- NLP
- TF-IDF Vectorization
- Cosine Similarity
- Recommendation Systems
- Modular Python Development
- Streamlit Application Development

---

# 📷 Project Demo

Add screenshots or a deployed application link here.

Example:

- Home Page
- Recommendation Results
- Similarity Score Output

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

## Muhammad Sufyan

**BS Information Technology Student**

**Machine Learning Intern at Decode Lab**

### Interests

- Machine Learning
- Artificial Intelligence
- Natural Language Processing
- Recommendation Systems
- Data Science

### Connect with Me

**LinkedIn**

https://www.linkedin.com/in/muhammad-sufyan-farzand-096a3b377/

---

⭐ **If you found this project helpful, please consider giving it a Star on GitHub!**
