# Beach-Store-project
A dashboard system application that uses GUI to manage and monitor employee performance, daily and monthly sales, expenses, and payroll at the Aloha Beach Store in Clearwater, FL and other locations. This was built by using Python, Tkinter, and MySQL.

---
## Features
- **Employee login** with shift tracking (clock in/out)
- **Manager Dashboard**: View reports for daily profit, expenses, payroll, and merchandise (limited to current month)
- **Owner Dashboard**: Access to every monthly performance history with dropdown filters
- **Clean and intuitive GUI** using Tkinter
- **Real-time MySQL integration** for dynamic data updates

---
### How To Use

1. **Clone the repository**:
    ```bash
    git clone https://github.com/abbyburkett/Beach-Store-project.git
    cd Beach-Store-project
    ```
    
2. **Install required Python packages**:
   ```bash
   pip install mysql-connector-python
   ```
   
3. **Set up the `.env` file**:
    - In the root directory, create a file named `.env`:
      ```bash
      MYSQL_PASSWORD="REPLACE_WITH_YOUR_MYSQL_PASSWORD"
      ```

4. **Run the app**:
    ```bash
    python app.py
    ```

5. **Login credentials** (for testing/demo):
    - **Employee**:  
      `Username: Employee`  
      `Password: 123`
    - **Manager**:  
      `Username: Manager`  
      `Password: 456`
    - **Owner**:  
      `Username: Owner`  
      `Password: 789`

---
## Database Setup

Make sure your MySQL server is running and that the following tables are created:
- `Employee`
- `Location`
- `ClockInOut`
- `Profit`
- `Expense`
- `Invoice`
- `Withdrawal`
- `PayRateBonusHistory`

Update your database connection parameters in the code to match your MySQL configuration.

---

## Contributors
- Hien Tran
- Abby Burkett
- Maya Schroeder

---
##  License

This project is licensed under the MIT License. See the LICENSE file for more details.
