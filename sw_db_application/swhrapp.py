import sussewurstconnect.swconnect as swconnect
import sussewurstconnect.swconfig as swconfig

hr_app = swconnect.SusseWurstConnect('susse_wurst_hr')

hr_cxn = hr_app.mysql_connect(swconfig.USER, swconfig.PSWD)

if hr_app.cxn_test(hr_cxn):
    hr_cursor = hr_cxn.cursor()
    
    emp_query = (
        """
        SELECT CONCAT(emp_fname,' ', emp_lname) AS "EMPLOYEE_NAME",
               DATE_FORMAT(emp_hire_date, '%b %e, %Y') AS "HIRE_DATE"
        FROM employee
        WHERE YEAR(emp_hire_date) = 2019
        ORDER BY emp_hire_date, emp_lname; 
        """
    )
    
    result = hr_cxn.cmd_query(emp_query)
    employees, eof = hr_cxn.get_rows()
    
    for employee in employees:
        print(employee[0], employee[1])

    # emp_2019_roster = hr_app.execute_query(hr_cursor, emp_query)
    
    # for name, hire_date in emp_2019_roster:
    #     print(name, hire_date)
    
hr_cxn.close()

if hr_app.cxn_test(hr_cxn):
    print('Still alive!')
else:
    print('The connection has been closed.')