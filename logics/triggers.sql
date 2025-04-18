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

CREATE TRIGGER CheckingOwnerBeforeDel
BEFORE DELETE ON Employee
FOR EACH ROW
BEGIN
    DECLARE owner_count INT;

    SELECT COUNT(*) INTO owner_count FROM Employee WHERE Role = 'Owner';

    IF OLD.Role = 'Owner' AND owner_count = 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete the last Owner account.';
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