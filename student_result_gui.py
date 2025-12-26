import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# ================= DATABASE SETUP =================
conn = sqlite3.connect("students.db")
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
conn.close()

# ================= FUNCTIONS =================
def add_student():
    try:
        name = entry_name.get()
        s1 = int(entry_s1.get())
        s2 = int(entry_s2.get())
        s3 = int(entry_s3.get())

        total = s1 + s2 + s3
        average = round(total / 3, 2)
        result = "Pass" if s1 >= 35 and s2 >= 35 and s3 >= 35 else "Fail"

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO students
        (name, subject1, subject2, subject3, total, average, result)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, s1, s2, s3, total, average, result))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student Result Added")
        clear_fields()
        view_results()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid marks")

def view_results():
    for row in table.get_children():
        table.delete(row)

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        table.insert("", tk.END, values=row)

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_s1.delete(0, tk.END)
    entry_s2.delete(0, tk.END)
    entry_s3.delete(0, tk.END)

# ================= GUI =================
root = tk.Tk()
root.title("Student Result Management System")
root.geometry("800x500")

# -------- INPUT SECTION --------
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Student Name").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_inputs)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Subject 1").grid(row=1, column=0, padx=5, pady=5)
entry_s1 = tk.Entry(frame_inputs)
entry_s1.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Subject 2").grid(row=2, column=0, padx=5, pady=5)
entry_s2 = tk.Entry(frame_inputs)
entry_s2.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Subject 3").grid(row=3, column=0, padx=5, pady=5)
entry_s3 = tk.Entry(frame_inputs)
entry_s3.grid(row=3, column=1, padx=5, pady=5)

# -------- BUTTONS --------
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Add Result", command=add_student, width=15).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="View Results", command=view_results, width=15).grid(row=0, column=1, padx=10)

# -------- TABLE --------
columns = ("ID", "Name", "Sub1", "Sub2", "Sub3", "Total", "Average", "Result")

table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=90, anchor="center")

table.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
