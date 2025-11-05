import sussewurstconnect.swconnect as swconnect
import sussewurstconnect.swconfig as swconfig

hr_app = swconnect.SusseWurstConnect('susse_wurst_hr')

hr_cxn = hr_app.mysql_connect(swconfig.USER, swconfig.PSWD)


if hr_app.cxn_test(hr_cxn):
    print(hr_cxn.connection_id)
    
    hr_cursor = hr_cxn.cursor()
    
    sql_stmt1 = """SELECT USER();"""
    
    sql_stmt2 = """SELECT DATABASE();"""
    
    query_result1 = hr_app.execute_query(hr_cursor, sql_stmt1)
    query_result2 = hr_app.execute_query(hr_cursor, sql_stmt2)
    
    print(type(query_result1))
    
    for user in query_result1:
        print(user[0])
    
    for db in query_result2:
        print(db[0])
        
    emp_query = (
        """
        SELECT CONCAT(emp_fname,' ', emp_lname),
               DATE_FORMAT(emp_hire_date, '%b %e, %Y')
        FROM employee
        WHERE YEAR(emp_hire_date) = 2019
        ORDER BY emp_hire_date, emp_lname; 
        """
    )
    
    emp_2019_roster = hr_app.execute_query(hr_cursor, emp_query)
    
    for name, hire_date in emp_2019_roster:
        print(name, hire_date)
    
hr_cxn.close()

if hr_app.cxn_test(hr_cxn):
    print('Still alive!')
else:
    print('The connection has been closed.')