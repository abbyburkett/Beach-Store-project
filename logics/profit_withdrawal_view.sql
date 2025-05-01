USE BeachStore;

CREATE OR REPLACE VIEW Profit_And_Withdrawal AS
SELECT
    dr.LocationID,
    COALESCE(SUM(dr.TotalRevenue) - SUM(dr.TotalExpense) - COALESCE(SUM(w.TotalWithdrawal), 0), 0) AS Profit
FROM (
    SELECT
        dl.LocationID,
        (dl.Cash + dl.Credit) AS TotalRevenue,
        COALESCE(dl.ExpenseValue, 0) + COALESCE(dl.Payroll, 0) AS TotalExpense
    FROM Daily_Report_By_Location dl
) AS dr
LEFT JOIN (
    SELECT
        LocationID,
        SUM(Amount) AS TotalWithdrawal
    FROM Withdrawal
    GROUP BY LocationID
) AS w ON dr.LocationID = w.LocationID
GROUP BY dr.LocationID;
