import mysql.connector
import hashlib
from tkinter import messagebox
import os

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
def create_employee(username, password, fname, lname, pay_rate, pay_bonus, role = "Employee"):

    if not username or not password:
        return False

    try:
        db = create_db_connection()
        if db is None:
            return False

        cursor = db.cursor()

        # Insert new employee into the database
        cursor.execute("INSERT INTO Employee (UserName, PinPassword, FName, LName, Role, PayRate, PayBonus) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (username, hash_password(password), fname, lname, role, pay_rate, pay_bonus))

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

            cursor.execute("SELECT EmployeeID, UserName, FName, LName, Role, PayRate, PayBonus FROM Employee WHERE IsDeleted = FALSE")
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

            # cursor.execute("DELETE FROM Employee WHERE EmployeeID = %s", (employee_id,))
            cursor.execute("UPDATE Employee SET IsDeleted = TRUE WHERE EmployeeID = %s", (employee_id,))

            db.commit()
            db.close()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error deleting employee: {err}")
            return False


def get_clock_data(employeeID, locationID):
    try:
        db = create_db_connection()
        if db is None:
            return []

        cursor = db.cursor()

        cursor.execute("""
            SELECT Date, ClockIn, ClockOut, BeforeBal, AfterBal
            FROM ClockInOut
            WHERE EmployeeID = %s AND LocationID = %s
            ORDER BY Date DESC
        """, (employeeID, locationID))

        rows = cursor.fetchall()
        db.close()
        cursor.close()

        return rows

    except mysql.connector.Error as err:
        print(f"Error fetching clock records: {err}")
        return []
    
def get_location_data():
    location_data = []
    try:
        db = create_db_connection()
        if db is None:
            return location_data

        cursor = db.cursor()

        query = """
            SELECT L.LocationID, L.Name, L.Address, E.Username, L.ManagerID
            FROM Location L
            JOIN Employee E ON L.ManagerID = E.EmployeeID
            WHERE L.IsDeleted = FALSE
        """
        cursor.execute(query)
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
            WHERE EmployeeID = %s AND Role != "Owner"
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
        
        # cursor.execute("DELETE FROM Location WHERE LocationID = %s", (location_id,))
        cursor.execute("UPDATE Location SET IsDeleted = TRUE WHERE LocationID = %s", (location_id,))
        
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
                ORDER BY ClockIn DESC
                LIMIT 1
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
                            SET ClockOut = NOW()
                            WHERE ClockInOutID = (
                                SELECT ClockInOutID FROM (
                                    SELECT ClockInOutID FROM ClockInOut
                                    WHERE EmployeeID = %s AND Date = %s AND LocationID = %s AND ClockIn = ClockOut
                                    ORDER BY ClockIn DESC
                                    LIMIT 1
                                ) AS Latest
                            )
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
    
def add_expense(date, locationID, amount, expense_type, is_merch, merch_type):
    try:
        db = create_db_connection()
        if db is None:
            return False

        cursor = db.cursor()

        insert_query = """
            INSERT INTO Expense (Date, LocationID, Amount, ExpenseType, isMerchandise, MerchType)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (date, locationID, amount, expense_type, is_merch, merch_type))
        db.commit()

        cursor.close()
        db.close()
        return True

    except mysql.connector.Error as err:
        print(f"Error recording Clock In: {err}")
        return False
    
def handle_close_out(employeeID, date, locationID, cash, credit):

    try:
        db = create_db_connection()
        if db is None:
            return False

        cursor = db.cursor()
        after_balance = cash + credit

        cursor.execute("""
            SELECT ProfitID FROM Profit WHERE Date = %s AND LocationID = %s
        """, (date, locationID))
        
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE Profit
                SET Cash = %s, Credit = %s, EmployeeID = %s
                WHERE ProfitID = %s
            """, (cash, credit, employeeID, existing[0]))
        else:
            cursor.execute("""
                INSERT INTO Profit (EmployeeID, Cash, Credit, Date, LocationID)
                VALUES (%s, %s, %s, %s, %s)
            """, (employeeID, cash, credit, date, locationID))

        update_clock_out = """
                                UPDATE ClockInOut
                                SET AfterBal = %s
                                WHERE ClockInOutID = (
                                    SELECT ClockInOutID FROM (
                                        SELECT ClockInOutID FROM ClockInOut
                                        WHERE EmployeeID = %s AND Date = %s AND LocationID = %s AND ClockIn != ClockOut
                                        ORDER BY ClockIn DESC
                                        LIMIT 1
                                    ) AS Latest
                                )
                            """
        cursor.execute(update_clock_out, (after_balance, employeeID, date, locationID))

        db.commit()
        cursor.close()
        db.close()
        return True

    except mysql.connector.Error as err:
        print(f"Error during handle_close_out: {err}")
        return False

def get_daily_report_data(location, today = None):

    report_data = []
    try:
        db = create_db_connection()
        cursor = db.cursor(dictionary=True)

        if today:
            current_month = int(today[5:7])
            current_year = int(today[:4])

            cursor.execute("""
                    SELECT 
                        Date,
                        Day,
                        Cash,
                        Credit,
                        ExpenseType,
                        ExpenseValue AS ExpenseAmount,
                        MerchandiseType,
                        MerchandiseValue AS MerchandiseAmount,
                        Payroll
                    FROM Daily_Report_By_Location
                    WHERE MONTH(Date) = %s AND YEAR(Date) = %s AND LocationID = %s
                    ORDER BY Date;
                """, (current_month, current_year, location))
        report_data = cursor.fetchall()
        db.commit()
        db.close()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error updating expense: {err}")
    return report_data

def get_expense_for_the_month(today):
    
    current_year = int(today[:4])
    current_month = int(today[5:7])

    expense_data = []

    try:
        # Connect to the database
        db = create_db_connection()
        if db is None:
            return expense_data

        cursor = db.cursor()

        query = """
        SELECT ExpenseID, Date, Amount, ExpenseType, isMerchandise, MerchType
        FROM Expense
        WHERE YEAR(Date) = %s AND MONTH(Date) = %s
        """
        cursor.execute(query, (current_year, current_month))
        expenses = cursor.fetchall()

        for expense in expenses:
            expense_data.append(expense)

        db.close()
        cursor.close()

    except mysql.connector.Error as err:
        print(f"Error fetching expenses data: {err}")
        
    return expense_data

def update_expense(expense_id, date, amount, expense_type, is_merch, merch_type):
    try:
        db = create_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE Expense
            SET Date = %s, Amount = %s, ExpenseType = %s,
                isMerchandise = %s, MerchType = %s
            WHERE ExpenseID = %s
        """, (date, amount, expense_type, is_merch, merch_type, expense_id))
        db.commit()
        db.close()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error updating expense: {err}")


def delete_expense(expense_id):
    try:
        db = create_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM Expense WHERE ExpenseID = %s", (expense_id,))
        db.commit()
        db.close()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error deleting expense: {err}")

def load_invoices():
    try:
        db = create_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT InvoiceNumber, Date, Company, AmountTotal, AmountPaid, DueDate, PaidWay, Paid FROM Invoice")
        invoices = cursor.fetchall()

        cursor.close()
        db.close()
    except mysql.connector.Error as err:
        print(f"Error deleting expense: {err}")
    
    return invoices
    

def insert_invoice(company, amount, amount_paid, payway, due_date):
    try:
        db = create_db_connection()
        cursor = db.cursor()
        query = ("INSERT INTO Invoice (Company, AmountTotal, AmountPaid, PaidWay, DueDate)"
                     "VALUES (%s, %s, %s, %s, %s) ")
        cursor.execute(query, (company, amount, amount_paid, payway, due_date))
        db.commit()
        cursor.close()
        db.close()

        return True
    except mysql.connector.Error as err:
        # print(f"Error updating expense: {err}")
        messagebox.showerror("Error", err)

        return False
    
def update_invoice_payment(invoice_number, new_payment):
    try:
        db = create_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT AmountPaid, AmountTotal FROM Invoice WHERE InvoiceNumber = %s", (invoice_number,))
        result = cursor.fetchone()
        if result:
            amount_paid, amount = result
            updated_amount = float(amount_paid) + float(new_payment)

            if updated_amount > amount:
                messagebox.showerror("Error", "Payment exceeds total amount.")
                return

            # Update the AmountPaid
            cursor.execute("UPDATE Invoice SET AmountPaid = %s WHERE InvoiceNumber = %s",
                        (updated_amount, invoice_number))
            db.commit()
        cursor.close()
        db.close()

        return True
    except mysql.connector.Error as err:
        print(f"Error updating expense: {err}")

        return False
    
def delete_invoice(invoice_number):
    try:
        db = create_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM Invoice WHERE InvoiceNumber = %s",(invoice_number,))
        db.commit()
        cursor.close()
        db.close()

        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Error", "Failed to delete invoice. {e}")
        return False
    
def get_withdrawal_data(location_id):
    withdrawal_data = []
    try:
        db = create_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT Date, Amount FROM Withdrawal WHERE LocationID = %s", (location_id,))
        data = cursor.fetchall()
        cursor.close()
        db.close()

        for info in data:
            withdrawal_data.append(info)
    except mysql.connector.Error as err:
        print(f"Error getting withdrawal data: {err}")

    return withdrawal_data

def get_profit(location_id):
    try:
        db = create_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT Profit FROM Profit_And_Withdrawal WHERE LocationID = %s", (location_id,))
        data = cursor.fetchone()
        cursor.close()
        db.close()
        return data[0] if data else 0.0
    except mysql.connector.Error as err:
        print(f"Error getting profit: {err}")
        return 0.0

def insert_withdrawal(location_id, amount):
    try:
        db = create_db_connection()
        cursor = db.cursor()

        query = "INSERT INTO Withdrawal (Amount, LocationID) VALUES (%s, %s)"
        cursor.execute(query, (amount, location_id))

        db.commit()
        cursor.close()
        db.close()

        return True
    except mysql.connector.Error as err:
        print(f"Error inserting withdrawal: {err}")
        return False