import mysql.connector
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv('MYSQL_PASSWORD')


# Hash Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Add User
def createEmployee(username, password, fname, lname):

    if not username or not password:
        # messagebox.showerror("Error", "All fields are required!")
        return False

    try:
        if db_password is None:
            print("Error: MYSQL_PASSWORD environment variable is not set!")
        else:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password=db_password,
                database='BeachStore'
            )
            
        cursor = db.cursor()


        hashed_pw = hash_password(password)
        cursor.execute("INSERT INTO Employee (UserName, PinPassword, FName, LName, Role) VALUES (%s, %s, %s, %s, %s)", (username, hashed_pw, fname, lname, 'Employee'))
        db.commit()
        # messagebox.showinfo("Success", "User registered successfully!")
        print("Successfullly register")
        return True
    except mysql.connector.Error as err:
        # messagebox.showerror("Error", f"Database error: {err}")
        print(f"Register Fail: {err}")
        return False

def getPayData(employeeID, columns):
    # Placeholder data: (PayAmount, BonusPercentage, GrossBonus, GrossPaid)

    data = [
        (100, 10, 1000, 1100),
        (200, 20, 2000, 1200),
        (300, 30, 3000, 1300),
        (400, 40, 4000, 1400),
    ]


    return data

def getCloseOutData(ProfitID, columns, target_date):

    data = [(102, 300.50, 400.75, 80.00, 20.25, 100.25, "2025-03-16")]
    

    return data

def getUserProfileData(employeeID):

    user_data = [
        (101, "John", "Doe", "******", "johndoe", "Employee")
    ]

    return user_data

