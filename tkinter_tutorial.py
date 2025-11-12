import tkinter as tk
import sw_db_application.sussewurstconnect.swconnect as swconnect
import sw_db_application.sussewurstconnect.swconfig as swconfig
from employeelookupgui import EmployeeLookupGUI
from storelookupgui import StoreLookupGUI
from onboardgui import EmployeeOnboardGUI

hr_app = swconnect.SusseWurstConnect('susse_wurst_hr')

hr_cxn = hr_app.mysql_connect(swconfig.USER, swconfig.PSWD, use_pure_flag=True)

if hr_app.cxn_test(hr_cxn):

    root = tk.Tk()
    EmployeeLookupGUI(root, hr_cxn)
    # StoreLookupGUI(root, hr_cxn)
    # EmployeeOnboardGUI(root, hr_cxn)
    
    root.mainloop()
    
if not root.mainloop():
    hr_cxn.close()

if hr_app.cxn_test(hr_cxn):
    print('Still alive!')
else:
    print('The connection has been closed.')