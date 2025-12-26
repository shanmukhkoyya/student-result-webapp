import streamlit as st
import sqlite3
import pandas as pd

# ================= DATABASE CONNECTION =================
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

# ================= USERS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# ================= STUDENTS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    student_name TEXT,
    subject1 INTEGER,
    subject2 INTEGER,
    subject3 INTEGER,
    total INTEGER,
    average REAL,
    result TEXT
)
""")

conn.commit()

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ================= APP TITLE =================
st.title("Student Result Management System")

# ================= AUTHENTICATION =================
menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

# ---------- SIGN UP ----------
if menu == "Sign Up":
    st.subheader("Create New Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (new_user, new_pass)
            )
            conn.commit()
            st.success("Account created successfully! Please login.")
        except:
            st.error("Username already exists")

# ---------- LOGIN ----------
elif menu == "Login":
    st.subheader("Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (user, pwd)
        )
        data = cursor.fetchone()

        if data:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.success("Login successful")
        else:
            st.error("Invalid username or password")

# ================= MAIN APP (AFTER LOGIN) =================
if st.session_state.logged_in:

    st.success(f"Welcome, {st.session_state.username}")

    st.subheader("Add Student Result")

    student_name = st.text_input("Student Name")
    s1 = st.number_input("Subject 1 Marks", 0, 100)
    s2 = st.number_input("Subject 2 Marks", 0, 100)
    s3 = st.number_input("Subject 3 Marks", 0, 100)

    if st.button("Add Result"):
        total = s1 + s2 + s3
        average = round(total / 3, 2)
        result = "Pass" if s1 >= 35 and s2 >= 35 and s3 >= 35 else "Fail"

        cursor.execute("""
        INSERT INTO students
        (username, student_name, subject1, subject2, subject3, total, average, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            st.session_state.username,
            student_name,
            s1, s2, s3,
            total,
            average,
            result
        ))

        conn.commit()
        st.success("Result added successfully")

    st.subheader("My Results")

    df = pd.read_sql(
        "SELECT student_name, subject1, subject2, subject3, total, average, result FROM students WHERE username=?",
        conn,
        params=(st.session_state.username,)
    )

    st.dataframe(df)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()
