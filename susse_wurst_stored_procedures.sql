#### Stored Routines for Susse Wurst database ###

-- functions
DROP FUNCTION IF EXISTS func_count_emp_by_state;

DELIMITER //

CREATE FUNCTION func_count_emp_by_state(state_param CHAR(2))
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

CREATE FUNCTION func_current_month()
RETURNS TINYINT
DETERMINISTIC
READS SQL DATA
COMMENT 'Returns the current month numeral.'
BEGIN
	DECLARE month_var TINYINT;
    
    SELECT MONTH(CURRENT_DATE)
    INTO month_var;
    
    RETURN month_var;
END//

DELIMITER ;


-- procedures
DROP PROCEDURE IF EXISTS sp_emp_by_state;
DELIMITER //

CREATE PROCEDURE sp_emp_by_state(IN state_param CHAR(2))
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