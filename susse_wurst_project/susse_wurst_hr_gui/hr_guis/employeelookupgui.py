"""
TITLE: Süsse Wurst HR Employee Lookup GUI
AUTHOR: N.F. Desmond
DATE: November 2025
DESCRIPTION: This module creates a GUI for looking up employee information 
in the Süsse Wurst HR database. It includes a field for entering an employee ID, 
which will display an employee's name, department, job title, manager, and 
length of service if found.
"""
import tkinter as tk
from tkinter import ttk
from susse_wurst_project.susse_wurst_hr_gui.sussewurstconnect.swconnect import SusseWurstConnect

class EmployeeLookupGUI:
    """Instantiate the Employee Lookup GUI."""
    def __init__(self, root, cxn):
        root.title("Süsse Wurst HR GO Employee Lookup")
        root.geometry('700x350')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.resizable(width=False, height=False)
        self.cxn = cxn
        
        
        # Implementing the top frame of the app which will feature the 
        # Süsse Wurst logo, app name, and close button
        
        topframe_style = ttk.Style()
        topframe_style.configure('SWLogo.TFrame',
                                 background='#737373',
                                 relief='raised')
        
        button_style = ttk.Style()
        button_style.configure('Button.TButton',
                               font=('TkMenuFont', 12))
        
        topframe = ttk.Frame(root, 
                             padding=22, 
                             style='SWLogo.TFrame', 
                             height=500)
        topframe.grid(column=0, row=0, sticky=tk.NSEW)
        
        self.logo = tk.PhotoImage(file=r'sw_db_application\sw_logos\sw_emplookup_logo.png')

        logo_label = ttk.Label(topframe, 
                               image=self.logo, 
                               background='#737373')
        logo_label.grid(column=0, row=0, sticky=tk.W)
        
        app_name_label = ttk.Label(topframe, 
                                   text='Employee Lookup', 
                                   background='#737373',
                                   foreground='#002060',
                                   font=('TkDefaultFont', 20, 'bold'))
        app_name_label.grid(column=1, row=0, sticky=tk.EW, padx=50)
        
        close_button = ttk.Button(topframe, 
                                  text="Close", 
                                  style='Button.TButton', 
                                  command=root.destroy)
        close_button.grid(column=2, row=0, sticky=tk.E)
        
        
        # implementing the main frame of the app for conducting employee searches
        entry_style = ttk.Style()
        entry_style.configure('IDEntry.TEntry',
                              background='white',
                              relief='sunken')
        
        dynamic_style = ttk.Style()
        dynamic_style.configure('Dynamic.TLabel',
                                foreground='#002060',
                                font=('TkTextFont', 13))
        
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=1, sticky=(tk.NSEW))
        
        
        self.emp_id_var = tk.StringVar()
        emp_id_entry = ttk.Entry(mainframe, 
                                 width=10, 
                                 style='IDEntry.TEntry', 
                                 font=('TkTextFont', 15),
                                 justify='left',
                                 textvariable=self.emp_id_var)
        
        emp_id_entry.grid(column=1, row=2, sticky=(tk.W))
        
        emp_id_label = ttk.Label(mainframe, 
                                 width=20, 
                                 text="Enter the employee ID", 
                                 font=('TkDefaultFont', 15, 'bold'))
        emp_id_label.grid(column=1, row=1, sticky=(tk.EW))
        
        
        name_label = ttk.Label(mainframe, 
                               text="NAME:", 
                               font=('TkDefaultFont', 12, 'bold'))
        name_label.grid(column=3, row=2, sticky=tk.E)
        
        self.emp_name_var = tk.StringVar()
        emp_name_label = ttk.Label(mainframe, 
                                   textvariable=self.emp_name_var, 
                                   width=25, 
                                   style='Dynamic.TLabel', 
                                   font='bold')
        emp_name_label.grid(column=4, row=2, sticky=tk.EW)
        
        job_title_label= ttk.Label(mainframe, 
                                   text="JOB TITLE:", 
                                   font=('TkDefaultFont', 12, 'bold'))
        job_title_label.grid(column=3, row=3, sticky=tk.E)
        
        self.job_title_var = tk.StringVar()
        job_label = ttk.Label(mainframe, 
                              textvariable=self.job_title_var, 
                              width=25, 
                              style='Dynamic.TLabel')
        job_label.grid(column=4, row=3, sticky=tk.W)
        
        dept_label = ttk.Label(mainframe, 
                               text="DEPT:", 
                               font=('TkDefaultFont', 12, 'bold'))
        dept_label.grid(column=3, row=4, sticky=tk.E)
        
        self.dept_name_var = tk.StringVar()
        dept_name_label = ttk.Label(mainframe, 
                                    textvariable=self.dept_name_var, 
                                    width=25, 
                                    style='Dynamic.TLabel')
        dept_name_label.grid(column=4, row=4, sticky=tk.W)
        
        mgr_label = ttk.Label(mainframe, 
                              text="MANAGER:", 
                              font=('TkDefaultFont', 12, 'bold'))
        mgr_label.grid(column=3, row=5, sticky=tk.E)
        
        self.mgr_name_var = tk.StringVar()
        mgr_name_label = ttk.Label(mainframe, 
                                   textvariable=self.mgr_name_var, 
                                   width=25, 
                                   style='Dynamic.TLabel')
        mgr_name_label.grid(column=4, row=5, sticky=tk.W)
        
        
        tenure_label = ttk.Label(mainframe, 
                                 text="LENGTH OF SERVICE:", 
                                 font=('TkDefaultFont', 12, 'bold'))
        tenure_label.grid(column=3, row=6, sticky=tk.E)
        
        self.tenure_var = tk.StringVar()
        tenure_var_label = ttk.Label(mainframe, 
                                     textvariable=self.tenure_var, 
                                     width=25, 
                                     style='Dynamic.TLabel')
        tenure_var_label.grid(column=4, row=6, sticky=tk.W)
        
        self.not_found_var = tk.StringVar()
        not_found_msg_label = ttk.Label(mainframe, 
                                        textvariable=self.not_found_var,
                                        foreground='red',
                                        font=('TkTextFont', 12, 'bold'))
        not_found_msg_label.grid(column=1, row=4, sticky=tk.W)
        
        self.found_var = tk.StringVar()
        found_msg_label = ttk.Label(mainframe, 
                                    textvariable=self.found_var,
                                    foreground='green',
                                    font=('TkTextFont', 12, 'bold'))
        found_msg_label.grid(column=1, row=4, sticky=tk.W)
        
        get_emp_bttn = ttk.Button(mainframe, 
                                  text="Find Employee", 
                                  style='Button.TButton', 
                                  command=self.set_employee_info)
        get_emp_bttn.grid(column=1, row=3, sticky=tk.W)
        
        
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
            
    def set_employee_info(self):
        """Retrieve and display employee information based on entered employee ID."""
        emp_id = int(self.emp_id_var.get())
        result_set = SusseWurstConnect.get_employee_info(emp_id, self.cxn)
        
        if not result_set:
            self.not_found_var.set(' *No employee found.')
            self.emp_name_var.set('')
            self.dept_name_var.set('')
            self.job_title_var.set('')
            self.mgr_name_var.set('')
            self.tenure_var.set('')
            self.found_var.set('')
        else:
            emp_name, dept_name, job_title, mgr_name, tenure = result_set[0]
        
            self.emp_name_var.set(emp_name)
            self.dept_name_var.set(dept_name)
            self.job_title_var.set(job_title)
            self.mgr_name_var.set(mgr_name)
            self.tenure_var.set(tenure)
            self.found_var.set('Found')
            self.not_found_var.set('')
        
        return None