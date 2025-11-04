--- ### Stored Procedures for Süsse Wurst database ###

-- functions
DROP FUNCTION IF EXISTS func_count_emp_by_state;

DELIMITER //

CREATE FUNCTION IF NOT EXISTS func_count_emp_by_state(state_param CHAR(2))
RETURNS INT
DETERMINISTIC
READS SQL DATA 
COMMENT 'This function counts all employees per state.'

BEGIN
 DECLARE total_emp_var INT;

 SELECT COUNT(*)
 INTO total_emp_var
 FROM employee
 WHERE emp_state = state_param;

 RETURN total_emp_var;
END//

DELIMITER ;

-- simple function: get current month
DROP FUNCTION IF EXISTS func_current_month;

DELIMITER //

CREATE FUNCTION IF NOT EXISTS func_current_month()
RETURNS TINYINT
DETERMINISTIC
READS SQL DATA
COMMENT 'Returns the current month numeral.'
BEGIN
	DECLARE month_var TINYINT;
    
    SELECT MONTH(CURRENT_DATE())
    INTO month_var;
    
    RETURN month_var;
END//

DELIMITER ;


-- simple function: get current day
DROP FUNCTION IF EXISTS func_current_day;

DELIMITER //

CREATE FUNCTION IF NOT EXISTS func_current_day()
RETURNS TINYINT
DETERMINISTIC
READS SQL DATA
COMMENT 'Returns the current day.'
BEGIN
	DECLARE day_var TINYINT;
    
    SELECT DAY(CURRENT_DATE())
    INTO day_var;
    
    RETURN day_var;
END//

DELIMITER ;



-- I'll use this function in my stores view
DROP FUNCTION IF EXISTS func_get_age;

DELIMITER //

CREATE FUNCTION IF NOT EXISTS func_get_age
(
	orig_date_param DATE
)
RETURNS VARCHAR(100)
NOT DETERMINISTIC 
READS SQL DATA
COMMENT 'This function subtracts a given date from the current date and returns the age in years, months, and days.'
BEGIN
	DECLARE years_var INT;
    DECLARE months_var TINYINT;
    DECLARE days_var TINYINT;
    
    SELECT FLOOR(PERIOD_DIFF(DATE_FORMAT(CURRENT_DATE(), '%Y%m'), DATE_FORMAT(orig_date_param, '%Y%m'))/12),
			     MOD(PERIOD_DIFF(DATE_FORMAT(CURRENT_DATE(), '%Y%m'), DATE_FORMAT(orig_date_param, '%Y%m')), 12),
                  DATEDIFF(DATE_ADD(orig_date_param, INTERVAL (PERIOD_DIFF(DATE_FORMAT(CURRENT_DATE(), '%Y%m'), DATE_FORMAT(orig_date_param, '%Y%m'))) MONTH),
									CURRENT_DATE())
	INTO years_var, months_var, days_var;
    
    RETURN CONCAT(years_var,' years ', months_var,' months ', days_var, ' days');
END//

DELIMITER ;







-- procedures
DROP PROCEDURE IF EXISTS sp_emp_by_state;
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_emp_by_state(IN state_param CHAR(2))
BEGIN
 DECLARE total_emp_var INT;

 SELECT CONCAT(emp_fname,' ',emp_lname) AS "Employee",
        emp_city
 FROM employee
 WHERE emp_state = state_param;

 IF state_param = 'AZ'
 THEN SELECT CONCAT(
       'You have ',
       func_count_emp_by_state(state_param),
       ' employees in Arizona.'
       ) AS "Employee Summary";
 ELSE SELECT CONCAT(
       'You have ',
       func_count_emp_by_state(state_param),
       ' employees in Nevada.'
       ) AS "Employee Summary";
 END IF;
END//

DELIMITER ;

-- get birthdays
DROP PROCEDURE IF EXISTS sp_get_monthly_birthdays;

DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_get_monthly_birthdays()
BEGIN
      SELECT CONCAT(e.emp_fname,' ',e.emp_lname) AS "EMPLOYEE",
             p.position_title AS "JOB TITLE",
             d.dept_name AS "DEPARTMENT",
             CONCAT(MONTH(e.emp_dob),'/',DAY(e.emp_dob)) AS "BIRTHDAY"
      FROM employee e
      JOIN active_employee a ON a.emp_id = e.emp_id 
      JOIN job_position p ON p.position_id = a.position_id
      JOIN department d ON d.dept_id = a.dept_id 
      WHERE MONTH(e.emp_dob) = func_current_month()
      ORDER BY DAY(e.emp_dob), e.emp_lname, e.emp_fname;
END//

DELIMITER ;

-- get today's birthdays
DROP PROCEDURE IF EXISTS sp_daily_birthdays;

DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_daily_birthdays()
BEGIN
      SELECT CONCAT(e.emp_fname,' ',e.emp_lname) AS "EMPLOYEE",
             p.position_title AS "JOB TITLE",
             d.dept_name AS "DEPARTMENT",
             CONCAT(MONTH(e.emp_dob),'/',DAY(e.emp_dob)) AS "BIRTHDAY"
      FROM employee e
      JOIN active_employee a ON a.emp_id = e.emp_id 
      JOIN job_position p ON p.position_id = a.position_id
      JOIN department d ON d.dept_id = a.dept_id 
      WHERE MONTH(e.emp_dob) = func_current_month() AND DAY(e.emp_dob) = func_current_day()
      ORDER BY DAY(e.emp_dob), e.emp_lname, e.emp_fname;
END//

DELIMITER ;



-- HR CRUD procedures

DROP PROCEDURE IF EXISTS sp_employee_insert;
DROP PROCEDURE IF EXISTS sp_emp_onboard;

DELIMITER //

-- INSERT INTO EMPLOYEE
CREATE PROCEDURE sp_employee_insert
(
	IN id_var INT,
    IN fname_var VARCHAR(75),
    IN lname_var VARCHAR(75),
    IN hiredate_var DATE,
    IN dob_var DATE,
    IN ssn_var CHAR(11),
    IN address_var VARCHAR(75),
    IN city_var VARCHAR(75),
    IN state_var CHAR(2),
    IN zip_var CHAR(5),
    IN phone_var CHAR(12),
    OUT emp_insert_msg BOOL
)
COMMENT 'This procedure inserts a new employee into the EMPLOYEE table.'

BEGIN
	DECLARE insert_error BOOL DEFAULT FALSE;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
		SET insert_error = TRUE;
    
        
	START TRANSACTION;
		INSERT INTO employee
        (emp_id, emp_fname, emp_lname, emp_hire_date, emp_dob, emp_ssn,
         emp_address, emp_city, emp_state, emp_zip, emp_phone)
		VALUES (id_var, fname_var, lname_var, hiredate_var, dob_var, ssn_var,
                       address_var, city_var, state_var, zip_var, phone_var);
		
        IF insert_error = FALSE THEN
			COMMIT;
            SET emp_insert_msg = TRUE;
		ELSE
			ROLLBACK;
            SET emp_insert_msg = FALSE;
		END IF;
END//

-- INSERT INTO ACTIVE EMPLOYEE
CREATE PROCEDURE IF NOT EXISTS sp_active_emp_insert
(
    IN empid_var INT, 
    IN jobid_var TINYINT,
    IN deptid_var TINYINT,
    IN empcomp_var DECIMAL(8,2),
    IN email_var VARCHAR(100),
    OUT active_emp_insert_msg BOOL 
)
COMMENT 'This procedure inserts a new employee into the ACTIVE_EMPLOYEE table.'

BEGIN
    DECLARE insert_error BOOL DEFAULT FALSE;

    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        SET insert_error = TRUE;

    START TRANSACTION;
        INSERT INTO active_employee
            (emp_id, position_id, dept_id, active_emp_comp, active_emp_email)
        VALUES (empid_var, jobid_var, deptid_var, empcomp_var, email_var);

        IF insert_error = FALSE THEN
			COMMIT;
            SET active_emp_insert_msg = TRUE;
		ELSE
			ROLLBACK;
            SET active_emp_insert_msg = FALSE;
		END IF;
END//


-- BUNDLED ONBOARDING PROCEDURE
CREATE PROCEDURE sp_emp_onboard
(
	IN id_var INT,
    IN fname_var VARCHAR(75),
    IN lname_var VARCHAR(75),
    IN hiredate_var DATE,
    IN dob_var DATE,
    IN ssn_var CHAR(11),
    IN address_var VARCHAR(75),
    IN city_var VARCHAR(75),
    IN state_var CHAR(2),
    IN zip_var CHAR(5),
    IN phone_var CHAR(12),
    IN jobid_var TINYINT,
    IN deptid_var TINYINT,
    IN empcomp_var DECIMAL(8,2),
    IN email_var VARCHAR(100)
)
COMMENT 'This procedure inserts a new employee into the EMPLOYEE and ACTIVE_EMPLOYEE tables.'

BEGIN
    CALL sp_employee_insert(
        id_var, fname_var, lname_var, hiredate_var, dob_var, ssn_var,
        address_var, city_var, state_var, zip_var, phone_var, @emp_insert_msg
    );
    
    IF @emp_insert_msg THEN
		CALL sp_active_emp_insert(id_var, jobid_var, deptid_var, empcomp_var, email_var, @active_emp_insert_msg);
        IF @active_emp_insert_msg THEN
			SELECT 'New employee onboarded successfully.' AS "MESSAGE";
		ELSE
			SELECT 'An error occurred. Active employees has not been updated.' AS "UPDATE";
		END IF;
	ELSE
		SELECT 'An error occurred. The transaction was not completed.' AS "UPDATE";
	END IF;
END//

DELIMITER ;


DELIMITER //
-- CREATE TRIGGER trig_insert_past_emp()
-- COMMENT 'This trigger updates the PAST_EMPLOYEE table when an employee is removed from the system.'

CREATE PROCEDURE IF NOT EXISTS sp_employee_delete
(
    IN id_var INT,
    OUT emp_delete_msg BOOL
)
COMMENT 'This procedure removes an employee from the ACTIVE_EMPLOYEE table.'

BEGIN
    DECLARE delete_error BOOL DEFAULT FALSE;

    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        SET delete_error = TRUE;
    
    START TRANSACTION;
        DELETE FROM active_employee 
        WHERE emp_id = id_var;

        IF delete_error = FALSE THEN
            COMMIT;
            SET emp_delete_msg = TRUE;
        ELSE
            ROLLBACK;
            SET emp_delete_msg = FALSE;
        END IF;  
END//

CREATE PROCEDURE IF NOT EXISTS sp_past_employee_insert
(
    IN id_var INT,
    IN jobid_var TINYINT,
    IN deptid_var TINYINT,
    IN term_date_var DATE,
    IN termid_var TINYINT,
    OUT past_insert_msg BOOL 
)
COMMENT 'This procedure adds recently removed employees to the PAST_EMPLOYEE table.'
BEGIN
    DECLARE insert_error BOOL DEFAULT FALSE;

    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        SET past_insert_msg = TRUE;
    
    START TRANSACTION;
        INSERT INTO past_employee
        (
            emp_id,
            position_id,
            dept_id,
            emp_term_date,
            term_type_code
        )
        VALUES 
        (
            id_var,
            jobid_var,
            deptid_var,
            term_date_var,
            termid_var
        );

        IF insert_error = FALSE THEN
            COMMIT;
            SET past_insert_msg = TRUE;
        ELSE
            ROLLBACK;
            SET past_insert_msg = FALSE;
        END IF;
END//

CREATE PROCEDURE IF NOT EXISTS sp_offboard_employee
(
    IN id_var INT,
    IN jobid_var TINYINT,
    IN deptid_var TINYINT,
    IN term_date_var DATE,
    IN termid_var TINYINT
)
COMMENT 'This procedure is used to offboard terminated employees.'
BEGIN
    DECLARE fname VARCHAR(75);
    DECLARE lname VARCHAR(75);
    DECLARE emp_full_name VARCHAR(200);


    -- get name of employee being offboarded
    SELECT emp_fname,
           emp_lname
    INTO fname,
         lname 
    FROM employee 
    WHERE emp_id = id_var;

    SET emp_full_name = CONCAT(lname,', ',fname);

    CALL sp_past_employee_insert
    (
        id_var,
        jobid_var,
        deptid_var,
        term_date_var,
        termid_var,
        @past_insert_msg
    )

    IF @past_insert_msg THEN
        CALL sp_employee_delete
        (
            id_var,
            @emp_delete_msg
        );

        IF @emp_delete_msg THEN
            SELECT CONCAT('Employee ', emp_full_name, ' has been offboarded.') AS "OFFBOARDING STATUS";
        ELSE
            SELECT 'There was an error. Deletion was not complete.' AS "OFFBOARDING STATUS";
        END IF;
    ELSE
        SELECT 'There was an error. Offboarding was not complete.' AS "OFFBOARDING STATUS";

END//

DELIMITER ;


-- UPDATE EMPLOYEE PROCEDURE
DROP PROCEDURE IF EXISTS sp_update_employee;

DELIMITER //

CREATE PROCEDURE IF NOT EXISTS sp_update_employee
(
    IN empid_var INT,
    IN column_name_var VARCHAR(25),
    IN update_string_var VARCHAR(75)
)
COMMENT 'Use this procedure to update employee data.'
BEGIN
	DECLARE update_error BOOL DEFAULT FALSE;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
		SET update_error = TRUE;
    
	SET @update_column = column_name_var;
    
    IF @update_column = 'emp_hire_date' OR @update_column = 'emp_dob' THEN
		SET update_string_var = CAST(update_string_var AS DATE);
	END IF;
    
    SET @update_query = CONCAT('UPDATE employee SET ', @update_column, ' = ? WHERE emp_id = ?');
	
    PREPARE update_stmt 
    FROM @update_query;
	
    SET @empid = empid_var;
	SET @update_value = update_string_var;
	
    START TRANSACTION;
		EXECUTE update_stmt 
		USING @update_value, @empid;
        
        IF update_error = FALSE THEN
			COMMIT;
			SELECT 'The employee data was updated successfully' AS "UPDATE STATUS";
            DEALLOCATE PREPARE update_stmt;     
		ELSE
			ROLLBACK;
            SELECT 'An error occurred, the update was not completed.' AS "UPDATE STATUS";
            DEALLOCATE PREPARE update_stmt;
		END IF;
END//

DELIMITER ;
