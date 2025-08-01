import sqlite3

def initialize_database():
    conn = sqlite3.connect("talentscout.db")
    cursor = conn.cursor()

    # Create tables only if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            candidate_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            location TEXT,
            position TEXT,
            experience TEXT,
            skills TEXT,
            session_time TEXT
        )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id TEXT,
        skill TEXT,
        question TEXT,
        answer TEXT,
        sentiment TEXT,
        correctness INTEGER,
        length_score INTEGER,
        grammar_score INTEGER,
        confidence_score INTEGER,
        FOREIGN KEY(candidate_id) REFERENCES candidate_info(id)
    )''')

    conn.commit()
    conn.close()

