-- Süsse Wurst Views

-- view monthly birthdays
-- view today's birthdays
-- view current employee roster
-- view current management
-- view stores
-- view employee count by state
-- view employee info


-- monthly birthday view
CREATE OR REPLACE VIEW view_monthly_birthdays AS
SELECT CONCAT(e.emp_lname,', ',e.emp_fname) AS "EMPLOYEE",
			  j.position_title AS "JOB_TITLE",
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

-- daily birthday view
CREATE OR REPLACE VIEW view_daily_birthdays AS
SELECT CONCAT(e.emp_lname,', ',e.emp_fname) AS "EMPLOYEE",
			  j.position_title AS "JOB_TITLE",
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
SELECT e.emp_id AS "EMP_ID",
			 e.emp_fname AS "EMP_FNAME",
			 e.emp_lname AS "EMP_LNAME",
             j.position_id AS "JOB_ID",
             j.position_title AS "JOB_TITLE",
             d.dept_id AS "DEPT_ID",
             d.dept_name AS "DEPT_NAME"
FROM employee e
JOIN active_employee a ON a.emp_id = e.emp_id
JOIN department d ON a.dept_id = d.dept_id
JOIN job_position j ON j.position_id = a.position_id
ORDER BY e.emp_hire_date;

SELECT *
FROM view_active_employees;

-- management view
CREATE OR REPLACE VIEW view_sw_mgmt AS
SELECT d.dept_id AS "DEPT_ID",
			 d.dept_name AS "DEPT_NAME",
             a.emp_id "DEPT_HEAD_ID",
             CONCAT(e.emp_lname,', ',e.emp_fname) AS "DEPT_HEAD",
             d.head_id AS "POSITION_ID",
             j.position_title AS "MGR_TITLE",
             a.active_emp_email AS "CONTACT"
FROM department d
JOIN active_employee a ON a.dept_id = d.dept_id
JOIN job_position j ON j.position_id = d.head_id
JOIN employee e ON (e.emp_id = a.emp_id AND a.position_id = d.head_id);

SELECT *
FROM view_sw_mgmt;


-- store view
CREATE OR REPLACE VIEW view_stores AS
SELECT l.loc_name AS "STORE_NAME",
			 l.loc_id AS "STORE_NUM",
             CONCAT(l.loc_address, ', ', l.loc_city,', ', l.loc_state,', ', l.loc_zip) AS "STORE_ADDRESS",
             l.loc_phone AS "STORE_PHONE",
             CONCAT(e.emp_fname,', ', e.emp_lname) AS "STORE_MANAGER",
             CONCAT(ee.emp_fname,', ', ee.emp_lname) AS "ASST_MANAGER",
             func_get_age(l.loc_start_date) AS "STORE_AGE"
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

-- view employee count by state
CREATE OR REPLACE VIEW view_state_emp_count AS 
SELECT CASE
				WHEN e.emp_state = 'AZ' THEN 'Arizona'
                WHEN e.emp_state = 'NV' THEN 'Nevada'
			 END AS "STATE",
             COUNT(*) AS "EMPLOYEE_COUNT"
FROM employee e 
JOIN active_employee a ON a.emp_id = e.emp_id
GROUP BY e.emp_state
ORDER BY e.emp_state;

SELECT *
FROM view_state_emp_count;

