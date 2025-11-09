import tkinter as tk
from tkinter import ttk
from sw_db_application.sussewurstconnect.swconnect import SusseWurstConnect

class StoreLookupGUI:
    def __init__(self, root, cxn):
        root.title("Süsse Wurst HR GO Store Lookup")
        root.geometry('400x200')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.cxn = cxn

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        store_list_label = ttk.Label(mainframe, text='Select a store number')
        store_list_label.grid(column=1, row=1, sticky=tk.W)
        
        store_nums = SusseWurstConnect.get_store_number(cxn)
        
        self.store_num_var = tk.StringVar()
        store_list = ttk.Combobox(mainframe, textvariable=self.store_num_var, values=store_nums)
        store_list.grid(column=1, row=2, sticky=tk.W)
        
        
        self.store_name_var = tk.StringVar()
        store_name_label = ttk.Label(mainframe, textvariable=self.store_name_var)
        store_name_label.grid(column=2, row=1, sticky=tk.EW)
        
        self.store_mgr_var = tk.StringVar()
        store_mgr_label = ttk.Label(mainframe, text='Store Manager:')
        store_mgr_label.grid(column=2, row=2, sticky=tk.E)
        
        store_mgr_display = ttk.Label(mainframe, textvariable=self.store_mgr_var)
        store_mgr_display.grid(column=3, row=2, sticky=tk.W)
        
        self.mgr_contact_var = tk.StringVar()
        store_mgr_contact = ttk.Label(mainframe, textvariable=self.mgr_contact_var)
        store_mgr_contact.grid(column=4, row=2,sticky=tk.W)
        
        self.asst_mgr_var = tk.StringVar()
        asst_mgr_label = ttk.Label(mainframe, text='Assistant Manager:')
        asst_mgr_label.grid(column=2, row=3, sticky=tk.E)
        
        asst_mgr_display = ttk.Label(mainframe, textvariable=self.asst_mgr_var)
        asst_mgr_display.grid(column=3, row=3, sticky=tk.W)
        
        self.asst_contact_var = tk.StringVar()
        asst_mgr_contact = ttk.Label(mainframe, textvariable=self.asst_contact_var)
        asst_mgr_contact.grid(column=4, row=3, sticky=tk.W)
        
        self.start_date_var = tk.StringVar()
        start_date_label = ttk.Label(mainframe, text='Opening Date:')
        start_date_label.grid(column=2, row=4, sticky=tk.E)
        
        start_date_display = ttk.Label(mainframe, textvariable=self.start_date_var)
        start_date_display.grid(column=3, row=4, sticky=tk.W)
        
        self.store_phone_var = tk.StringVar()
        store_phone_display = ttk.Label(mainframe, textvariable=self.store_phone_var)
        store_phone_display.grid(column=3, row=1, sticky=tk.W)
        
        self.store_address_var = tk.StringVar()
        store_address_display = ttk.Label(mainframe, textvariable=self.store_address_var)
        store_address_display.grid(column=4, row=1, sticky=tk.W)
        
        get_store_button = ttk.Button(mainframe, text='Search', command=self.set_store_info)
        get_store_button.grid(column=1, row=7, sticky=tk.W)
        
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
    
    def set_store_info(self):
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