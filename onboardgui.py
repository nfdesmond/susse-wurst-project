# import tkinter as tk
# from tkinter import ttk
# from sw_db_application.sussewurstconnect.swconnect import SusseWurstConnect
# import random

# class EmployeeOnboardGUI:
#     def __init__(self, root, cxn):
#         root.title("Süsse Wurst HR GO Employee Onboard")
#         root.geometry('500x600')
#         root.columnconfigure(0, weight=1)
#         root.rowconfigure(0, weight=1)
#         self.cxn = cxn
        
        
#         mainframe = ttk.Frame(root, padding="3 3 12 12")
#         mainframe.grid(column=0, row=0, sticky=(tk.NSEW))
        
#         onboard_label = ttk.Label(mainframe, text='Süsse Wurst New Employee Onboard')
#         onboard_label.grid(column=0, row=1, sticky=tk.W)
        
        
        
#         self.new_emp_id = tk.StringVar()
#         ttk.Label(mainframe, text='New Employee ID:').grid(column=0, row=3, sticky=tk.W)
#         emp_id_label = ttk.Label(mainframe, textvariable=self.new_emp_id)
#         emp_id_label.grid(column=1, row=3, sticky=tk.W)
        
#         emp_id = self.get_new_emp_id()
        
#         button = ttk.Button(mainframe, text='generate', command=self.set_new_emp_id(emp_id))
#         button.grid(column=1, row=4, sticky=tk.W)
        
       
        
        
        
        
#     def get_new_emp_id(self):
#         emp_ids = SusseWurstConnect.get_employee_nums(self.cxn)
#         while True:
#             new_id = random.randint(0, 999999)
#             if new_id not in emp_ids:
#                 return new_id
    
#     def set_new_emp_id(self, id_num):
#         self.new_emp_id.set(id_num)
        

import tkinter as tk
from tkinter import ttk
from sw_db_application.sussewurstconnect.swconnect import SusseWurstConnect
import random


class EmployeeOnboardGUI:
    def __init__(self, root, cxn):
        root.title("Süsse Wurst HR GO Employee Onboard")
        root.geometry('500x600')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.cxn = cxn

        # Retrieve existing employee IDs from the DB
        emp_ids = set(SusseWurstConnect.get_employee_nums(self.cxn))

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(tk.NSEW))

        onboard_label = ttk.Label(mainframe, text='Süsse Wurst New Employee Onboard')
        onboard_label.grid(column=0, row=1, sticky=tk.W)

        self.new_emp_id = tk.StringVar()

        ttk.Label(mainframe, text='New Employee ID:').grid(column=0, row=3, sticky=tk.W)
        emp_id_label = ttk.Label(mainframe, textvariable=self.new_emp_id)
        emp_id_label.grid(column=1, row=3, sticky=tk.W)

        generate_btn = ttk.Button(mainframe, text="Generate New ID", command=lambda: self.refresh_emp_id(emp_ids))
        generate_btn.grid(column=1, row=4, sticky=tk.W)

    def get_new_emp_id(self, emp_ids):
        while True:
            new_id = random.randint(0, 999999)
            if new_id not in emp_ids:
                return f"{new_id:06d}"  # Keep consistent format

    def refresh_emp_id(self, emp_ids):
        new_id = self.get_new_emp_id(emp_ids)
        self.new_emp_id.set(new_id)