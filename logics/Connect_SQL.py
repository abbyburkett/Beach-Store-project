# import tkinter as tk
# from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
# import hashlib

db_password = os.getenv('MYSQL_PASSWORD')

FILEPATH = "../Tables.sql"

def run_sql_file(file_path):
    try:
        if db_password is None:
            print("Error: MYSQL_PASSWORD environment variable is not set!")
            return
        
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password=db_password
        )

        cursor = db.cursor()
        
        cursor.execute("SHOW DATABASES LIKE 'BeachStore'")
        result = cursor.fetchone()

        if result:
            print("Database 'BeachStore' already exists. Skipping SQL file execution.")
        else:
            # If the database doesn't exist, create it and then run the SQL file
            cursor.execute("CREATE DATABASE BeachStore")
            print("Database 'BeachStore' created.")

            cursor.execute("USE BeachStore")

            with open(file_path, 'r') as file:
                sql_commands = file.read()

            for command in sql_commands.split(';'):
                if command.strip():
                    cursor.execute(command)

            db.commit()
            print("SQL file executed successfully.")

        cursor.close()
        db.close()

    except mysql.connector.Error as e:
        print(f"Error: {e}")



# Verify Login
# def login_user():
#     username = entry_username.get()
#     password = entry_password.get()

#     if not username or not password:
#         messagebox.showerror("Error", "All fields are required!")
#         return

#     hashed_pw = hash_password(PinPassword)


# cursor.execute('use BeachStore')
# cursor.execute('show tables')

# for x in cursor:
#     print(x)
