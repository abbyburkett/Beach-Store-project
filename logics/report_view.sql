USE BeachStore;

CREATE OR REPLACE VIEW Daily_Report_By_Location AS
WITH RECURSIVE calendar AS (
    SELECT MIN(DATE_FORMAT(Date, '%Y-%m-01')) AS Date
    FROM Profit
    UNION ALL
    SELECT DATE_ADD(Date, INTERVAL 1 DAY)
    FROM calendar
    WHERE Date < LAST_DAY((SELECT MAX(Date) FROM Profit))
),
date_location AS (
    SELECT 
        c.Date,
        l.LocationID
    FROM calendar c
    CROSS JOIN (SELECT LocationID FROM Location WHERE IsDeleted = FALSE) l
),
payroll_data AS (
    SELECT 
        ep.EmployeeID,
        ep.Week_Range,
        ep.LocationID,
        (ep.Base_Salary + ep.Bonus_Pay) AS TotalPay
    FROM Employee_Pay ep
)
SELECT  
    dl.Date,
    DAYNAME(dl.Date) AS Day,
    dl.LocationID,
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

    IF(
        DAYNAME(dl.Date) = 'Sunday',
        (
            SELECT SUM(TotalPay)
            FROM payroll_data pd
            WHERE pd.LocationID = dl.LocationID
            AND pd.Week_Range = CONCAT(
                DATE_FORMAT(DATE_SUB(dl.Date, INTERVAL WEEKDAY(dl.Date) DAY), '%Y-%b %d'),
                ' - ',
                DATE_FORMAT(DATE_ADD(dl.Date, INTERVAL (6 - WEEKDAY(dl.Date)) DAY),'%Y-%b %d')
            )
        ), NULL) AS Payroll

FROM date_location dl
LEFT JOIN Profit p ON p.Date = dl.Date AND p.LocationID = dl.LocationID
LEFT JOIN Expense e ON e.Date = dl.Date AND e.LocationID = dl.LocationID;
