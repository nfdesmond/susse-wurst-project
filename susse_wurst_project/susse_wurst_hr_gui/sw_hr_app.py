"""
TITLE: Süsse Wurst HR Application
AUTHOR: N.F. Desmond
DATE: November 2025
DESCRIPTION: This is the main module for running the Süsse Wurst HR application. 
It establishes a connection to the HR database and launches a GUI. From there, 
an HR associate can view employee and store information and onboard new hires into 
the system.
"""
import tkinter as tk
import sussewurstconnect.swconnect as swconnect
import sussewurstconnect.swconfig as swconfig
import hr_guis.hrgogui as hrgui

def main():
    """Establishes a connection to the Süsse Wurst HR database and launches the HR GUI application."""
    hr_app = swconnect.SusseWurstConnect('sw_hr')
    
    hr_cxn = hr_app.mysql_connect(swconfig.USER, swconfig.PSWD, use_pure_flag=True)

    if hr_app.cxn_test(hr_cxn):
        root = tk.Tk()
        hr_gui = hrgui.HRGui(root, hr_cxn)
        root.mainloop()
    
    if not root.mainloop():
        hr_cxn.close()

    if hr_app.cxn_test(hr_cxn):
        print('You are online with the Süsse Wurst HR database.')
    else:
        print('Database connection has been closed.')
        
    
if __name__ == '__main__':
    main()