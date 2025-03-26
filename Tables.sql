CREATE DATABASE IF NOT EXISTS BeachStore;

USE BeachStore;

DROP TABLE IF EXISTS Employee;
CREATE TABLE IF NOT EXISTS Employee (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    FName VARCHAR(255),
    LName VARCHAR(255),
    PinPassword VARCHAR(255) UNIQUE,
    UserName VARCHAR(255) UNIQUE,
    Role ENUM('Owner', 'Manager', 'Employee')
);

DROP TABLE IF EXISTS Location;
CREATE TABLE IF NOT EXISTS Location (
    LocationID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Address VARCHAR(255),
    ManagerID INT,
    FOREIGN KEY (ManagerID) REFERENCES Employee(EmployeeID)
);

DROP TABLE IF EXISTS Pay;
CREATE TABLE IF NOT EXISTS Pay (
    PaidID INT PRIMARY KEY AUTO_INCREMENT,
    PayAmount DOUBLE,
    EmployeeID INT,
    BonusPercentage DOUBLE,
    GrossBonus DOUBLE,
    GrossPaid DOUBLE,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

DROP TABLE IF EXISTS ClockInOut;
CREATE TABLE IF NOT EXISTS ClockInOut (
    Date DATE,
    EmployeeID INT,
    ClockIn DATETIME,
    ClockOut DATETIME,
    PaidRate DOUBLE,
    PaidID INT,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (PaidID) REFERENCES Pay(PaidID)
);

DROP TABLE IF EXISTS Profit;
CREATE TABLE IF NOT EXISTS Profit (
    ProfitID INT PRIMARY KEY AUTO_INCREMENT,
    EmployeeID INT,
    BeforeBal DOUBLE,
    AfterBal DOUBLE,
    Cash DOUBLE,
    Credit DOUBLE,
    GrossRevenue DOUBLE,
    Date DATE,
    LocationID INT,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

DROP TABLE IF EXISTS Expense;
CREATE TABLE IF NOT EXISTS Expense (
    ExpenseID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATETIME,
    LocationID INT,
    Amount DOUBLE,
    isMerchandise BOOLEAN,
    MerchType VARCHAR(255),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

DROP TABLE IF EXISTS Invoice;
CREATE TABLE IF NOT EXISTS Invoice (
    InvoiceNumber INT PRIMARY KEY AUTO_INCREMENT,
    PaidWay ENUM('Cash', 'Credit', 'Check'),
    AmountTotal DOUBLE,
    AmountPaid DOUBLE,
    Company VARCHAR(255),
    DueDate DATETIME,
    Paid BOOLEAN,
    Date DATETIME
);