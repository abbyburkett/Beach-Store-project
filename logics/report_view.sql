Use BeachStore;

CREATE VIEW Daily_Report_By_Location AS
SELECT  
    p.Date,
    DAYNAME(p.Date) AS Day,
    p.LocationID,
    p.Cash,
    p.Credit,
    
    e.ExpenseType,
    e.Amount AS ExpenseValue,
    
    CASE 
        WHEN e.isMerchandise THEN e.ExpenseType ELSE NULL 
    END AS MerchandiseType,
    CASE 
        WHEN e.isMerchandise THEN e.Amount ELSE NULL
    END AS MerchandiseValue,
    
    CASE 
        WHEN DAYNAME(p.Date) = 'Sunday' THEN (
            SELECT SUM(ep.Base_Salary + ep.Bonus_Pay)
            FROM Employee_Pay ep
            JOIN Employee emp ON emp.EmployeeID = ep.EmployeeID
            WHERE 
                CONCAT(
                    DATE_FORMAT(DATE_SUB(p.Date, INTERVAL WEEKDAY(p.Date) DAY), '%b %d'),
                    ' - ',
                    DATE_FORMAT(DATE_ADD(p.Date, INTERVAL (6 - WEEKDAY(p.Date)) DAY), '%b %d')
                ) = ep.Week_Range
                AND ep.LocationID = p.LocationID 
        )
        ELSE NULL
    END AS Payroll

FROM Profit p
LEFT JOIN Expense e ON p.Date = e.Date AND p.LocationID = e.LocationID;