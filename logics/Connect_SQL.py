import mysql.connector
import os
from logics.dashboard_functions import hash_password

FILEPATH = "../Tables.sql"

TRIGGERPATH = "logics/triggers.sql"

PAYVIEWPATH = "logics/pay_view.sql"

REPORTPATH = "logics/report_view.sql"

def run_sql_file(file_path = FILEPATH):
    try:
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

        cursor.execute("SHOW DATABASES LIKE 'BeachStore'")
        result = cursor.fetchone()

        if not result:
            cursor.execute("CREATE DATABASE BeachStore")
            print("Database 'BeachStore' created.")
        else:
            print("Database 'BeachStore' already exists.")

        cursor.execute("USE BeachStore")

        with open(file_path, 'r') as file:
            sql_commands = file.read()

        for command in sql_commands.split(';'):
            if command.strip():
                cursor.execute(command)

        db.commit()
        print("Table SQL file executed successfully.")

        # reading the trigger SQL
        with open(TRIGGERPATH, 'r') as file:
            trigger_sql = file.read()

        cleaned_sql = []
        for line in trigger_sql.splitlines():
            if not line.strip().upper().startswith('DELIMITER'):
                cleaned_sql.append(line)
        trigger_sql = "\n".join(cleaned_sql)

        for statement in trigger_sql.split('//'):
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except mysql.connector.Error as e:
                    print(f"Error executing trigger: {e}")
        
        # reading the pay view SQL
        with open(PAYVIEWPATH, 'r') as file:
            pay_view_sql = file.read()

        statements = [stmt.strip() for stmt in pay_view_sql.split(';') if stmt.strip()]

        for stmt in statements:
            try:
                cursor.execute(stmt)
            except mysql.connector.Error as e:
                print(f"Error executing statement: {e}\nStatement: {stmt}")

        # reading the report view SQL
        with open(REPORTPATH, 'r') as file:
            pay_view_sql = file.read()

        statements = [stmt.strip() for stmt in pay_view_sql.split(';') if stmt.strip()]

        for stmt in statements:
            try:
                cursor.execute(stmt)
            except mysql.connector.Error as e:
                print(f"Error executing statement: {e}\nStatement: {stmt}")


        # Insert default users (Employee, Manager, Owner) if they don't already exist
        cursor.execute("SELECT COUNT(*) FROM Employee WHERE Role = 'Employee'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Employee (UserName, PinPassword, FName, LName, Role, PayRate, PayBonus) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                        ('Employee', hash_password("123"), "Emp", "loyee", 'Employee', 15.00, 10.00))

        cursor.execute("SELECT COUNT(*) FROM Employee WHERE Role = 'Manager'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Employee (UserName, PinPassword, FName, LName, Role, PayRate, PayBonus) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                        ('Manager', hash_password("456"), "Mana", "ger", 'Manager', 20.00, 10.00))

        cursor.execute("SELECT COUNT(*) FROM Employee WHERE Role = 'Owner'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Employee (UserName, PinPassword, FName, LName, Role, PayRate, PayBonus) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                        ('Owner', hash_password("789"), "Own", "er", 'Owner', 30.00, 10.00))
            
        # # Insert default location if it doesn't already exist
        cursor.execute("SELECT COUNT(*) FROM Location WHERE IsDeleted = FALSE")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO Location (Name, Address, ManagerID)
                VALUES (%s, %s, %s)
            """, ("Aloha", "123 dfsadk sadjasnd", 2))

        db.commit()
        
        print("Default users inserted successfully.")

        # Close the cursor and database connection
        cursor.close()
        db.close()

    except mysql.connector.Error as e:
        print(f"Error: {e}")
