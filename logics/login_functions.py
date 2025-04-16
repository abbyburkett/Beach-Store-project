import os
import mysql.connector
from logics.dashboard_functions import hash_password

def check_credentials(username, password):

    db_password = os.getenv('MYSQL_PASSWORD')

    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password=db_password,
            database='BeachStore',
        )
        cursor = db.cursor()

        hashed_pw = hash_password(password)

        cursor.execute("SELECT * FROM Employee WHERE UserName = %s AND PinPassword = %s", (username, hashed_pw))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            user_id = user[0]
            user_role = user[7]  # Index 5 corresponds to the 'Role' field in the query result
            print(f"Login successful. User role: {user_role}")
            return True, user_id, user_role
        else:
            print("Invalid credentials")
            return False, None, None

    except mysql.connector.Error as err:
        print(f"Erro in login functions.pyr: {err}")
        return False, None, None


def get_location_list():

    db_password = os.getenv('MYSQL_PASSWORD')

    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password=db_password,
            database='BeachStore',
        )
        cursor = db.cursor()

        cursor.execute("SELECT LocationID, Name FROM Location")
        location_list = cursor.fetchall()
        cursor.close()
        db.close()
        
        return location_list

    except mysql.connector.Error as err:
        print(f"Erro in login functions.py: {err}")
        return False