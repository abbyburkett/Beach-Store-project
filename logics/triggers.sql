DELIMITER //

CREATE TRIGGER ChangeEmployeeAfterLocationDel
AFTER DELETE ON Location
FOR EACH ROW
BEGIN
    UPDATE Employee
    SET Role = 'Employee'
    WHERE EmployeeID = OLD.ManagerID;
END //

CREATE TRIGGER UpdateManagerRoleOnLocationUpdate
BEFORE UPDATE ON Location
FOR EACH ROW
BEGIN
    IF NEW.ManagerID != OLD.ManagerID THEN
        IF EXISTS (SELECT 1 FROM Employee WHERE (EmployeeID = NEW.ManagerID AND Role != "Owner")) THEN
            UPDATE Employee
            SET Role = 'Manager'
            WHERE EmployeeID = NEW.ManagerID;
        END IF;

        IF NOT EXISTS (
            SELECT 1 FROM Location
            WHERE ManagerID = OLD.ManagerID AND LocationID != OLD.LocationID
        ) THEN
            UPDATE Employee
            SET Role = 'Employee'
            WHERE EmployeeID = OLD.ManagerID AND Role != "Owner";
        END IF;
    END IF;
END //

DELIMITER ;