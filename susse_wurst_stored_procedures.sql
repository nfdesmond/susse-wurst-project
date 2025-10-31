#### Stored Routines for Susse Wurst database ###

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

    CALL sp_active_emp_insert(
        id_var, jobid_var, deptid_var, empcomp_var, email_var, @active_emp_insert_msg
    );

    IF @emp_insert_msg = TRUE AND @active_emp_insert_msg THEN
        SELECT 'New employee onboarded successfully.' AS "MESSAGE";
    ELSE
        SELECT 'An error occurred. The transaction was not completed.' AS "UPDATE";
	END IF;
END//

DELIMITER ;