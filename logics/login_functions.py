def check_credentials(username, password, location):
    cursor.execute("SELECT * FROM Employee WHERE UserName = %s AND PinPassword = %s", (username, hashed_pw))
    user = cursor.fetchone()
    return True

