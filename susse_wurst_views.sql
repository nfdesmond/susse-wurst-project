-- Süsse Wurst Views

-- birthdays
-- stores
-- employees by department

USE susse_wurst_hr;

SELECT func_current_day();
SELECT func_current_month();
SELECT func_current_year();

DELIMITER //
CREATE FUNCTION IF NOT EXISTS func_current_year()
RETURNS INT
DETERMINISTIC
READS SQL DATA
COMMENT 'This function returns the current year.'
BEGIN
	DECLARE current_year_var INT;
    SELECT YEAR(CURRENT_DATE())
    INTO current_year_var;
    
    RETURN current_year_var;
END//
DELIMITER ;

-- # ----------------- VIEWS ----------------- #

-- monthly birthday view
CREATE OR REPLACE VIEW view_monthly_birthdays AS
SELECT CONCAT(e.emp_lname,', ',e.emp_fname) AS "EMPLOYEE",
			  j.position_title AS "JOB TITLE",
             d.dept_name AS "DEPARTMENT",
             CONCAT(MONTH(e.emp_dob),'/',DAY(e.emp_dob)) AS "BIRTHDAY"
FROM employee e 
JOIN active_employee a ON a.emp_id = e.emp_id
JOIN department d ON a.dept_id = d.dept_id
JOIN job_position j ON a.position_id = j.position_id
WHERE MONTH(e.emp_dob) = func_current_month()
ORDER BY DAY(e.emp_dob), e.emp_lname, e.emp_fname;

SELECT *
FROM view_monthly_birthdays;

CALL sp_get_monthly_birthdays();

-- daily birthday view
CREATE OR REPLACE VIEW view_daily_birthdays AS
SELECT CONCAT(e.emp_lname,', ',e.emp_fname) AS "EMPLOYEE",
			  j.position_title AS "JOB TITLE",
             d.dept_name AS "DEPARTMENT",
             CONCAT(MONTH(e.emp_dob),'/',DAY(e.emp_dob)) AS "BIRTHDAY"
FROM employee e 
JOIN active_employee a ON a.emp_id = e.emp_id
JOIN department d ON a.dept_id = d.dept_id
JOIN job_position j ON a.position_id = j.position_id
WHERE CONCAT(MONTH(e.emp_dob),'/',DAY(e.emp_dob)) = CONCAT(func_current_month(),'/',func_current_day())
ORDER BY e.emp_lname, e.emp_fname;

SELECT *
FROM view_daily_birthdays;

-- current employees view
CREATE OR REPLACE VIEW view_active_employees AS
SELECT e.emp_id AS "EMP#",
			 e.emp_fname AS "EMP FNAME",
			 e.emp_lname AS "EMP LNAME",
             j.position_id AS "JOB ID",
             j.position_title AS "JOB TITLE",
             d.dept_id AS "DEPT#",
             d.dept_name AS "DEPT NAME"
FROM employee e
JOIN active_employee a ON a.emp_id = e.emp_id
JOIN department d ON a.dept_id = d.dept_id
JOIN job_position j ON j.position_id = a.position_id
ORDER BY e.emp_hire_date;

SELECT *
FROM view_active_employees;

-- management view
CREATE OR REPLACE VIEW view_sw_mgmt AS
SELECT d.dept_id AS "DEPT ID",
			 d.dept_name AS "DEPT NAME",
             a.emp_id "DEPT HEAD ID",
             CONCAT(e.emp_lname,', ',e.emp_fname) AS "DEPT HEAD/MANAGER",
             d.head_id AS "POSITION ID",
             j.position_title AS "MANAGER TITLE",
             a.active_emp_email AS "CONTACT"
FROM department d
JOIN active_employee a ON a.dept_id = d.dept_id
JOIN job_position j ON j.position_id = d.head_id
JOIN employee e ON (e.emp_id = a.emp_id AND a.position_id = d.head_id);

SELECT *
FROM view_sw_mgmt;


-- store view
CREATE OR REPLACE VIEW view_stores AS
SELECT l.loc_name AS "STORE NAME",
			 l.loc_id AS "STORE#",
             CONCAT(l.loc_address, ', ', l.loc_city,', ', l.loc_state,', ', l.loc_zip) AS "STORE ADDRESS",
             l.loc_phone AS "STORE PHONE",
             CONCAT(e.emp_fname,', ', e.emp_lname) AS "STORE MANAGER",
             CONCAT(ee.emp_fname,', ', ee.emp_lname) AS "ASST MANAGER",
             CONCAT(TIMESTAMPDIFF(YEAR, loc_start_date, CURRENT_DATE()),' years ',
							(TIMESTAMPDIFF(MONTH, loc_start_date, CURRENT_DATE()) - (TIMESTAMPDIFF(YEAR, loc_start_date, CURRENT_DATE()) * 12)), ' months ',
							(TIMESTAMPDIFF(DAY, loc_start_date, CURRENT_DATE()) - (TIMESTAMPDIFF(YEAR, loc_start_date, CURRENT_DATE()) * 365) -
							(TIMESTAMPDIFF(MONTH, loc_start_date, CURRENT_DATE()) - (TIMESTAMPDIFF(YEAR, loc_start_date, CURRENT_DATE()) * 12)) * 31), ' days'
) AS "STORE AGE"
FROM location l
JOIN department d ON d.loc_id = l.loc_id
JOIN active_employee a ON a.dept_id = d.dept_id
JOIN employee e ON e.emp_id = a.emp_id
JOIN active_employee aa ON aa.dept_id = d.dept_id
JOIN employee ee ON ee.emp_id = aa.emp_id
WHERE l.loc_id != 999 AND a.position_id = 38 AND aa.position_id = 39
ORDER BY l.loc_id;

SELECT *
FROM view_stores;