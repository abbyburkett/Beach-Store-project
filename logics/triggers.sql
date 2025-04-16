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
        IF EXISTS (SELECT 1 FROM Employee WHERE EmployeeID = NEW.ManagerID) THEN
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
            WHERE EmployeeID = OLD.ManagerID;
        END IF;
    END IF;
END //

CREATE TRIGGER UpdateInvoicePaidStatus
BEFORE UPDATE ON Invoice
FOR EACH ROW
BEGIN
     IF NEW.AmountPaid >= OLD.AmountTotal THEN
        SET NEW.Paid = TRUE;
    ELSE
        SET NEW.Paid = FALSE;
    END IF;
END //


CREATE TRIGGER SetPaidOnInsert
BEFORE INSERT ON Invoice
FOR EACH ROW
BEGIN
     IF NEW.AmountPaid >= NEW.AmountTotal THEN
         SET NEW.Paid = TRUE;
     ELSE
         SET NEW.Paid = FALSE;
     END IF;
 END//

DELIMITER ;