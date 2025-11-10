import sw_db_application.sussewurstconnect.swconnect as swconnect
import sw_db_application.sussewurstconnect.swconfig as swconfig

hr_app = swconnect.SusseWurstConnect('susse_wurst_hr')

hr_cxn = hr_app.mysql_connect(swconfig.USER, swconfig.PSWD, use_pure_flag=True)

if hr_app.cxn_test(hr_cxn):
    hr_cursor = hr_cxn.cursor()
    
    # tesing stored procedure call using python
    params = (999666, 'Nicole', 'Desmond', '2025-10-31', '1984-12-24', '555-55-1111',
              '10854 N 60th Ave', 'Glendale', 'AZ', '85304', '480-555-5555',
              14, 2, 70000.00, 'ndesmond@sussewurst.com', 0)
    
    result_args = hr_cursor.callproc('sp_emp_onboard', params)
    print(result_args[15])
    # sql = """
    #       SELECT e.emp_fname,
    #              e.emp_lname,
    #              CONCAT(e.emp_city,', ', e.emp_state,' ', e.emp_zip) AS "emp_address"
    #       FROM employee e
    #       WHERE e.emp_id = 999666;
    #       """
          
    # hr_cursor.execute(sql)
    # result_set = hr_cursor.fetchall()
    # print(hr_cursor.column_names[0],' ', hr_cursor.column_names[1],' ', hr_cursor.column_names[2])
    # for item in result_set:
    #     print(item[0],' ', item[1],' ', item[2])
    
    hr_cursor.close()
    

hr_cxn.close()

if hr_app.cxn_test(hr_cxn):
    print('Still alive!')
else:
    print('The connection has been closed.')



