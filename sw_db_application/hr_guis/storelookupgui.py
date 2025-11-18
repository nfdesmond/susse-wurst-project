"""
TITLE: Süsse Wurst HR Store Lookup GUI
AUTHOR: N.F. Desmond
DATE: November 2025
DESCRIPTION: This module creates a GUI for looking up store information 
in the Süsse Wurst HR database. It includes a combobox for selecting a 
store number, which will display the store's name, address, phone number, 
manager, assistant manager, and opening date.
"""
import webbrowser
import tkinter as tk
from tkinter import ttk
from sw_db_application.sussewurstconnect.swconnect import SusseWurstConnect

class StoreLookupGUI:
    def __init__(self, root, cxn):
        root.title("Süsse Wurst HR GO Store Lookup")
        root.geometry('1000x350')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.resizable(width=False, height=False)
        self.cxn = cxn
        
        
        # Implementing the top frame of the app which will feature the 
        # Süsse Wurst logo, app name, and close button
        
        topframe_style = ttk.Style()
        topframe_style.configure('SWLogo.TFrame',
                                 background='#0B769F',
                                 relief='raised')
        
        button_style = ttk.Style()
        button_style.configure('Button.TButton',
                               font=('TkMenuFont', 10))
        
        topframe = ttk.Frame(root, 
                             padding=22, 
                             style='SWLogo.TFrame', 
                             height=500)
        topframe.grid(column=0, row=0, sticky=tk.NSEW)
        
        self.logo = tk.PhotoImage(file=r'sw_db_application\sw_logos\sw_storelookup_logo.png')

        logo_label = ttk.Label(topframe, 
                               image=self.logo, 
                               background='#0B769F')
        logo_label.grid(column=0, row=0, sticky=tk.W)
        
        
        app_name_label = ttk.Label(topframe, 
                                   text='Store Lookup', 
                                   background='#0B769F',
                                   foreground='#E8E8E8',
                                   font=('TkDefaultFont', 25, 'bold'))
        app_name_label.grid(column=1, row=0, sticky=tk.EW, padx=150)
        
        close_button = ttk.Button(topframe, 
                                  text="Close", 
                                  style='Button.TButton', 
                                  command=root.destroy)
        close_button.grid(column=2, row=0, sticky=tk.E, padx=50)
        
        
        
        # implementing the main frame of the app for displaying store details
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=1, sticky=(tk.NSEW))
        
        store_list_label = ttk.Label(mainframe, 
                                     width=20, 
                                     text='Select a store number', 
                                     font=('TkDefaultFont', 15, 'bold'))
        store_list_label.grid(column=1, row=1, sticky=tk.W)
        
        store_nums = SusseWurstConnect.get_store_number(self.cxn)
        
        
        self.store_num_var = tk.StringVar()
        store_list = ttk.Combobox(mainframe, 
                                  textvariable=self.store_num_var, 
                                  values=store_nums,
                                  width=10,
                                  font=('TkTextFont', 12, 'bold'))
        store_list.grid(column=1, row=2, sticky=tk.W)
        
        
        self.store_name_var = tk.StringVar()
        store_name_label = ttk.Label(mainframe,
                                     textvariable=self.store_name_var,
                                     foreground='#1D4C8B',
                                     font=('TkDefaultFont', 15, 'bold'))
        store_name_label.grid(column=2, row=1, sticky=tk.E)
        
        self.store_mgr_var = tk.StringVar()
        store_mgr_label = ttk.Label(mainframe, 
                                    text='Store Manager:',
                                    font=('TkDefaultFont', 12, 'bold'))
        store_mgr_label.grid(column=2, row=2, sticky=tk.E)
        
        store_mgr_display = ttk.Label(mainframe, 
                                      textvariable=self.store_mgr_var,
                                      font=('TkDefaultFont', 11))
        store_mgr_display.grid(column=3, row=2, sticky=tk.W)
        
        self.mgr_contact_var = tk.StringVar()
        store_mgr_contact = ttk.Label(mainframe, 
                                      textvariable=self.mgr_contact_var,
                                      foreground='blue',
                                      font=('TkDefaultFont', 11, 'underline', 'italic'),
                                      cursor='hand2')
        store_mgr_contact.grid(column=4, row=2,sticky=tk.W)
        store_mgr_contact.bind("<Button-1>", lambda e: self.go_to_email(self.asst_contact_var))
        
        
        self.asst_mgr_var = tk.StringVar()
        asst_mgr_label = ttk.Label(mainframe, 
                                   text='Assistant Manager:',
                                   font=('TkTextFont', 12, 'bold'))
        asst_mgr_label.grid(column=2, row=3, sticky=tk.E)
        
        asst_mgr_display = ttk.Label(mainframe, 
                                     textvariable=self.asst_mgr_var,
                                     font=('TkDefaultFont', 11))
        asst_mgr_display.grid(column=3, row=3, sticky=tk.W)
        
        self.asst_contact_var = tk.StringVar()
        asst_mgr_contact = ttk.Label(mainframe,
                                     textvariable=self.asst_contact_var,
                                     foreground='blue',
                                     font=('TkDefaultFont', 11, 'underline', 'italic'),
                                     cursor='hand2')
        asst_mgr_contact.grid(column=4, row=3, sticky=tk.W)
        
        asst_mgr_contact.bind("<Button-1>", lambda e: self.go_to_email(self.asst_contact_var))
        
        self.start_date_var = tk.StringVar()
        start_date_label = ttk.Label(mainframe, 
                                     text='Opening Date:',
                                     font=('TkDefaultFont', 12, 'bold'))
        start_date_label.grid(column=2, row=4, sticky=tk.E)
        
        start_date_display = ttk.Label(mainframe, 
                                       textvariable=self.start_date_var,
                                       font=('TkDefaultFont', 11))
        start_date_display.grid(column=3, row=4, sticky=tk.W)
        
        self.store_phone_var = tk.StringVar()
        store_phone_display = ttk.Label(mainframe, 
                                        textvariable=self.store_phone_var,
                                        font=('TkDefaultFont', 12))
        store_phone_display.grid(column=3, row=1, sticky=tk.W)
        
        self.store_address_var = tk.StringVar()
        store_address_display = ttk.Label(mainframe, 
                                          textvariable=self.store_address_var,
                                          font=('TkDefaultFont', 12))
        store_address_display.grid(column=4, row=1, sticky=tk.W)
        
        get_store_button = ttk.Button(mainframe, 
                                      text='Search', 
                                      style='Button.TButton', 
                                      command=self.set_store_info)
        get_store_button.grid(column=1, row=7, sticky=tk.W)
        
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
    
    def set_store_info(self):
        """Retrieve and display store information based on selected store number."""
        store_num = int(self.store_num_var.get())
        result_set = SusseWurstConnect.get_store_info(store_num, self.cxn)
        
        (store_name, store_address, store_phone, store_mgr, 
         mgr_contact, asst_mgr, asst_contact, start_date) = result_set[0]
        
        self.store_name_var.set(store_name)
        self.store_mgr_var.set(store_mgr)
        self.asst_mgr_var.set(asst_mgr)
        self.mgr_contact_var.set(mgr_contact)
        self.asst_contact_var.set(asst_contact)
        self.start_date_var.set(start_date)
        self.store_address_var.set(store_address)
        self.store_phone_var.set(store_phone)
        
        return None
    
    def go_to_email(self, email_address):
        """Open default email client to send email to provided address."""
        webbrowser.open_new_tab(f"mailto:{email_address.get()}")
        return None