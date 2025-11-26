import susse_wurst_project.susse_wurst_hr_gui.serverconnect.mysqlconnect as mysqlconnect


class SusseWurstConnect(mysqlconnect.MySQLDatabaseConnect):
    def __init__(self, db_name):
        super().__init__(db_name)
        
    def get_employee_info(employee_id, cxn):
        cursor = cxn.cursor(prepared=True)
        
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
    
    def get_store_number(cxn):
        store_num_list = []
        
        cursor = cxn.cursor()
        query = (
            """
            SELECT store_num
            FROM view_stores; 
            """
        )
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        for item in result:
            store_num_list.append(item[0])
        
        return store_num_list
    
    
    
    def get_store_info(store_num, cxn):
        cursor = cxn.cursor(prepared=True)
        
        query_params = (store_num,)
        
        query = (
            """
            SELECT store_name,
                   store_address,
                   store_phone,
                   store_manager,
                   mgr_email,
                   asst_manager,
                   asst_mgr_email,
                   store_start_date
            FROM view_stores
            WHERE store_num = %s;
            """
        )
        
        cursor.execute(query, params=query_params)
        
        result = cursor.fetchall()
        
        cursor.close()
        
        return result
    
    def get_employee_nums(cxn):
        # we will convert this list to a tuple
        employee_id_tuple = []
        
        cursor = cxn.cursor()
        
        query = (
            """
            SELECT emp_id
            FROM employee
            ORDER BY emp_id;
            """
        )
        
        cursor.execute(query)
        
        result = cursor.fetchall()
        
        for num in result:
            employee_id_tuple.append(num[0])
        
        employee_id_tuple = tuple(employee_id_tuple)
        
        return employee_id_tuple
    
    
    def get_state_list(cxn):
        state_list = []

        cursor = cxn.cursor()
        query = (
            """
            SELECT DISTINCT loc_state
            FROM location;
            """
        )
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        for item in result:
            state_list.append(item[0])

        return state_list

    def get_position_id_list(cxn):
        position_id_list = []

        cursor = cxn.cursor()
        query = (
            """
            SELECT DISTINCT position_id
            FROM view_jobs_and_depts;
            """
        )

        cursor.execute(query)
        result = cursor.fetchall()

        for item in result:
            position_id_list.append(item[0])

        return position_id_list

    def get_position_info(position_id, loc_id, cxn):
        cursor = cxn.cursor(prepared=True)

        query_params = (position_id, loc_id)

        query = (
            """
            SELECT position_title,
                   dept_id,
                   dept_name
            FROM view_pos_dept_loc
            WHERE position_id = %s
            AND loc_id = %s;
            """
        )

        cursor.execute(query, params=query_params)

        result = cursor.fetchall()

        cursor.close()

        return result
    
    def get_location_numbers(cxn):
        location_num_list = []
        
        cursor = cxn.cursor()
        query = (
            """
            SELECT DISTINCT loc_id
            FROM view_pos_dept_loc
            ORDER BY loc_id;
            """
        )
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        for item in result:
            location_num_list.append(item[0])
            
        cursor.close()

        return location_num_list


    def onboard_employee(cxn, sp_name, args):
        cursor = cxn.cursor()
        result_arg = cursor.callproc(sp_name, args)
        cursor.close()
        
        return result_arg[-1]