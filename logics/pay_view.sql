CREATE VIEW Employee_Pay AS
SELECT
    c.EmployeeID,
    CONCAT(
        DATE_FORMAT(DATE_SUB(c.ClockIn, INTERVAL WEEKDAY(c.ClockIn) DAY), '%b %d'),
        ' - ',
        DATE_FORMAT(DATE_ADD(c.ClockIn, INTERVAL (6 - WEEKDAY(c.ClockIn)) DAY), '%b %d')
    ) AS Week_Range,
    SUM(TIMESTAMPDIFF(SECOND, c.ClockIn, c.ClockOut) / 3600.0 * e.PayRate) AS Base_Salary,
    SUM((c.AfterBal - c.BeforeBal)) * e.PayBonus AS Bonus_Pay
FROM ClockInOut c
JOIN Employee e ON c.EmployeeID = e.EmployeeID
GROUP BY 
    e.EmployeeID,
    Week_Range;
