import streamlit as st
import sqlite3
import pandas as pd

# ---------- DATABASE ----------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject1 INTEGER,
    subject2 INTEGER,
    subject3 INTEGER,
    total INTEGER,
    average REAL,
    result TEXT
)
""")
conn.commit()

# ---------- WEB APP ----------
st.title("Student Result Management System")

st.subheader("Add Student Result")

name = st.text_input("Student Name")

s1 = st.number_input("Subject 1 Marks", 0, 100)
s2 = st.number_input("Subject 2 Marks", 0, 100)
s3 = st.number_input("Subject 3 Marks", 0, 100)

if st.button("Add Result"):
    total = s1 + s2 + s3
    avg = round(total / 3, 2)
    result = "Pass" if s1 >= 35 and s2 >= 35 and s3 >= 35 else "Fail"

    cursor.execute(
        "INSERT INTO students (name, subject1, subject2, subject3, total, average, result) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, s1, s2, s3, total, avg, result)
    )
    conn.commit()
    st.success("Student result added!")

st.subheader("Student Results")

df = pd.read_sql("SELECT * FROM students", conn)
st.dataframe(df)
