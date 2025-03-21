#import necessary libraries
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import hashlib

# Database Connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='BeachStorePass',
    database='BeachStore'
)

cursor = db.cursor()


# Hash Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Add User
def register_user():

    if not UserName or not PinPassword:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        hashed_pw = hash_password(PinPassword)
        cursor.execute("INSERT INTO Employee (UserName, Password) VALUES (%s, %s)", (UserName, hashed_pw))
        db.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")


# Verify Login
def login_user():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    hashed_pw = hash_password(PinPassword)


cursor.execute('use BeachStore')
cursor.execute('show tables')

for x in cursor:
    print(x)
