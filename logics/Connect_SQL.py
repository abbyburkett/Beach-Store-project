# import tkinter as tk
# from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
from logics.dashboard_functions import hash_password
# import hashlib

db_password = os.getenv('MYSQL_PASSWORD')

FILEPATH = "../Tables.sql"

def run_sql_file(file_path = FILEPATH):
    try:
        # Fetch the password from environment variable
        db_password = os.getenv('MYSQL_PASSWORD')
        
        if db_password is None:
            print("Error: MYSQL_PASSWORD environment variable is not set!")
            return
        
        # Connect to the MySQL server
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password=db_password,
            auth_plugin='mysql_native_password'
        )

        cursor = db.cursor()

        # Check if the 'BeachStore' database exists
        cursor.execute("SHOW DATABASES LIKE 'BeachStore'")
        result = cursor.fetchone()

        if not result:
            # If the database doesn't exist, create it
            cursor.execute("CREATE DATABASE BeachStore")
            print("Database 'BeachStore' created.")
        else:
            print("Database 'BeachStore' already exists.")

        cursor.execute("USE BeachStore")

        # Check if the tables exist by using SHOW TABLES
        cursor.execute("SHOW TABLES LIKE 'Employee'")
        employee_table = cursor.fetchone()

        cursor.execute("SHOW TABLES LIKE 'Location'")
        location_table = cursor.fetchone()

        cursor.execute("SHOW TABLES LIKE 'Pay'")
        pay_table = cursor.fetchone()

        cursor.execute("SHOW TABLES LIKE 'ClockInOut'")
        clock_in_out_table = cursor.fetchone()

        cursor.execute("SHOW TABLES LIKE 'Profit'")
        profit_table = cursor.fetchone()

        cursor.execute("SHOW TABLES LIKE 'Expense'")
        expense_table = cursor.fetchone()

        cursor.execute("SHOW TABLES LIKE 'Invoice'")
        invoice_table = cursor.fetchone()

        # If any table is missing, run the SQL file
        if not employee_table or not location_table or not pay_table or not clock_in_out_table or not profit_table or not expense_table or not invoice_table:
            print("One or more tables are missing. Running SQL file to create tables.")
            with open(file_path, 'r') as file:
                sql_commands = file.read()

            # Execute the SQL commands from the file
            for command in sql_commands.split(';'):
                if command.strip():
                    cursor.execute(command)

            db.commit()
            print("SQL file executed successfully.")
        else:
            print("All tables already exist. No need to run SQL file.")

        # Insert default users (Employee, Manager, Owner) if they don't already exist
        cursor.execute("SELECT COUNT(*) FROM Employee WHERE UserName = 'Employee'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Employee (UserName, PinPassword, FName, LName, Role, PayRate) VALUES (%s, %s, %s, %s, %s, %s)", 
                        ('Employee', hash_password("123"), "Emp", "loyee", 'Employee', 15.00))

        cursor.execute("SELECT COUNT(*) FROM Employee WHERE UserName = 'Manager'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Employee (UserName, PinPassword, FName, LName, Role, PayRate) VALUES (%s, %s, %s, %s, %s, %s)", 
                        ('Manager', hash_password("456"), "Mana", "ger", 'Manager', 20.00))

        cursor.execute("SELECT COUNT(*) FROM Employee WHERE UserName = 'Owner'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Employee (UserName, PinPassword, FName, LName, Role, PayRate) VALUES (%s, %s, %s, %s, %s, %s)", 
                        ('Owner', hash_password("789"), "Own", "er", 'Owner', 30.00))

        db.commit()
        
        print("Default users inserted successfully.")

        # Close the cursor and database connection
        cursor.close()
        db.close()

    except mysql.connector.Error as e:
        print(f"Error: {e}")
