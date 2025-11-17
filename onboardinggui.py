import tkinter as tk
from tkinter import ttk
import random
from datetime import date
from sw_db_application.sussewurstconnect.swconnect import SusseWurstConnect


class OnboardingGui:
    def __init__(self, root, cxn):
        root.title("Süsse Wurst New Employee Onboarding")
        root.geometry('900x700')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.resizable(width=False, height=False)
        self.cxn = cxn
        
        # Retrieve existing employee IDs from the DB
        emp_ids = set(SusseWurstConnect.get_employee_nums(self.cxn))
        
         # we will be implementing three frames: a top frame and two side-by-side main frames
        
        # top frame
        
        topframe_style = ttk.Style()
        topframe_style.configure('SWLogo.TFrame',
                                 background='#A02B93',
                                 foreground='white')
        
        
        topframe = ttk.Frame(root, padding=22, style='SWLogo.TFrame', relief='ridge')
        topframe.grid(column=0, row=0, sticky=tk.NSEW, columnspan=2)
        
        self.logo = tk.PhotoImage(file='sw_onboard_logo.png')
        logo_label = tk.Label(topframe, image=self.logo, background='#A02B93')
        logo_label.grid(column=0, row=0, sticky=tk.W)
        
        app_name_label = ttk.Label(topframe, 
                                   text='Onboarding Portal',
                                   background='#A02B93',
                                   foreground='white',
                                   font=('TkDefaultFont', 25, 'bold'))
        app_name_label.grid(column=1, row=0, sticky=tk.EW, padx=75)
        
        close_button = ttk.Button(topframe, text='Close', style='Button.TButton', command=root.destroy)
        close_button.grid(column=2, row=0, sticky=tk.E, padx=25)
        
        # side-by-side main frames
        
        # main frame one
        mainone = ttk.Frame(root, padding='3 3 12 12', relief='ridge')
        mainone.grid(column=0, row=1, sticky=(tk.NSEW))
        
        ## employee auto id
        emp_id_label = ttk.Label(mainone, 
                                 text='Employee ID:',
                                 font=('TkTextFont', 12))
        emp_id_label.grid(column=0, row=0, sticky=tk.W)
        
        self.auto_id = self.get_new_emp_id(emp_ids)
        
        
        auto_emp_id_label = ttk.Label(mainone,
                                      width=7, 
                                      text=f'{self.auto_id:06d}',
                                      background='white',
                                      relief='sunken',
                                      font=('TkTextFont', 12),
                                      justify=tk.CENTER)
        auto_emp_id_label.grid(column=1, row=0, sticky=tk.W)
        
        ttk.Label(mainone,
                  text='Hiring Date:',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=0, sticky=tk.E)

        # hire_date_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        hire_date = date.today()
        hire_date_label = ttk.Label(mainone,
                                    width=10,
                                    text=hire_date.strftime('%m/%d/%Y'),
                                    background='white',
                                    relief='sunken',
                                    font=('TkTextFont', 12),
                                    justify=tk.CENTER)
        hire_date_label.grid(column=3, row=0, sticky=tk.W)

        ttk.Label(mainone, 
                  width=20, 
                  text='Employee Information', 
                  font=('TkDefaultFont', 15, 'bold')
                  ).grid(column=0, row=1, sticky=tk.W, columnspan=4)
        
        
        ttk.Label(mainone, 
                  width=20, 
                  text='Personal Identification', 
                  font=('TkDefaultFont', 12, 'italic', 'underline')
                  ).grid(column=0, row=2, sticky=tk.W, columnspan=4)

        ## employee name
        ttk.Label(mainone,
                  text='First Name:',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=3, sticky=tk.E)
        
        self.emp_fname_var = tk.StringVar()
        emp_fname_entry = ttk.Entry(mainone,
                                    width=15,
                                    font=('TkTextFont', 12),
                                    textvariable=self.emp_fname_var)
        emp_fname_entry.grid(column=1, row=3, sticky=tk.W)

        ttk.Label(mainone,
                  text='Last Name:',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=3, sticky=tk.E)


        self.emp_lname_var = tk.StringVar()
        emp_lname_entry = ttk.Entry(mainone,
                                    width=15,
                                    font=('TkTextFont', 12),
                                    textvariable=self.emp_lname_var)
        emp_lname_entry.grid(column=3, row=3, sticky=tk.W)
        
        
        ## employee date of birth
        ttk.Label(mainone,
                  text='Date of Birth:',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=4, sticky=tk.E)


        self.emp_dob_var = tk.StringVar()
        emp_dob_entry = ttk.Entry(mainone,
                                    width=15,
                                    font=('TkTextFont', 12),
                                    textvariable=self.emp_dob_var)
        emp_dob_entry.grid(column=1, row=4, sticky=tk.W)


        ## employee SSN
        ttk.Label(mainone,
                  text='Social Security Number:',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=4, sticky=tk.E)

        
        self.emp_ssn_var = tk.StringVar()
        emp_ssn_entry = ttk.Entry(mainone,
                                    width=15,
                                    font=('TkTextFont', 12),
                                    textvariable=self.emp_ssn_var)
        emp_ssn_entry.grid(column=3, row=4, sticky=tk.W)


        ttk.Label(mainone, 
                  width=20, 
                  text='Contact Information', 
                  font=('TkDefaultFont', 12, 'italic', 'underline')
                  ).grid(column=0, row=5, sticky=tk.W, columnspan=4)

        ## employee address
        ttk.Label(mainone,
                  text='Address:',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=6, sticky=tk.E)

        self.emp_address_var = tk.StringVar()
        emp_address_entry = ttk.Entry(mainone,
                                    width=25,
                                    font=('TkTextFont', 12),
                                    textvariable=self.emp_address_var)
        emp_address_entry.grid(column=1, row=6, sticky=tk.W)
        
        ## employee city
        ttk.Label(mainone,
                  text='City:',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=6, sticky=tk.E)

        self.emp_city_var = tk.StringVar()
        emp_city_entry = ttk.Entry(mainone,
                                   width=15,
                                   font=('TkTextFont', 12),
                                   textvariable=self.emp_city_var)
        emp_city_entry.grid(column=3, row=6, sticky=tk.W)


        ## employee state
        states = SusseWurstConnect.get_state_list(self.cxn)
        
        ttk.Label(mainone,
                  text='State:',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=7, sticky=tk.E)


        self.emp_state_var = tk.StringVar()
        emp_state_entry = ttk.Combobox(mainone,
                                       textvariable=self.emp_state_var,
                                       values=states,
                                       width=3,
                                       font=('TkTextFont', 12))
        emp_state_entry.grid(column=1, row=7, sticky=tk.W)
        
        ## employee zip code
        ttk.Label(mainone,
                  text='Zip Code:',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=7, sticky=tk.E)

        self.emp_zip_var = tk.StringVar()
        emp_zip_entry = ttk.Entry(mainone,
                                  width=10,
                                  font=('TkTextFont', 12),
                                  textvariable=self.emp_zip_var)
        emp_zip_entry.grid(column=3, row=7, sticky=tk.W)
        
        ## employee phone number
        ttk.Label(mainone,
                  text='Phone Number:',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=8, sticky=tk.E)

        self.emp_phone_var = tk.StringVar()
        emp_phone_entry = ttk.Entry(mainone,
                                  width=12,
                                  font=('TkTextFont', 12),
                                  textvariable=self.emp_phone_var)
        emp_phone_entry.grid(column=1, row=8, sticky=tk.W)
        
        
        ## employee email
        ttk.Label(mainone,
                  text='Email:',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=8, sticky=tk.E)

        self.emp_email_var = tk.StringVar()
        emp_email_entry = ttk.Entry(mainone,
                                  width=25,
                                  font=('TkTextFont', 12),
                                  textvariable=self.emp_email_var)
        emp_email_entry.grid(column=3, row=8, sticky=tk.W)
        
        
        ttk.Label(mainone, 
                  width=20, 
                  text='Hiring Details', 
                  font=('TkDefaultFont', 12, 'italic', 'underline')
                  ).grid(column=0, row=9, sticky=tk.W, columnspan=4)
        
        
        ttk.Label(mainone,
                  text='Position ID:',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=10, sticky=tk.E)


        self.position_id_var = tk.StringVar()
        position_id_entry = ttk.Entry(mainone,
                                  width=3,
                                  font=('TkTextFont', 12),
                                  textvariable=self.position_id_var)
        position_id_entry.grid(column=1, row=10, sticky=tk.W)

        ttk.Label(mainone,
                  text='Position Title:',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=10, sticky=tk.E)

        self.position_title_var = tk.StringVar()
        position_title_entry = ttk.Label(mainone,
                                  width=20,
                                  font=('TkTextFont', 12),
                                  textvariable=self.position_title_var,
                                  relief='sunken')
        position_title_entry.grid(column=3, row=10, sticky=tk.W)
        
        ttk.Label(mainone,
                  text='Department ID:',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=11, sticky=tk.E)

        self.dept_id_var = tk.StringVar()
        dept_id_entry = ttk.Label(mainone,
                                  width=3,
                                  font=('TkTextFont', 12),
                                  textvariable=self.dept_id_var,
                                  relief='sunken')
        dept_id_entry.grid(column=3, row=11, sticky=tk.W)
        
        ttk.Label(mainone,
                  text='Department Name:',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=12, sticky=tk.E)

        self.dept_name_var = tk.StringVar()
        dept_name_entry = ttk.Label(mainone,
                                  width=20,
                                  font=('TkTextFont', 12),
                                  textvariable=self.dept_name_var,
                                  relief='sunken')
        dept_name_entry.grid(column=3, row=12, sticky=tk.W)

        ttk.Label(mainone,
                  text='Location ID:', 
                  font=('TkDefaultFont', 12)
                  ).grid(column=0, row=11, sticky=tk.E)

        loc_nums = SusseWurstConnect.get_location_numbers(self.cxn)
        
        self.loc_num_var = tk.StringVar()
        location_list = ttk.Combobox(mainone, 
                                  textvariable=self.loc_num_var, 
                                  values=loc_nums,
                                  width=5,
                                  font=('TkTextFont', 12, 'bold'))
        location_list.grid(column=1, row=11, sticky=tk.W)

        discover_button = ttk.Button(mainone, 
                                     text='Discover',
                                     command=self.set_position_info)
        discover_button.grid(column=1, row=9, sticky=tk.W)

        ttk.Label(mainone,
                  text='Starting Compensation:',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=12, sticky=tk.E)

        self.emp_comp_var = tk.StringVar()
        emp_comp_entry = ttk.Entry(mainone,
                                   width=10,
                                   font=('TkTextFont', 12),
                                   textvariable=self.emp_comp_var)
        emp_comp_entry.grid(column=1, row=12, sticky=tk.W)


        onboard_button = ttk.Button(mainone,
                                    text='Onboard',
                                    command=self.onboard_args)
        onboard_button.grid(column=1, row=13, sticky=tk.W)


        # main frame two
        maintwo = ttk.Frame(root, padding='3 3 12 12', relief='ridge')
        maintwo.grid(column=1, row=1, sticky=(tk.NSEW))
        
        onboard_label = ttk.Label(maintwo, text='Süsse Wurst New Employee Onboard')
        onboard_label.grid(column=0, row=0, sticky=tk.E)
        
        self.onboard_status_var = tk.StringVar()
        ttk.Label(maintwo,
                  textvariable=self.onboard_status_var
                  ).grid(column=0, row=1, sticky=tk.W)
        
        
    def get_new_emp_id(self, emp_ids):
        while True:
            new_id = random.randint(1, 999999)
            if new_id not in emp_ids:
                return new_id
    
    
    def set_position_info(self):
        pos_id = int(self.position_id_var.get())
        loc_num = int(self.loc_num_var.get())
        result_set = SusseWurstConnect.get_position_info(pos_id, loc_num, self.cxn)


        (position_title, dept_id, dept_name) = result_set[0]

        self.position_title_var.set(position_title)
        self.dept_id_var.set(dept_id)
        self.dept_name_var.set(dept_name)

        
        return None

    def onboard_args(self):
        # Implementation of the onboarding procedure goes here
        emp_id = int(self.auto_id)
        fname = self.emp_fname_var.get()
        lname = self.emp_lname_var.get()
        hire_date = date.today().strftime('%Y-%m-%d')
        dob = self.emp_dob_var.get()
        ssn = self.emp_ssn_var.get()
        address = self.emp_address_var.get()
        city = self.emp_city_var.get()
        state = self.emp_state_var.get()
        zip = self.emp_zip_var.get()
        phone = self.emp_phone_var.get()
        pos_id = int(self.position_id_var.get())
        dept_id = int(self.dept_id_var.get())   
        compensation = float(self.emp_comp_var.get())
        email = self.emp_email_var.get()
        status = ''
        
        args = (emp_id, fname, lname, hire_date, dob, ssn, address, city, state, zip, phone, pos_id, dept_id, compensation, email, status)
        
        onboard_status = SusseWurstConnect.onboard_employee(self.cxn, 'sp_employee_onboard', args)

        self.onboard_status_var.set(onboard_status)

        return None
