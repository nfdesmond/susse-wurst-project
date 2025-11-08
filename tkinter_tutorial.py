import tkinter as tk
from tkinter import ttk
import sw_db_application.sussewurstconnect.swconnect as swconnect
import sw_db_application.sussewurstconnect.swconfig as swconfig


hr_app = swconnect.SusseWurstConnect('susse_wurst_hr')

hr_cxn = hr_app.mysql_connect(swconfig.USER, swconfig.PSWD, use_pure_flag=True)

if hr_app.cxn_test(hr_cxn):
    def get_employee_info(employee_id):
        hr_cursor = hr_cxn.cursor()
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
        
        hr_cursor.execute(query, params=query_params)
        result = hr_cursor.fetchall()

        hr_cursor.close()
        
        return result 

    
    
    root = tk.Tk()
    root.title("Susse Wurst Employee Lookup")
    
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    emp_id_var = tk.IntVar()
    emp_id_entry = ttk.Entry(mainframe, width=10, textvariable=emp_id_var)
    emp_id_entry.grid(column=1, row=2, sticky=(tk.W))
    
    emp_id_label = ttk.Label(mainframe, width=20, text="Enter the employee ID")
    emp_id_label.grid(column=1, row=1, sticky=(tk.W, tk.E))
    
    
    name_label = ttk.Label(mainframe, text="NAME:")
    name_label.grid(column=3, row=2, sticky=tk.E)
    
    emp_name_var = tk.StringVar()
    emp_name_label = ttk.Label(mainframe, textvariable=emp_name_var)
    emp_name_label.grid(column=4, row=2, sticky=tk.W)
    
    job_title_label= ttk.Label(mainframe, text="JOB TITLE:")
    job_title_label.grid(column=3, row=3, sticky=tk.E)
    
    job_title_var = tk.StringVar()
    job_label = ttk.Label(mainframe, textvariable=job_title_var)
    job_label.grid(column=4, row=3, sticky=tk.W)
    
    dept_label = ttk.Label(mainframe, text="DEPT:")
    dept_label.grid(column=3, row=4, sticky=tk.E)
    
    dept_name_var = tk.StringVar()
    dept_name_label = ttk.Label(mainframe, textvariable=dept_name_var)
    dept_name_label.grid(column=4, row=4, sticky=tk.W)
    
    mgr_label = ttk.Label(mainframe, text="MANAGER:")
    mgr_label.grid(column=3, row=5, sticky=tk.E)
    
    mgr_name_var = tk.StringVar()
    mgr_name_label = ttk.Label(mainframe, textvariable=mgr_name_var)
    mgr_name_label.grid(column=4, row=5, sticky=tk.W)
    
    
    tenure_label = ttk.Label(mainframe, text="LENGTH OF SERVICE:")
    tenure_label.grid(column=3, row=6, sticky=tk.E)
    
    tenure_var = tk.StringVar()
    tenure_var_label = ttk.Label(mainframe, textvariable=tenure_var)
    tenure_var_label.grid(column=4, row=6, sticky=tk.W)
    
    not_found_var = tk.StringVar()
    not_found_msg_label = ttk.Label(mainframe, textvariable=not_found_var)
    not_found_msg_label.grid(column=1, row=4, sticky=tk.W)
    
    
    
    
    def set_employee_info():
        emp_id = int(emp_id_var.get())
        result_set = get_employee_info(emp_id)
        
        if not result_set:
            not_found_var.set('No employee found.')
            emp_name_var.set('')
            dept_name_var.set('')
            job_title_var.set('')
            mgr_name_var.set('')
            tenure_var.set('')
        else:
            emp_name, dept_name, job_title, mgr_name, tenure = result_set[0]
        
            emp_name_var.set(emp_name)
            dept_name_var.set(dept_name)
            job_title_var.set(job_title)
            mgr_name_var.set(mgr_name)
            tenure_var.set(tenure)
            not_found_var.set('')
    
    get_emp_bttn = ttk.Button(mainframe, text="Find Employee", command=set_employee_info)
    get_emp_bttn.grid(column=1, row=3, sticky=tk.W)
    
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)
    
    root.mainloop()
    


# hr_cxn.close()

# if hr_app.cxn_test(hr_cxn):
#     print('Still alive!')
# else:
#     print('The connection has been closed.')