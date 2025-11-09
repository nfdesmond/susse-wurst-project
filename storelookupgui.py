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
        
        store_num_var = tk.StringVar()
        store_list = ttk.Combobox(mainframe, textvariable=store_num_var, values=store_nums)
        store_list.grid(column=1, row=2, sticky=tk.W)
        
        
        store_name_var = tk.StringVar()
        store_name_label = ttk.Label(mainframe, textvariable=store_name_var)
        store_name_label.grid(column=2, row=1, sticky=tk.EW)
        
        store_mgr_var = tk.StringVar()
        store_mgr_label = ttk.Label(mainframe, text='Store Manager:')
        store_mgr_label.grid(column=2, row=2, sticky=tk.W)
        
        store_mgr_display = ttk.Label(mainframe, textvariable=store_mgr_var)
        store_mgr_display.grid(column=3, row=2, sticky=tk.W)
        
        mgr_contact_var = tk.StringVar()
        store_mgr_contact = ttk.Label(mainframe, textvariable=mgr_contact_var)
        store_mgr_contact.grid(column=4, row=2,sticky=tk.W)