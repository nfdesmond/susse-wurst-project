import sw_db_application.serverconnect.mysqlconnect as mysqlconnect


class SusseWurstConnect(mysqlconnect.MySQLDatabaseConnect):
    def __init__(self, db_name):
        super().__init__(db_name)
        
    def get_employee_info(employee_id, cxn):
        cursor = cxn.cursor()
        
        query_params = (employee_id,)
        
        query = (
            """
            SELECT emp_name,
                   dept_name,
                   position_title,
                   mgr_name,
                   length_of_hire
            FROM view_emp_info
            WHERE emp_id = %s;
            """
        )
        
        cursor.execute(query, params=query_params)
        
        result = cursor.fetchall()

        cursor.close()
        
        return result 



