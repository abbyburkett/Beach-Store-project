USE BeachStore;

CREATE VIEW Employee_Pay AS
SELECT
    c.EmployeeID,
    CONCAT(
        DATE_FORMAT(DATE_SUB(c.ClockIn, INTERVAL WEEKDAY(c.ClockIn) DAY), '%b %d'),
        ' - ',
        DATE_FORMAT(DATE_ADD(c.ClockIn, INTERVAL (6 - WEEKDAY(c.ClockIn)) DAY), '%b %d')
    ) AS Week_Range,
    c.LocationID,
    SUM(TIMESTAMPDIFF(SECOND, c.ClockIn, c.ClockOut) / 3600.0 * e.PayRate) AS Base_Salary,
    SUM(
        CASE WHEN c.AfterBal > c.BeforeBal 
             THEN (c.AfterBal - c.BeforeBal) * e.PayBonus 
             ELSE 0 
        END
    ) AS Bonus_Pay
FROM ClockInOut c
JOIN Employee e ON c.EmployeeID = e.EmployeeID
GROUP BY 
    e.EmployeeID,
    c.LocationID,
    Week_Range;