
# 🚀 TalentScout Hiring Assistant

An AI-powered candidate screening assistant that intelligently evaluates technical candidates based on their provided skillsets and experience.

![Streamlit UI](https://img.shields.io/badge/Built%20With-Streamlit-red?style=for-the-badge)
![LangGraph Workflow](https://img.shields.io/badge/LLM%20Orchestrator-LangGraph-blueviolet?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 Overview

TalentScout is a smart interview assistant that leverages **LangGraph + LLMs** to dynamically:
- Collect candidate info through a sleek **Streamlit** UI
- Generate tech-specific questions from a given skill set
- Analyze responses using **sentiment analysis**, **grammar scoring**, and **LLM-based evaluation**
- Store candidate history and performance securely

---

## 🛠️ Tech Stack

| Area        | Technology          |
|-------------|---------------------|
| Frontend    | Streamlit           |
| Workflow    | LangGraph           |
| LLM Backend | OpenAI API / LLaMA  |
| Database    | SQLite              |
| Language    | Python              |

---

## 💡 Features

- 🌐 Interactive UI for candidate interaction
- 🧠 LLM-generated technical questions based on input skills
- 📊 Sentiment & performance evaluation using LLMs
- 🔐 Local database (SQLite) for storing all candidate sessions securely
- 🧾 Final session summary with performance breakdown

---

## 🧭 Project Structure

```
├── graph/         # LangGraph workflow logic (question generation, evaluation)
├── ui/            # Streamlit UI components
├── utils/         # LLM models, prompts, helper functions
├── init_db.py     # DB setup script
├── requirements.txt
├── streamlit_app.py (you may rename interface.py)
├── talentscout.db (excluded in .gitignore)
```

---

## 🧪 Setup Instructions

### 1️⃣ Clone & Install

```bash
git clone https://github.com/vinaykumarreddy9/talentscout-assistant.git
cd talentscout-assistant
pip install -r requirements.txt
```

### 2️⃣ Initialize Database

```bash
python init_db.py
```

### 3️⃣ Launch App

```bash
streamlit run ui/interface.py
```

---

## 🧠 LangGraph Workflow

The workflow performs two major tasks:

1. **Question Generation** — based on random sampled skills & experience

2. **Response Evaluation** — returns feedback including:

   - Sentiment

   - Correctness score

   - Grammar & length check

   - Confidence indicator

---

## 🔐 Data Security & Multi-user Support

- Each candidate is tracked by a UUID
- All interactions tied to their session ID
- Only stores anonymized local data (SQLite)
- Compatible with future upgrade to PostgreSQL

---

## 🚀 Future Enhancements

- 🌍 Multilingual candidate support
- ☁️ Deployment on Render

---

## 👨‍💻 Author

**Kovvuri Vinay Kumar Reddy** 


