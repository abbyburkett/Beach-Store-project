import mysql.connector
import hashlib
from tkinter import messagebox
import os

#db_password = os.getenv('MYSQL_PASSWORD')


# Hash Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# database connection
def create_db_connection():
    try:
        db_password = os.getenv('MYSQL_PASSWORD')
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password=db_password,
            database='BeachStore'
        )
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# Add User
def create_employee(username, password, fname, lname, pay_rate, pay_bonus):

    if not username or not password:
        return False

    try:
        if db_password is None:
            print("Error: MYSQL_PASSWORD environment variable is not set!")
            return False

        db = create_db_connection()
        if db is None:
            return False

        cursor = db.cursor()

        # Insert new employee into the database
        cursor.execute("INSERT INTO Employee (UserName, PinPassword, FName, LName, Role, PayRate, PayBonus) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (username, hash_password(password), fname, lname, 'Employee', pay_rate, pay_bonus))

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
            db = create_db_connection()
            if db is None:
                return employee_data
            cursor = db.cursor()

            cursor.execute("SELECT EmployeeID, UserName, FName, LName, Role, PayRate, PayBonus FROM Employee")
            employees = cursor.fetchall()

            for emp in employees:
                employee_data.append(emp)

            db.close()
            cursor.close()

        except mysql.connector.Error as err:
            print(f"Error fetching employee data: {err}")
        
        return employee_data

def update_employee_in_db(username, fname, lname, pay_rate, bonus_rate):
    try:
        db = create_db_connection()
        if db is None:
            return False

        cursor = db.cursor()

        # Update the employee in the database
        cursor.execute("""
            UPDATE Employee
            SET FName = %s, LName = %s, PayRate = %s, PayBonus = %s
            WHERE UserName = %s
        """, (fname, lname, pay_rate, bonus_rate, username))

        db.commit()
        db.close()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print("The username ", username)
        print("The fname ", fname)
        print("The lname ", lname)
        print("The payRate ", pay_rate)
        print("The bonus ", bonus_rate)
        print(f"Error updating employee: {err}")
        return False
    
def delete_employee_from_db(employee_id):
        try:
            db = create_db_connection()
            if db is None:
                return False

            cursor = db.cursor()

            cursor.execute("DELETE FROM Employee WHERE EmployeeID = %s", (employee_id,))
            db.commit()
            db.close()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error deleting employee: {err}")
            return False


def get_pay_data(employeeID, columns):
    # Placeholder data: (PayAmount, BonusPercentage, GrossBonus, GrossPaid)

    return [[1000, 0.32, 1234, 12334]]
    
def get_location_data():
    location_data = []
    try:
        db = create_db_connection()
        if db is None:
            return location_data

        cursor = db.cursor()
        cursor.execute("SELECT LocationID, Name, Address, ManagerID FROM Location")
        locations = cursor.fetchall()

        for loc in locations:
            location_data.append(loc)

        db.close()
        cursor.close()

    except mysql.connector.Error as err:
        print(f"Error fetching location data: {err}")

    return location_data
 
def add_location(name, address, manager_id):
    try:
        db = create_db_connection()
        if db is None:
            return False

        cursor = db.cursor()
        query = """
            INSERT INTO Location (Name, Address, ManagerID)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (name, address, manager_id))
        db.commit()

        update_query = """
            UPDATE Employee
            SET Role = 'Manager'
            WHERE EmployeeID = %s
        """
        cursor.execute(update_query, (manager_id,))
        db.commit()

        db.close()
        cursor.close()
        return True

    except mysql.connector.Error as err:
        print(f"Error adding location: {err}")
        return False

def update_location(location_id, name, address, manager_id):
    try:
        db = create_db_connection()
        if db is None:
            return False

        cursor = db.cursor()
        query = """
            UPDATE Location
            SET Name = %s, Address = %s, ManagerID = %s
            WHERE LocationID = %s
        """
        cursor.execute(query, (name, address, manager_id, location_id))
        db.commit()
        db.close()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating location: {err}")
        return False

def delete_location(location_id):
    try:
        db = create_db_connection()
        if db is None:
            return False

        cursor = db.cursor()
        
        cursor.execute("DELETE FROM Location WHERE LocationID = %s", (location_id,))
        
        db.commit()
        db.close()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error deleting location: {err}")
        return False


def get_before_balance(employeeID, date, locationID):

    try:
        db = create_db_connection()
        if db is None:
            return False
        
        cursor = db.cursor()
        
        query = """
                SELECT BeforeBal
                FROM ClockInOut
                WHERE EmployeeID = %s AND Date = %s AND LocationID = %s
                """
        cursor.execute(query, (employeeID, date, locationID))
        result = cursor.fetchone()

        cursor.close()
        db.close()
        return result[0] if result else 0.0
    
    except mysql.connector.Error as err:
            print(f"Error deleting employee: {err}")
            return False

def get_user_profile_data(employeeID):

    try:
        db = create_db_connection()
        if db is None:
            return False
        
        cursor = db.cursor()
        
        query = """
                SELECT FName, LName, UserName, Role
                FROM Employee
                WHERE EmployeeID = %s
                """
        cursor.execute(query, (employeeID,))
        data = cursor.fetchall()

        cursor.close()
        db.close()
        return data
    
    except mysql.connector.Error as err:
            print(f"Error deleting employee: {err}")
            return False
    
def clock_out(user_id, date, locationID):
    try:
        db = create_db_connection()
        if db is None:
            return False

        cursor = db.cursor()

        cursor.execute("""
                    UPDATE ClockInOut
                    Set ClockOut = NOW()
                    Where EmployeeID = %s AND Date = %s AND LocationID = %s AND ClockIn = ClockOut 
               """, (user_id, date, locationID))
        db.commit()
        db.close()
        cursor.close()
        print("You have been successfully clocked out!")
        return True
    except mysql.connector.Error as err:
        print(f"Error recording Clock Out: {err}")
        return False

def clock_in(user_id, date, locationID, balance):
    try:
        db = create_db_connection()
        if db is None:
            return False

        cursor = db.cursor()

        cursor.execute("""
            SELECT COUNT(*) 
            FROM ClockInOut
            WHERE EmployeeID = %s AND Date = %s AND locationID = %s AND ClockIn = ClockOut
        """, (user_id, date, locationID))
        existing_clock_in = cursor.fetchone()[0]

        if existing_clock_in > 0:
            messagebox.showwarning("Already Clocked In", "You have to clock out first!")
            db.close()
            cursor.close()
            return False

        cursor.execute("""
            INSERT INTO ClockInOut (EmployeeID, ClockIn, Date, LocationID, BeforeBal)
            VALUES (%s, NOW(), %s, %s, %s)
        """, (user_id, date, locationID, balance))

        db.commit()
        db.close()
        cursor.close()
        print("Clock In recorded successfully!")
        return True
    except mysql.connector.Error as err:
        print(f"Error recording Clock In: {err}")
        return False