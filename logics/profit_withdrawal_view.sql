USE BeachStore;

CREATE OR REPLACE VIEW Profit_And_Withdrawal AS
SELECT
    dr.LocationID,
    COALESCE(dr.TotalRevenue - dr.TotalExpense - COALESCE(w.TotalWithdrawal, 0), 0) AS Profit
FROM (
    SELECT
        LocationID,
        SUM(DISTINCT (Cash + Credit)) AS TotalRevenue,
        SUM(COALESCE(ExpenseValue,0) + COALESCE(Payroll, 0)) AS TotalExpense
    FROM Daily_Report_By_Location
    GROUP BY Daily_Report_By_Location.LocationID, Daily_Report_By_Location.Date
) AS dr
LEFT JOIN (
    SELECT
        LocationID,
        SUM(Amount) AS TotalWithdrawal
    FROM Withdrawal
    GROUP BY LocationID
) AS w ON dr.LocationID = w.LocationID;
