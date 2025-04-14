import os
import mysql.connector
from dotenv import load_dotenv
from logics.dashboard_functions import hash_password

load_dotenv()

db_password = os.getenv('MYSQL_PASSWORD')

def check_credentials(username, password):

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