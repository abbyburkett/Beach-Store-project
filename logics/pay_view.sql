USE BeachStore;

CREATE OR REPLACE VIEW Employee_Pay AS
SELECT
    c.EmployeeID,
    CONCAT(
        DATE_FORMAT(DATE_SUB(c.ClockIn, INTERVAL WEEKDAY(c.ClockIn) DAY), '%Y-%b %d'),
        ' - ',
        DATE_FORMAT(DATE_ADD(c.ClockIn, INTERVAL (6 - WEEKDAY(c.ClockIn)) DAY), '%Y-%b %d')
    ) AS Week_Range,
    c.LocationID,
    SUM(TIMESTAMPDIFF(SECOND, c.ClockIn, c.ClockOut) / 3600.0 * pr.PayRate) AS Base_Salary,
    SUM(
        CASE WHEN c.AfterBal > c.BeforeBal 
             THEN (c.AfterBal - c.BeforeBal) * pr.PayBonus 
             ELSE 0 
        END
    ) AS Bonus_Pay
FROM ClockInOut c
JOIN PayRateBonusHistory pr
    ON c.EmployeeID = pr.EmployeeID
    AND pr.EffectiveDate <= c.ClockIn
    AND pr.EffectiveDate = (
        SELECT MAX(EffectiveDate) 
        FROM PayRateBonusHistory 
        WHERE EmployeeID = pr.EmployeeID AND EffectiveDate <= c.ClockIn
    )

GROUP BY 
    c.EmployeeID,
    c.LocationID,
    Week_Range;