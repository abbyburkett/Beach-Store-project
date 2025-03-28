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
def createEmployee(username, password, fname, lname, pay_rate):

    if not username or not password:
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

        # Insert new employee into the database
        cursor.execute("INSERT INTO Employee (UserName, PinPassword, FName, LName, Role, PayRate) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (username, hash_password(password), fname, lname, 'Employee', pay_rate))

        db.commit()
        print("Successfully registered")
        cursor.close()
        db.close()
        return True
    except mysql.connector.Error as err:
        print(f"Register Fail: {err}")
        cursor.close()
        db.close()
        return False
    
def get_all_Emp_data():
        employee_data = []
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password=db_password,
                database='BeachStore'
            )
            cursor = db.cursor()

            cursor.execute("SELECT UserName, FName, LName, Role, PayRate FROM Employee")
            employees = cursor.fetchall()

            # Store employee data in a list
            for emp in employees:
                employee_data.append(emp)

            db.close()

        except mysql.connector.Error as err:
            print(f"Error fetching employee data: {err}")
        
        return employee_data

def update_employee_in_db(username, fname, lname, pay_rate):
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password=db_password,
            database='BeachStore'
        )
        cursor = db.cursor()

        # Update the employee in the database
        cursor.execute("""
            UPDATE Employee
            SET FName = %s, LName = %s, PayRate = %s
            WHERE UserName = %s
        """, (fname, lname, pay_rate, username))

        db.commit()
        db.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating employee: {err}")
        return False
    
def delete_employee_from_db(username):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password=db_password,
                database='BeachStore'
            )
            cursor = db.cursor()

            cursor.execute("DELETE FROM Employee WHERE UserName = %s", (username,))
            db.commit()
            db.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error deleting employee: {err}")
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

