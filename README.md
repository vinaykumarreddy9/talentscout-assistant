# 📄 TalentScout: AI-Powered Hiring Assistant

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Framework-Streamlit-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/LLM-Llama_3-green.svg" alt="Llama 3">
  <img src="https://img.shields.io/badge/Engine-LangGraph-orange.svg" alt="LangGraph">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
</div>

**TalentScout** is an intelligent, interactive hiring assistant designed to streamline and automate the initial candidate screening process. By leveraging Large Language Models (LLMs), it conducts dynamic interviews, evaluates responses with a structured rubric, and provides a comprehensive dashboard for recruiters.

---

### 📌 Table of Contents
1. [About The Project](#-about-the-project)
    - [Key Features](#-key-features)
    - [Tech Stack](#-tech-stack)
2. [Live Demo](#-live-demo)
3. [Getting Started](#-getting-started)
    - [Prerequisites](#-prerequisites)
    - [Installation & Setup](#-installation--setup)
4. [Usage](#-usage)
    - [Running the Application](#-running-the-application)
    - [Admin Panel Access](#-admin-panel-access)
5. [Core Logic: The LangGraph Workflow](#-core-logic-the-langgraph-workflow)
6. [Database Schema](#-database-schema)
7. [Project Structure](#-project-structure)
8. [Roadmap](#-roadmap)
9. [Contributing](#-contributing)
10. [License](#-license)

---

## 🧐 About The Project

TalentScout addresses the challenge of initial technical screening by providing a consistent, unbiased, and automated interview experience. It assesses candidates based on their conceptual understanding of their stated skills, freeing up hiring managers to focus on qualified candidates.

### ✨ Key Features

-   **📝 Dynamic Candidate Assessment**: Gathers candidate information, experience, and skills to tailor the interview.
-   **🤖 AI-Generated Questions**: Dynamically creates five unique, domain-specific conceptual questions—no coding required.
-   **🧠 Intelligent Evaluation**: Utilizes a `LangGraph`-powered workflow to evaluate candidate answers based on correctness, grammar, sentiment, confidence, and conciseness.
-   **📊 Centralized Admin Dashboard**: A secure panel for administrators to review all candidate profiles, interview responses, and evaluation scores.
-   **⬇️ Data Export**: Easily export all candidate and response data to a CSV file for further analysis or record-keeping.
-   **💾 Persistent Storage**: All data is reliably stored in a local SQLite database, which is automatically generated.

### 🛠️ Tech Stack

| Category | Technology / Tool |
| :--- | :--- |
| 🖥 **Frontend UI** | Streamlit |
| 🧠 **LLM Orchestration**| LangChain |
| ⚡ **LLM Inference** | Groq API with Llama 3 |
| ⚙ **Workflow Engine**| LangGraph |
| 🗃 **Database** | SQLite 3 |
| 🐍 **Language** | Python 3.11+ |

---

## 🚀 Live Demo

The application consists of two primary interfaces, both built with Streamlit:
1.  **Candidate Interview App**: The portal where candidates take the automated interview.
2.  **Admin Panel**: The dashboard for reviewing candidate submissions and analytics.

You can navigate between both pages using the sidebar in the Streamlit application.



---

## 🏁 Getting Started

Follow these instructions to get a local copy of TalentScout up and running.

### ✅ Prerequisites

-   Python 3.11+
-   Git
-   A **Groq API Key** for LLM inference. You can get one from the [Groq Console](https://console.groq.com/keys).

### ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/vinaykumarreddy9/talentscout-hiring-assistant.git
    cd talentscout-hiring-assistant
    ```

2.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    Create a `.env` file in the root directory and add your Groq API key.
    ```sh
    echo "GROQ_API_KEY=your_groq_api_key" > .env
    ```

4.  **Initialize the database:**
    This command creates the `talentscout.db` file and sets up the necessary tables.
    ```sh
    python init_db.py
    ```

---

## 💡 Usage

### Running the Application

Launch the Streamlit multi-page application with a single command:

```bash
streamlit run home.py
```

Your web browser will open a new tab with the TalentScout homepage.
### Admin Panel Access
Navigate to the "Admin" page from the sidebar to access the dashboard.

Email: admin@talentscout.ai

Password: admin123


🧠 Core Logic: The LangGraph Workflow
The intelligence of this application is powered by a LangGraph workflow defined in graph/workflow.py. This graph determines the logic for handling a candidate's session.

```workflow
graph TD
    A[START] --> B{Has Unanswered Question?};
    B -->|No| C[Question Generator Node];
    B -->|Yes| D[Evaluator Node];
    C --> E[END];
    D --> E[END];
```

**Router Node**: The entry point that checks the current state to decide the path. If an unanswered question exists in the state, it routes to the evaluator. Otherwise, it proceeds to the question_generator.

**Question Generator Node**: Generates a new, relevant interview question based on the candidate's specified skill, experience level, and a desired complexity.

**Evaluator Node**: Takes the candidate's answer and evaluates it against multiple criteria, returning a structured JSON object using a Pydantic schema for consistency.


# 🗃️ Database Schema
Data is stored across two main tables in the talentscout.db SQLite database.
**candidates Table**
```Table
Field	        Type	Description
candidate_id	TEXT	Primary Key, Unique UUID for the candidate
name	        TEXT	Candidate full name
email	        TEXT	Candidate's email address
phone	        TEXT	Candidate's phone number
location	    TEXT	Candidate's location
position	    TEXT	Position applied for
experience	    TEXT	Years of experience
skills	        TEXT	Comma-separated list of skills
session_time	TEXT	Timestamp of the session
```
**Response Table**
```sh
Field	            Type	    Description
id	                INTEGER	    Primary Key, Auto-incrementing ID
candidate_id	    TEXT	    Foreign Key to candidates table
skill	            TEXT	    The skill the question is based on
question	        TEXT	    The question asked
answer	            TEXT	    The candidate answer
sentiment	        TEXT	    Sentiment analysis of the answer
correctness	        INTEGER	    Score for technical correctness
length_score	    INTEGER	    Score for appropriate length
grammar_score	    INTEGER	    Score for grammar
confidence_score	INTEGER	    Score for perceived confidence
```

# 📁 Project Structure
```sh
TalentScout_Hiring_Assistant/
├── pages/
│   ├── 1_interview.py          # Candidate interview app
│   └── 2_admin.py              # Admin panel
├── graph/
│   ├── agent.py                # LangGraph nodes: evaluator, question generator
│   ├── workflow.py             # LangGraph flow configuration
│   └── state.py                # LangGraph state + Pydantic schemas
├── utils/
│   ├── prompts.py              # LLM prompts
│   └── models.py               # Groq model wrapper
├── init_db.py                  # Database setup script
├── home.py                     # Streamlit homepage
├── talentscout.db              # SQLite database (auto-generated)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```


# 🗺️ Roadmap
Here are some planned improvements for future versions of TalentScout:

**Secure Admin Login**: Replace hardcoded credentials with a database-backed authentication system.

**Visual Analytics**: Add charts and graphs to the admin panel for better visualization of candidate performance.

**Email Notifications**: Automatically send confirmation or results emails to candidates upon completion.

**Skill-Level Tagging**: Implement difficulty analysis for questions and tag them accordingly.

**Cloud Database Integration**: Migrate from SQLite to a scalable cloud database like PostgreSQL or MySQL.

**Containerization**: Add a Dockerfile for easy deployment with Docker.

# 🙌 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

**Fork the Project**
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request