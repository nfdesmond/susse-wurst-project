"""
TITLE: GUI for Süsse Wurst New Employee Onboarding Application
AUTHOR: N.F. Desmond
DATE: November 2025
DESCRIPTION: This module implements a GUI for onboarding new employees into the Süsse Wurst HR database.
It features fields for entering personal information, contact details, and hiring specifics, along with buttons to discover position details and finalize the onboarding process. An Employee ID is auto-generated to ensure uniqueness.
"""
import tkinter as tk
from tkinter import ttk
import random
from datetime import date
from sw_db_application.sussewurstconnect.swconnect import SusseWurstConnect


class OnboardingGui:
  def __init__(self, root, cxn):
    root.title("Süsse Wurst New Employee Onboarding")
    root.geometry('900x600')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.resizable(width=False, height=False)
    self.cxn = cxn
        
    # Retrieve existing employee IDs from the HR database to check each new ID against
    emp_ids = set(SusseWurstConnect.get_employee_nums(self.cxn))       
        
    # We will be implementing three primary frames: a top frame and two side-by-side main frames
        
    # Top Frame
    topframe_style = ttk.Style()
    topframe_style.configure('SWLogo.TFrame',
                              background='#A02B93',
                              foreground='white')
        
    topframe = ttk.Frame(root,
                         padding=22, 
                         style='SWLogo.TFrame', 
                         relief='ridge')
    topframe.grid(column=0, row=0, sticky=tk.NSEW, columnspan=2)
    
    self.logo = tk.PhotoImage(file='sw_onboard_logo.png')
    logo_label = tk.Label(topframe, 
                          image=self.logo, 
                          background='#A02B93')
    logo_label.grid(column=0, row=0, sticky=tk.W)
        
    app_name_label = ttk.Label(topframe, 
                               text='Onboarding Portal',
                               background='#A02B93',
                               foreground='white',
                               font=('TkDefaultFont', 25, 'bold'))
    app_name_label.grid(column=1, row=0, sticky=tk.EW, padx=75)
        
    close_button = ttk.Button(topframe,
                              text='Close',
                              style='Button.TButton', 
                              command=root.destroy)
    close_button.grid(column=2, row=0, sticky=tk.E, padx=25)
        
    # Side-By-Side Main Frames
    mainone_style = ttk.Style()
    mainone_style.configure('MainOne.TFrame',
                             background='#D3D3D3')
        
    #### main frame one has four children: top, middle, bottom, last ####
    mainone = ttk.Frame(root, 
                        padding='3 3 12 12', 
                        relief='ridge',
                        style='MainOne.TFrame')
    mainone.grid(column=0, row=1, sticky=(tk.NSEW))
        
    mainonetop = ttk.Frame(mainone,
                           padding='3 3 12 12',
                           style='MainOne.TFrame')
    mainonetop.grid(column=0, row=0, sticky=(tk.NSEW))

        
        ttk.Label(mainonetop, 
                  width=20, 
                  text='Employee Information', 
                  background='#D3D3D3',
                  font=('TkDefaultFont', 15, 'bold')
                  ).grid(column=0, row=0, sticky=tk.W)
        
        ttk.Label(mainonetop,
                  text='Hiring Date:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=1, row=0, sticky=tk.E)
        
        hire_date = date.today()
        hire_date_label = ttk.Label(mainonetop,
                                    width=10,
                                    text=hire_date.strftime('%m/%d/%Y'),
                                    background='white',
                                    relief='sunken',
                                    font=('TkTextFont', 12),
                                    justify=tk.CENTER)
        hire_date_label.grid(column=2, row=0, sticky=tk.EW)
        
        
        onboard_button = ttk.Button(mainonetop,
                                    text='Onboard',
                                    command=self.onboard_args)
        onboard_button.grid(column=3, row=0, sticky=tk.E)

        
        mainonemiddle = ttk.Frame(mainone,
                                  padding='3 3 12 12',
                                  style='MainOne.TFrame')
        mainonemiddle.grid(column=0, row=1, sticky=(tk.NSEW))
        
        
        ttk.Label(mainonemiddle, 
                  width=20, 
                  text='Personal Identification', 
                  background='#D3D3D3',
                  font=('TkDefaultFont', 14, 'italic', 'underline')
                  ).grid(column=0, row=0, sticky=tk.W, columnspan=5)
        
        
        ## employee auto id
        emp_id_label = ttk.Label(mainonemiddle, 
                                 text='Employee ID:',
                                 background='#D3D3D3',
                                 font=('TkTextFont', 12))
        emp_id_label.grid(column=0, row=1, sticky=tk.W)
        
        self.auto_id = self.get_new_emp_id(emp_ids)
        
        
        auto_emp_id_label = ttk.Label(mainonemiddle,
                                      width=7, 
                                      text=f'{self.auto_id:06d}',
                                      background='#DFF4FD',
                                      relief='sunken',
                                      font=('TkTextFont', 12, 'bold'),
                                      justify=tk.CENTER)
        auto_emp_id_label.grid(column=1, row=1, sticky=tk.W)
        

        ## employee name
        ttk.Label(mainonemiddle,
                  text='First Name:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=2, sticky=tk.E)
        
        self.emp_fname_var = tk.StringVar()
        emp_fname_entry = ttk.Entry(mainonemiddle,
                                    width=15,
                                    font=('TkTextFont', 12),
                                    textvariable=self.emp_fname_var)
        emp_fname_entry.grid(column=1, row=2, sticky=tk.W)
        
        ttk.Label(mainonemiddle,
                  text='Last Name:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=2, sticky=tk.E)

        self.emp_lname_var = tk.StringVar()
        emp_lname_entry = ttk.Entry(mainonemiddle,
                                    width=15,
                                    font=('TkTextFont', 12),
                                    textvariable=self.emp_lname_var)
        emp_lname_entry.grid(column=3, row=2, sticky=tk.W)
        
        
        ## employee date of birth
        ttk.Label(mainonemiddle,
                  text='Date of Birth:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=3, sticky=tk.E)


        self.emp_dob_var = tk.StringVar()
        emp_dob_entry = ttk.Entry(mainonemiddle,
                                    width=15,
                                    font=('TkTextFont', 12),
                                    textvariable=self.emp_dob_var)
        emp_dob_entry.grid(column=1, row=3, sticky=tk.W)

        ## employee SSN
        ttk.Label(mainonemiddle,
                  text='Social Security Number:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=3, sticky=tk.E)

        
        self.emp_ssn_var = tk.StringVar()
        emp_ssn_entry = ttk.Entry(mainonemiddle,
                                    width=15,
                                    font=('TkTextFont', 12),
                                    textvariable=self.emp_ssn_var)
        emp_ssn_entry.grid(column=3, row=3, sticky=tk.W)



        mainonebottom = ttk.Frame(mainone,
                                  padding='3 3 12 12',
                                  style='MainOne.TFrame')
        mainonebottom.grid(column=0, row=2, sticky=(tk.NSEW))
        
        
        ttk.Label(mainonebottom, 
                  width=20, 
                  text='Contact Information', 
                  background='#D3D3D3',
                  font=('TkDefaultFont', 14, 'italic', 'underline')
                  ).grid(column=0, row=0, sticky=tk.W, columnspan=5)

        ## employee address
        ttk.Label(mainonebottom,
                  text='Address:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=1, sticky=tk.E)

        self.emp_address_var = tk.StringVar()
        emp_address_entry = ttk.Entry(mainonebottom,
                                    width=25,
                                    font=('TkTextFont', 12),
                                    textvariable=self.emp_address_var)
        emp_address_entry.grid(column=1, row=1, sticky=tk.W)
        
        ## employee city
        ttk.Label(mainonebottom,
                  text='City:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=1, sticky=tk.E)

        self.emp_city_var = tk.StringVar()
        emp_city_entry = ttk.Entry(mainonebottom,
                                   width=15,
                                   font=('TkTextFont', 12),
                                   textvariable=self.emp_city_var)
        emp_city_entry.grid(column=3, row=1, sticky=tk.W)

        ## employee state
        states = SusseWurstConnect.get_state_list(self.cxn)
        
        ttk.Label(mainonebottom,
                  text='State:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=2, sticky=tk.E)


        self.emp_state_var = tk.StringVar()
        emp_state_entry = ttk.Combobox(mainonebottom,
                                       textvariable=self.emp_state_var,
                                       values=states,
                                       width=3,
                                       font=('TkTextFont', 12))
        emp_state_entry.grid(column=1, row=2, sticky=tk.W)
        
        ## employee zip code
        ttk.Label(mainonebottom,
                  text='Zip Code:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=2, sticky=tk.E)

        self.emp_zip_var = tk.StringVar()
        emp_zip_entry = ttk.Entry(mainonebottom,
                                  width=10,
                                  font=('TkTextFont', 12),
                                  textvariable=self.emp_zip_var)
        emp_zip_entry.grid(column=3, row=2, sticky=tk.W)
        
        ## employee phone number
        ttk.Label(mainonebottom,
                  text='Phone Number:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=3, sticky=tk.E)

        self.emp_phone_var = tk.StringVar()
        emp_phone_entry = ttk.Entry(mainonebottom,
                                  width=12,
                                  font=('TkTextFont', 12),
                                  textvariable=self.emp_phone_var)
        emp_phone_entry.grid(column=1, row=3, sticky=tk.W)
        
        
        ## employee email
        ttk.Label(mainonebottom,
                  text='Email:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=3, sticky=tk.E)

        self.emp_email_var = tk.StringVar()
        emp_email_entry = ttk.Entry(mainonebottom,
                                  width=25,
                                  font=('TkTextFont', 12),
                                  textvariable=self.emp_email_var)
        emp_email_entry.grid(column=3, row=3, sticky=tk.W)
        
        
        mainonelast = ttk.Frame(mainone,
                                  padding='3 3 12 12',
                                  style='MainOne.TFrame')
        mainonelast.grid(column=0, row=3, sticky=(tk.NSEW))
        
        ttk.Label(mainonelast, 
                  width=20, 
                  text='Hiring Details',
                  background='#D3D3D3',
                  font=('TkDefaultFont', 14, 'italic', 'underline')
                  ).grid(column=0, row=0, sticky=tk.W, columnspan=4)
        
        
        discover_button = ttk.Button(mainonelast, 
                                     text='Discover',
                                     command=self.set_position_info)
        discover_button.grid(column=1, row=0, sticky=tk.W)
        
        
        ttk.Label(mainonelast,
                  text='Position ID:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=2, sticky=tk.E)


        self.position_id_var = tk.StringVar()
        position_id_entry = ttk.Entry(mainonelast,
                                  width=3,
                                  font=('TkTextFont', 12),
                                  textvariable=self.position_id_var)
        position_id_entry.grid(column=1, row=2, sticky=tk.W)
        
        ttk.Label(mainonelast,
                  text='Position Title:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=2, sticky=tk.E)
        
        
        self.position_title_var = tk.StringVar()
        position_title_entry = ttk.Label(mainonelast,
                                  width=20,
                                  font=('TkTextFont', 12),
                                  textvariable=self.position_title_var,
                                  relief='sunken')
        position_title_entry.grid(column=3, row=2, sticky=tk.W)
        
        
        ttk.Label(mainonelast,
                  text='Location ID:', 
                  background='#D3D3D3',
                  font=('TkDefaultFont', 12)
                  ).grid(column=0, row=3, sticky=tk.E)

        loc_nums = SusseWurstConnect.get_location_numbers(self.cxn)
        
        self.loc_num_var = tk.StringVar()
        location_list = ttk.Combobox(mainonelast, 
                                  textvariable=self.loc_num_var, 
                                  values=loc_nums,
                                  width=5,
                                  font=('TkTextFont', 12, 'bold'))
        location_list.grid(column=1, row=3, sticky=tk.W)
        
        
        ttk.Label(mainonelast,
                  text='Department ID:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=3, sticky=tk.E)

        self.dept_id_var = tk.StringVar()
        dept_id_entry = ttk.Label(mainonelast,
                                  width=3,
                                  font=('TkTextFont', 12),
                                  textvariable=self.dept_id_var,
                                  relief='sunken')
        dept_id_entry.grid(column=3, row=3, sticky=tk.W)
        
        ttk.Label(mainonelast,
                  text='Department Name:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=2, row=4, sticky=tk.E)

        self.dept_name_var = tk.StringVar()
        dept_name_entry = ttk.Label(mainonelast,
                                  width=20,
                                  font=('TkTextFont', 12),
                                  textvariable=self.dept_name_var,
                                  relief='sunken')
        dept_name_entry.grid(column=3, row=4, sticky=tk.W)

      
        ttk.Label(mainonelast,
                  text='Starting Compensation:',
                  background='#D3D3D3',
                  font=('TkTextFont', 12)
                ).grid(column=0, row=4, sticky=tk.E)

        self.emp_comp_var = tk.StringVar()
        emp_comp_entry = ttk.Entry(mainonelast,
                                   width=10,
                                   font=('TkTextFont', 12),
                                   textvariable=self.emp_comp_var)
        emp_comp_entry.grid(column=1, row=4, sticky=tk.W)

        
        for child in mainone.winfo_children():
          for grandchild in child.winfo_children():
              grandchild.grid_configure(padx=3, pady=3)


        # main frame two
        maintwo_style = ttk.Style()
        maintwo_style.configure('MainTwo.TFrame', background='#FBF3DD')
        
        maintwo = ttk.Frame(root, 
                            padding='3 3 12 12',
                            relief='ridge',
                            style='MainTwo.TFrame')
        maintwo.grid(column=1, row=1, sticky=(tk.NSEW))
        
        onboard_label = ttk.Label(maintwo,
                                  text='Onboard Status:',
                                  background='#FBF3DD',
                                  font=('TkDefaultFont', 12, 'bold'))
        onboard_label.grid(column=0, row=0, sticky=tk.E)
        
        self.onboard_status_var = tk.StringVar()
        status_label = ttk.Label(maintwo,
                                 textvariable=self.onboard_status_var,
                                 font=('TkTextFont', 12))
        status_label.grid(column=0, row=1, sticky=tk.W)
        
        
    def get_new_emp_id(self, emp_ids):
      """Generate a unique employee ID not already in emp_ids set."""
      while True:
        new_id = random.randint(1, 999999)
        if new_id not in emp_ids:
          return new_id
    
    
    def set_position_info(self):
      """Retrieve and set job position information based on entered Position ID and Location Number."""
      pos_id = int(self.position_id_var.get())
      loc_num = int(self.loc_num_var.get())
      result_set = SusseWurstConnect.get_position_info(pos_id, loc_num, self.cxn)
      
      (position_title, dept_id, dept_name) = result_set[0]

      self.position_title_var.set(position_title)
      self.dept_id_var.set(dept_id)
      self.dept_name_var.set(dept_name)

      return None


    def onboard_args(self):
      """Collect all onboarding information and call the onboard_employee stored procedure."""
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
        
      args = (
        emp_id, fname, lname, hire_date, dob, 
        ssn, address, city, state, zip, phone, 
        pos_id, dept_id, compensation, email, status
        )
        
      onboard_status = SusseWurstConnect.onboard_employee(self.cxn, 'sp_employee_onboard', args)

      self.onboard_status_var.set(onboard_status)

      return None
