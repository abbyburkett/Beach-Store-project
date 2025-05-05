DELIMITER //

-- Transaction for creating a new employee and their initial pay rate history
CREATE PROCEDURE CreateEmployeeWithHistory(
    IN p_username VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_fname VARCHAR(255),
    IN p_lname VARCHAR(255),
    IN p_pay_rate DOUBLE,
    IN p_pay_bonus DOUBLE,
    IN p_role ENUM('Owner', 'Manager', 'Employee')
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error creating employee';
    END;

    START TRANSACTION;
    
    -- Insert new employee
    INSERT INTO Employee (UserName, PinPassword, FName, LName, PayRate, PayBonus, Role)
    VALUES (p_username, p_password, p_fname, p_lname, p_pay_rate, p_pay_bonus, p_role);
    
    -- Get the new employee ID
    SET @new_employee_id = LAST_INSERT_ID();
    
    -- Insert initial pay rate history
    INSERT INTO PayRateBonusHistory (EmployeeID, PayRate, PayBonus, EffectiveDate)
    VALUES (@new_employee_id, p_pay_rate, p_pay_bonus, NOW());
    
    COMMIT;
END //

-- Transaction for updating employee role and pay rate
CREATE PROCEDURE UpdateEmployeeRoleAndPay(
    IN p_employee_id INT,
    IN p_new_role ENUM('Owner', 'Manager', 'Employee'),
    IN p_new_pay_rate DOUBLE,
    IN p_new_pay_bonus DOUBLE
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error updating employee';
    END;

    START TRANSACTION;
    
    -- Update employee role and pay rate
    UPDATE Employee 
    SET Role = p_new_role,
        PayRate = p_new_pay_rate,
        PayBonus = p_new_pay_bonus
    WHERE EmployeeID = p_employee_id;
    
    -- Record the pay rate change in history
    INSERT INTO PayRateBonusHistory (EmployeeID, PayRate, PayBonus, EffectiveDate)
    VALUES (p_employee_id, p_new_pay_rate, p_new_pay_bonus, NOW());
    
    COMMIT;
END //

-- Transaction for handling location deletion and manager role update
CREATE PROCEDURE DeleteLocationAndUpdateManager(
    IN p_location_id INT
)
BEGIN
    DECLARE v_manager_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error deleting location';
    END;

    START TRANSACTION;
    
    -- Get the manager ID before deletion
    SELECT ManagerID INTO v_manager_id
    FROM Location
    WHERE LocationID = p_location_id;
    
    -- Soft delete the location
    UPDATE Location
    SET IsDeleted = TRUE
    WHERE LocationID = p_location_id;
    
    -- Check if manager has other locations
    IF NOT EXISTS (
        SELECT 1 
        FROM Location 
        WHERE ManagerID = v_manager_id 
        AND LocationID != p_location_id
        AND IsDeleted = FALSE
    ) THEN
        -- Update manager role to employee if they have no other locations
        UPDATE Employee
        SET Role = 'Employee'
        WHERE EmployeeID = v_manager_id 
        AND Role != 'Owner';
    END IF;
    
    COMMIT;
END //

-- Transaction for handling invoice payment and profit recording
CREATE PROCEDURE ProcessInvoicePayment(
    IN p_invoice_number INT,
    IN p_payment_amount DECIMAL(10,2),
    IN p_payment_way ENUM('Cash', 'Credit', 'Check'),
    IN p_location_id INT,
    IN p_employee_id INT
)
BEGIN
    DECLARE v_current_amount_paid DECIMAL(10,2);
    DECLARE v_total_amount DECIMAL(10,2);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error processing payment';
    END;

    START TRANSACTION;
    
    -- Get current payment status
    SELECT AmountPaid, AmountTotal 
    INTO v_current_amount_paid, v_total_amount
    FROM Invoice
    WHERE InvoiceNumber = p_invoice_number;
    
    -- Update invoice payment
    UPDATE Invoice
    SET AmountPaid = v_current_amount_paid + p_payment_amount,
        Paid = (v_current_amount_paid + p_payment_amount >= v_total_amount)
    WHERE InvoiceNumber = p_invoice_number;
    
    -- Record profit based on payment way
    IF p_payment_way = 'Cash' THEN
        INSERT INTO Profit (EmployeeID, Cash, Credit, Date, LocationID)
        VALUES (p_employee_id, p_payment_amount, 0, CURDATE(), p_location_id);
    ELSE
        INSERT INTO Profit (EmployeeID, Cash, Credit, Date, LocationID)
        VALUES (p_employee_id, 0, p_payment_amount, CURDATE(), p_location_id);
    END IF;
    
    COMMIT;
END //

-- Transaction for handling expense and profit adjustment
CREATE PROCEDURE RecordExpenseAndAdjustProfit(
    IN p_date DATE,
    IN p_location_id INT,
    IN p_amount DOUBLE,
    IN p_expense_type VARCHAR(255),
    IN p_is_merchandise BOOLEAN,
    IN p_merch_type VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error recording expense';
    END;

    START TRANSACTION;
    
    -- Insert expense
    INSERT INTO Expense (Date, LocationID, Amount, ExpenseType, isMerchandise, MerchType)
    VALUES (p_date, p_location_id, p_amount, p_expense_type, p_is_merchandise, p_merch_type);
    
    -- Adjust profit by reducing cash
    INSERT INTO Profit (EmployeeID, Cash, Credit, Date, LocationID)
    VALUES (NULL, -p_amount, 0, p_date, p_location_id);
    
    COMMIT;
END //

DELIMITER ;
