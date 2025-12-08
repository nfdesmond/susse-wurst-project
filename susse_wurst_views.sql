-- Süsse Wurst Views

-- HR
-- view monthly birthdays
-- view today's birthdays
-- view current employee roster
-- view managers and departments
-- view positions and departments
-- view stores
-- view employee count by state
-- view employee info

-- STORE
-- view active inventory
-- view ingredient purchasing invoices



-- HR VIEWS
-- monthly birthday view
DROP VIEW IF EXISTS view_monthly_birthdays;

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



-- daily birthday view
DROP VIEW IF EXISTS view_daily_birthdays;

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



-- current employees view
DROP VIEW IF EXISTS view_active_employees;

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



-- managers and departments
-- This view matches all managers with their respective departments. Some managers head a department. 
-- Some managers have managers that aren't in the same department as them. Some manager roles can be 
-- found in more than one department, as is the case with the various store departments. The view 
-- breaks down each manager/department scenario using a CTE, then combines them with UNION to form
-- a single result set. 

DROP VIEW IF EXISTS view_mgrs_and_depts;

CREATE OR REPLACE VIEW view_mgrs_and_depts AS
    WITH 
        -- find all managers who answer to the CSO or who are the CSO
        sw_csuite AS
            (SELECT position_id,
                    position_title,
                    head_id
            FROM job_position
            WHERE head_id = 1 OR head_id IS NULL),
        
        -- find all managers who answer to top managers
        middle_mgmt AS
            (SELECT position_id,
                    position_title,
                    head_id
            FROM job_position
            WHERE position_id IN (SELECT head_id
                                  FROM job_position
                                  WHERE head_id IS NOT NULL)
            AND position_id NOT IN (SELECT position_id
                                    FROM sw_csuite)),

        -- combine top managers and middle managers
        sw_mgmt AS
            (SELECT *
             FROM sw_csuite
             UNION
             SELECT *
             FROM middle_mgmt),

        -- match managers with explicit department connections
        mgr_with_dept AS
            (SELECT m.position_id,
                    m.position_title,
                    m.head_id,
                    d.dept_id,
                    d.dept_name
            FROM sw_mgmt m
            LEFT OUTER JOIN department d ON m.position_id = d.head_id
            WHERE d.dept_id IS NOT NULL),
            
        -- find managers with no explicit department connection
        mgr_no_dept AS
            (SELECT m.position_id,
                    m.position_title,
                    m.head_id,
                    d.dept_id,
                    d.dept_name
            FROM sw_mgmt m
            LEFT OUTER JOIN department d ON m.position_id = d.head_id
            WHERE d.dept_id IS NULL),
        
        -- connect unmatched managers to the departments of their managers
        matched_mgrs AS
            (SELECT m.position_id,
                    m.position_title,
                    d.dept_id,
                    d.dept_name
            FROM mgr_no_dept m
            LEFT OUTER JOIN department d ON d.head_id = m.head_id
            WHERE d.dept_id IS NOT NULL),

        -- managers who have unmatched managers (who are now matched using matched_mgrs CTE)
        final_mgrs AS
            (SELECT m.position_id,
                    m.position_title,
                    m.head_id,
                    d.dept_id,
                    d.dept_name
            FROM mgr_no_dept m
            LEFT OUTER JOIN department d ON d.head_id = m.head_id
            WHERE d.dept_id IS NULL),

        -- managers now matched to the departments of their previously unmatched managers
        matched_final_mgrs AS
            (SELECT m.position_id,
                    m.position_title,
                    n.dept_id,
                    n.dept_name
            FROM final_mgrs m
            JOIN matched_mgrs n ON m.head_id = n.position_id)

        -- combine it all using UNION
    SELECT position_id, position_title, dept_id, dept_name FROM mgr_with_dept
    UNION
    SELECT * FROM matched_mgrs
    UNION
    SELECT * FROM matched_final_mgrs
    ORDER BY position_id;



-- job positions and their departments
DROP VIEW IF EXISTS view_jobs_and_depts;

CREATE OR REPLACE VIEW view_jobs_and_depts AS
    SELECT p.position_id,
           p.position_title,
           v.dept_id,
           v.dept_name
    FROM job_position p 
    JOIN view_mgrs_and_depts v ON p.head_id = v.position_id
    WHERE p.position_id NOT IN (SELECT position_id
                                FROM view_mgrs_and_depts)
    UNION
    SELECT *
    FROM view_mgrs_and_depts
    ORDER BY position_id;



-- store view
DROP VIEW IF EXISTS view_stores;

CREATE OR REPLACE VIEW view_stores AS
    SELECT l.loc_name AS "store_name",
           l.loc_id AS "store_num",
           CONCAT(l.loc_address, ', ', l.loc_city,', ', l.loc_state,', ', l.loc_zip) AS "store_address",
           l.loc_phone AS "store_phone",
           CONCAT(e.emp_fname,' ', e.emp_lname) AS "store_manager",
           a.active_emp_email AS "mgr_email",
           CONCAT(ee.emp_fname,' ', ee.emp_lname) AS "asst_manager",
           aa.active_emp_email AS "asst_mgr_email",
           DATE_FORMAT(l.loc_start_date,'%m/%d/%Y') AS "store_start_date",
           func_get_age(l.loc_start_date) AS "store_age"
    FROM location l
    JOIN department d ON d.loc_id = l.loc_id
    JOIN active_employee a ON a.dept_id = d.dept_id
    JOIN employee e ON e.emp_id = a.emp_id
    JOIN active_employee aa ON aa.dept_id = d.dept_id
    JOIN employee ee ON ee.emp_id = aa.emp_id
    WHERE l.loc_id != 999 AND a.position_id = 38 AND aa.position_id = 39
    ORDER BY l.loc_id;



-- view employee count by state
DROP VIEW IF EXISTS view_state_emp_count;

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




-- view employee info
DROP VIEW IF EXISTS view_emp_info;

CREATE OR REPLACE VIEW view_emp_info AS
	SELECT e.emp_id,
		   CONCAT(e.emp_fname,' ', e.emp_lname) AS "emp_name",
		   d.dept_name,
		   j.position_title,
		   func_emp_mgr(e.emp_id) AS "mgr_name",
		   func_get_age(e.emp_hire_date) AS "length_of_hire"		
	FROM employee e
	JOIN active_employee a ON e.emp_id = a.emp_id
	JOIN department d ON d.dept_id = a.dept_id
	JOIN job_position j ON j.position_id = a.position_id
    ORDER BY e.emp_hire_date;



-- STORE VIEWS

-- view active inventory
-- view ingredient purchasing invoices

DROP VIEW IF EXISTS view_active_inventory;

CREATE OR REPLACE VIEW view_active_inventory AS
SELECT a.active_id AS "inventory_id",
			 i.inventory_item_name AS "item_name",
             pt.product_type_name AS "product_type",
             CONCAT(i.package_size_oz, ' ', 'oz') AS "package_size",
             mat.material_name AS "package_material",
             pck.package_type_name AS "package_type",
             manu.manu_name AS "manufacturer",
             c.common_country_name AS "country",
             i.upc AS "upc",
             a.sku AS "sku"
FROM active_inventory a 
JOIN inventory i ON a.active_id = i.inventory_id
JOIN product_type pt ON i.product_type_id = pt.product_type_id
JOIN package_type pck ON i.package_type_id = pck.package_type_id
JOIN package_material mat ON i.material_id = mat.material_id
JOIN manufacturer manu ON i.manu_id = manu.manu_id
JOIN country c ON c.country_id = manu.country_id
ORDER BY a.active_id;



DROP VIEW IF EXISTS view_ingredient_invoice;

CREATE OR REPLACE VIEW view_ingredient_invoice AS
SELECT soi.order_id AS "order_id",
			 sw_hr.e.emp_fname AS "emp_first_name",
             sw_hr.e.emp_lname AS "emp_last_name",
             sw_hr.d.dept_name AS "department", 
             ing.store_ingred_name AS "ingredient",
             v.vendor_name AS "vendor",
             io.order_date AS "timestamp",
             soi.item_quantity AS "quantity",
             soi.vendor_price AS "vendor_price",
             soi.item_quantity * soi.vendor_price AS "total_purchase"
FROM inventory_order io
JOIN store_order_item soi ON io.order_id = soi.order_id
JOIN sw_hr.employee e ON io.emp_id = e.emp_id
JOIN sw_hr.department d ON io.dept_id = d.dept_id
JOIN store_ingredient ing ON soi.store_ingred_id = ing.store_ingred_id
JOIN vendor v ON v.vendor_id = soi.vendor_id;