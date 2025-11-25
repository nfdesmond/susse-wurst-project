"""
TITLE: Süsse Wurst HR GUI
AUTHOR: N.F. Desmond
DATE: November 2025
DESCRIPTION: This module creates the GUI for the Süsse Wurst HR application. 
The GUI is a jumpad for accessing the employee portal, store lookup, and onboarding
GUIs.
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime as dt
from sussewurstconnect import swconfig
from sussewurstconnect.swconnect import SusseWurstConnect
from hr_guis.employeelookupgui import EmployeeLookupGUI
from hr_guis.storelookupgui import StoreLookupGUI
from hr_guis.onboardinggui import OnboardingGui


class HRGui:
    """Instantiate the Süsse Wurst HR GUI."""
    def __init__(self, root, cxn):
        self.root = root
        root.title('Süsse Wurst Human Resources')
        root.resizable(width=False, height=False)
        root.geometry('900x500')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0)
        root.rowconfigure(1, weight=1)
        self.cxn = cxn

        # top frame styling
        topframe_style = ttk.Style()
        topframe_style.theme_use('clam')
        topframe_style.configure(style='tf.TFrame', 
                                 background='#3A3A3A')
        
        toplabel_style = ttk.Style()
        toplabel_style.theme_use('clam')
        toplabel_style.configure(style='tf.TLabel',
                                 font=('arial', 13), 
                                 background='#3A3A3A',
                                 foreground='white')
        
        topbutton_style = ttk.Style()
        topbutton_style.theme_use('clam')
        topbutton_style.configure(style='tf.TButton',
                                  font=('arial', 12, 'bold'))
        
        
        
        # mainframe styling
        mf_style = ttk.Style()
        mf_style.theme_use('clam')
        mf_style.configure(style='mf.TFrame', 
                           background='#1F90C3')
        
        mf_label_style = ttk.Style()
        mf_label_style.theme_use('clam')
        mf_label_style.configure(style='mf.TLabel', 
                                 background='#1F90C3')
        
        top_button_style = ttk.Style()
        top_button_style.theme_use('clam')
        top_button_style.configure(style='tr.TButton',
                                   font=('Arial', 13, 'bold'),
                                   padding='3',
                                   background='#ED8A59',
                                   foreground='black')
        
        top_button_style.map('tr.TButton',
                             foreground=[('active', 'black')],
                             background=[('active', '#E76321')])
        
        
        side_button_style = ttk.Style()
        side_button_style.theme_use('clam')
        side_button_style.configure(style='sc.TButton',
                                    font=('Arial', 13, 'bold'),
                                    padding='5',
                                    background='#4EA72E',
                                    foreground='white')
        
        
        side_button_style.map('sc.TButton', 
                              foreground=[('active', 'white')],
                              background=[('active', '#3B7D23')])
        
        
        
        # create top frame and top frame widgets
        self.topframe = ttk.Frame(root,
                                  padding='3 3 6 6',
                                  style='tf.TFrame')
        
        self.topframe.grid(column=0, row=0, sticky=tk.NSEW)
        
        self.topframe.columnconfigure(0, weight=1)
        self.topframe.columnconfigure(1, weight=1)
        self.topframe.columnconfigure(2, weight=1)
        self.topframe.rowconfigure(0)
        

        company_logo = tk.PhotoImage(file=r'sw_db_application\sw_logos\sw_logo.png', 
                                     height=50, width=215)
        
        
        self.comp_label = ttk.Label(self.topframe,
                                    image=company_logo,
                                    style='tf.TLabel')
        self.comp_label.grid(column=0, row=0, sticky=tk.W)
        
        
        today = dt.now().strftime('%A, %B %d %Y %I:%M %p')
        
        self.date_label = ttk.Label(self.topframe,
                                    text=today,
                                    style='tf.TLabel')
        
        self.date_label.grid(column=1, row=0, sticky=tk.EW)
        
        
        self.quit_button = ttk.Button(self.topframe,
                                      width=5,
                                      text='Quit',
                                      command=root.destroy,
                                      style='tf.TButton')
        
        self.quit_button.grid(column=2, row=0, padx=15, sticky=tk.E)
        
        
        # create mainframe and mainframe widgets
        self.mainframe = ttk.Frame(root,
                                   padding='3 3 12 12',
                                   style='mf.TFrame')
        
        self.mainframe.grid(column=0, row=1, sticky=tk.NSEW)
        
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.columnconfigure(3, weight=1)
        self.mainframe.columnconfigure(4, weight=1)
        self.mainframe.rowconfigure(0)
        self.mainframe.rowconfigure(1)
        self.mainframe.rowconfigure(2)
        self.mainframe.rowconfigure(3)
        
        hrgo_logo = tk.PhotoImage(file=r'sw_db_application\sw_logos\hr_go_logo.png',
                                  height=85,
                                  width=305)
        
        self.hrgo_label = ttk.Label(self.mainframe,
                                    image=hrgo_logo,
                                    style='mf.TLabel')
        
        self.hrgo_label.grid(column=0, row=0, sticky=tk.W)
        
        ## mainframe top row buttons
        self.store_button = ttk.Button(self.mainframe, 
                                     text='Stores', 
                                     command=self.open_storelookup_gui,
                                     style='tr.TButton')
        self.store_button.grid(column=1, row=0)
        
        self.portal_button = ttk.Button(self.mainframe, 
                                        text='Employee Portal', 
                                        command=self.open_emplookup_gui,
                                        style='tr.TButton')
        self.portal_button.grid(column=3, row=0)
        
        self.onboard_button = ttk.Button(self.mainframe, 
                                       text='Onboard New Hire', 
                                       command=self.open_onboarding_gui,
                                       style='tr.TButton')
        self.onboard_button.grid(column=5, row=0)
        
        
        
        
        ## mainframe side column buttons
        self.depts_button = ttk.Button(self.mainframe, 
                                       text='Departments', 
                                       command=self.open_depts_window,
                                       style='sc.TButton')
        self.depts_button.grid(column=0, row=1, sticky=tk.W, pady=15, padx=10)
        
        self.pos_button = ttk.Button(self.mainframe, 
                                     text='Positions', 
                                     command=self.open_position_window,
                                     style='sc.TButton')
        self.pos_button.grid(column=0, row=2, sticky=tk.W, pady=15, padx=10)
        
        self.open_pos_button = ttk.Button(self.mainframe, 
                                          text='View Open Positions', 
                                          command=self.view_open_positions,
                                          style='sc.TButton')
        self.open_pos_button.grid(column=0, row=3, sticky=tk.W, pady=15, padx=10)
        
        root.mainloop()
        
        
        
    def open_storelookup_gui(self):
        """Instantiate the Store Lookup GUI."""
        parent = tk.Toplevel(self.mainframe)
        store_gui = StoreLookupGUI(parent, self.cxn)
        parent.mainloop()
        
        
    def open_emplookup_gui(self):
        """Instantiate the Employee Lookup GUI."""
        parent = tk.Toplevel(self.mainframe)
        emp_gui = EmployeeLookupGUI(parent, self.cxn)
        parent.mainloop()
    

    def open_onboarding_gui(self):
        """Instantiate the Onboarding GUI."""
        parent = tk.Toplevel(self.mainframe)
        board_gui = OnboardingGui(parent, self.cxn)
        parent.mainloop()
    
    
    def open_depts_window(self):
        dept_window = tk.Toplevel(self.mainframe)
        dept_window.title('Süsse Wurst Departments')
        dept_window.geometry('300x300')
        dept_window.focus()
    
    def open_position_window(self):
        pos_window = tk.Toplevel(self.mainframe)
        pos_window.title('Süsse Wurst Positions')
        pos_window.geometry('300x300')
        pos_window.focus()
    
    def view_open_positions(self):
        openpos_window = tk.Toplevel(self.mainframe)
        openpos_window.title('Süsse Wurst Open Positions')
        openpos_window.geometry('300x300')
        openpos_window.focus()
   
        
        


