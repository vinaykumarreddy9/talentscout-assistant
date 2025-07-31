# pages/2_Admin_Panel.py

import streamlit as st
import sqlite3
import pandas as pd
import hashlib

st.set_page_config(page_title="Admin Panel", layout="wide")

# -------------------------------
# 🔐 Admin Credentials (Hardcoded or use a DB in future)
ADMIN_EMAIL = "admin@talentscout.ai"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()  # store hashed passwords

# -------------------------------
def check_credentials(email, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return email == ADMIN_EMAIL and password_hash == ADMIN_PASSWORD_HASH

# -------------------------------
def get_data(query):
    conn = sqlite3.connect("talentscout.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# -------------------------------
def login_ui():
    st.title("🛡️ Admin Login")

    with st.form("admin_login_form"):
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if check_credentials(email, password):
                st.session_state["admin_logged_in"] = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

# -------------------------------
def admin_dashboard():
    st.title("📊 Admin Dashboard")

    menu = st.sidebar.radio("📁 Choose Table", ["Candidates", "Responses"])

    if menu == "Candidates":
        df = get_data("SELECT * FROM candidates")
        st.subheader("👥 Candidate Submissions")
    else:
        df = get_data("SELECT * FROM responses")
        st.subheader("📝 Interview Responses")

    st.dataframe(df, use_container_width=True)
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name=f"{menu.lower()}.csv")

    if st.button("🔓 Logout"):
        st.session_state["admin_logged_in"] = False
        st.experimental_rerun()

# -------------------------------
def main():
    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False

    if st.session_state["admin_logged_in"]:
        admin_dashboard()
    else:
        login_ui()

if __name__ == "__main__":
    main()
