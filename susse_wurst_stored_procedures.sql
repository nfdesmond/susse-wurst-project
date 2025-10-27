#### Stored Routines for Susse Wurst database ###

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