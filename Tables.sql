CREATE DATABASE BeachStore;

Use BeachStore;
drop table if exists Employee;
CREATE TABLE if not exists Employee(
    EmployeeID int PRIMARY KEY NOT NULL,
    FName varchar(255),
    LName varchar(255),
    PinPassword varchar(255),3
    UserName varchar(255),
    Role enum('Owner','Manager','Employee')
);
drop table if exists Location;
CREATE TABLE if not exists Location(
    LocationID int PRIMARY KEY NOT NULL,
    Name varchar(255),
    Address varchar(255),
    ManagerID int,
    FOREIGN KEY (ManagerID) REFERENCES Employee(EmployeeID)
);

drop table if exists Pay;
Create TABLE if not exists Pay(
    PaidID int PRIMARY KEY NOT NULL,
    PayAmount double,
    EmployeeID int,
    BonusPercentage double,
    GrossBonus double,
    GrossPaid double,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

drop table if exists ClockInOut;
CREATE TABLE if not exists ClockInOut(
    Date date,
    EmployeeID int,
    ClockIn datetime,
    ClockOut datetime,
    PaidRate double,
    PaidID int,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (PaidID) REFERENCES Pay(PaidID)
);

drop table if exists Profit;
CREATE TABLE if not exists Profit(
    ProfitID int PRIMARY KEY,
    EmployeeID int,
    BeforeBal double,
    AfterBal double,
    Cash double,
    Credit double,
    GrossRevenue double,
    Date date,
    LocationID int,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

drop table if exists Expense;
CREATE TABLE if not exists Expense(
    ExpenseID int PRIMARY KEY,
    Date datetime,
    LocationID int,
    Amount double,
    isMerchandise boolean,
    MerchType varchar(255),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

drop table if exists Invoice;
CREATE TABLE if not exists Invoice(
    InvoiceNumber int PRIMARY KEY,
    PaidWay enum('Cash','Credit','Check'),
    AmountTotal double,
    AmountPaid double,
    Company varchar(255),
    DueDate datetime,
    Paid boolean,
    Date datetime
);

