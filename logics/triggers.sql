CREATE TRIGGER ChangeEmployeeAfterLocationDel
AFTER DELETE ON Location
FOR EACH ROW
BEGIN
    UPDATE Employee
    SET Role = 'Employee'
    WHERE EmployeeID = OLD.ManagerID;
END;