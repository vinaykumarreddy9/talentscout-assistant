import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from graph.workflow import app
import sqlite3
import uuid
import datetime
import random
from init_db import initialize_database
from streamlit_lottie import st_lottie
import requests

# --- Save to DB ---
def save_candidate(candidate_id, name, email, experience, phone, location, position, skills):
    conn = sqlite3.connect("talentscout.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?,?,?,?)",
                   (candidate_id, name, email, experience,  phone, location, position, ",".join(skills), str(datetime.datetime.now())))
    conn.commit()
    conn.close()

def save_response(candidate_id, skill, question, answer, feedback):
    conn = sqlite3.connect("talentscout.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO responses
        (candidate_id, skill, question, answer, sentiment, correctness, length_score, grammar_score, confidence_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (candidate_id, skill, question, answer, feedback["sentiment"], feedback["correctness"],
         feedback["length_score"], feedback["grammer_quality"], feedback["confidence"]))
    conn.commit()
    conn.close()
def main():
    if "database" not in st.session_state:
        st.session_state.database = "database"
        initialize_database()

    # --- App Start ---
    st.set_page_config(page_title="TalentScout Interview", layout="centered")

    st.title("🧠 TalentScout AI Hiring Assistant")

    # --- Candidate Info ---
    if "stage" not in st.session_state:
        st.session_state.stage = "collect_info"
        st.session_state.candidate_id = str(uuid.uuid4())

    if st.session_state.stage == "collect_info":
        st.markdown("Welcome! We'll assess your technical communication and skills. Please fill in the details below.")
        name = st.text_input("Full Name")
        st.session_state.name = name
        email = st.text_input("Email")
        phone = st.text_input("Mobile number")
        location = st.text_input("Your current location")
        position = st.text_input("Your desired position")
        experience = st.text_area("Describe your overall tech experience")
        skills_input = st.text_input("Enter your technical skills (comma-separated, at least 5)")
        
        if st.button("Start Assessment"):
            if name and email and experience and skills_input:
                skills = [s.strip() for s in skills_input.split(",") if s.strip()]
                if len(skills) < 5:
                    st.warning("Please enter at least 5 skills.")
                else:
                    st.session_state.skills = random.sample(skills, 5)
                    st.session_state.answers = []
                    save_candidate(candidate_id=st.session_state.candidate_id, name=name, email=email, phone=phone, location=location, position=position, experience=experience, skills=skills)
                    st.session_state.experience = experience
                    st.session_state.stage = "interview"
                    st.rerun()
            else:
                st.warning("Fill all fields before proceeding.")

    # --- Interview Loop ---
    elif st.session_state.stage == "interview":
        st.markdown(f"Welcome {st.session_state.name}! We'll assess your technical communication and skills through this interview.")
        idx = st.session_state.get("question_index", 0)
        if idx < 5:
            skill = st.session_state.skills[idx]
            experience = st.session_state.experience
            complexity = random.randint(0, 50)
            response = app.invoke({"skill" : skill, "experience":experience, "complexity" : complexity})
            question = response["question"]
            st.markdown(f"### Question {idx + 1} on {skill}")
            st.markdown(f"**{question}**")

            answer = st.text_area("Your Answer", key=f"answer_{idx}")
            if st.button("Submit Answer", key=f"submit_{idx}"):
                feedback = app.invoke({"question":question, "answer":answer, "skill":skill})
                save_response(candidate_id=st.session_state.candidate_id, skill=skill, question=question, answer=answer, feedback=feedback)
                st.session_state.answers.append((question, answer, feedback))
                st.session_state.question_index = idx + 1
                st.rerun()
        else:
            st.session_state.stage = "summary"
            st.rerun()

    # --- Final Feedback ---
    elif st.session_state.stage == "summary":
        st.success("🎉 Interview Completed! Here's a summary:")
        for i, (q, a, f) in enumerate(st.session_state.answers):
            st.markdown(f"#### Q{i+1}: {q}")
            st.markdown(f"**Your Answer:** {a}")

        st.session_state.stage = "greetings"
        if st.button("Done"):
            st.rerun()

    elif st.session_state.stage == "greetings":

        # Load Lottie animation
        def load_lottie_url(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()

        thank_you_animation = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_puciaact.json")

        # Apply custom CSS
        st.markdown("""
            <style>
                .main {
                    background-color: #0e1117;
                    color: #ffffff;
                }
                .thank-you-box {
                    background-color: #1e3a5f;
                    padding: 20px;
                    border-radius: 12px;
                    text-align: center;
                    font-size: 20px;
                    font-weight: 500;
                    color: #ffffff;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                }
                .emoji {
                    font-size: 40px;
                    animation: bounce 1s infinite;
                }
                @keyframes bounce {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-8px); }
                }
            </style>
        """, unsafe_allow_html=True)

        # Lottie Animation
        if thank_you_animation:
            st_lottie(thank_you_animation, height=250)

        # Thank You Message
        st.markdown("""
        <div class="thank-you-box">
            <div class="emoji">🎉</div>
            Thank you for participating! <br> 
            We'll get back to you with the next steps soon. <br><br>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()