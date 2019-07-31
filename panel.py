import tkinter as tk
from tkinter import messagebox as msg
#import Run_IV.py as Run
import sys
import subprocess
import numpy as np

master = tk.Tk()

master.title("NBI: IV / CV scan")
#master.geometry('1000x600')
frame = tk.Frame(master, bg='pink')
frame.grid(row=1, rowspan = 3, column=1, columnspan = 5, sticky = tk.W+tk.E)

tk.Label(master, text="MODULE TESTING", font='Helvetica 18 bold').grid(row=0, column=2, columnspan = 2, sticky = tk.W+tk.E, pady=4)

#-----------------------------------------------------------------------------#
##   User   ##

tk.Label(frame, text="User:", bg='pink').grid(row=1, column=1, pady=15)
e4 = tk.Entry(frame, width=10, bg='DarkSeaGreen1')
e4.grid(row=1, column=2)

#-----------------------------------------------------------------------------#
##   Set measurement type   ##

tk.Label(frame, text="Measurement type:", bg='pink').grid(row=2, column=1)
var = tk.IntVar()
CVoltage = tk.Radiobutton(frame, text = "CV", variable = var, value = 1, bg='pink').grid(row=2, column=2)
IVoltage = tk.Radiobutton(frame, text = "IV", variable = var, value = 2, bg='pink').grid(row=2, column=3)

def calcmeastype():
    if var.get() > 1.5:
        MeasType = 'IV'
    else:
        MeasType = 'CV'
    return MeasType

#-----------------------------------------------------------------------------#
##   Voltage    ##

tk.Label(frame, text="Voltage:", bg='pink').grid(row=3, column=1)
tk.Label(frame, text="V       to", bg='pink').grid(row=3, column=3)
tk.Label(frame, text="V        Step size:", bg='pink').grid(row=3, column=5)

e1 = tk.Entry(frame, width=10, bg='DarkSeaGreen1')
e2 = tk.Entry(frame, width=10, bg='DarkSeaGreen1')
e3 = tk.Entry(frame, width=10, bg='DarkSeaGreen1')      #(master, cnf{}, **kw)

##  Start values (could also be blank) ##
e1.insert(10, "0")
e2.insert(10,"2")
e3.insert(10, "1")
e4.insert(10,"cnh")
var.set(2) #start with IV scan

## Placing value boxes ##
e1.grid(row=3, column=2)
e2.grid(row=3, column=4)
e3.grid(row=3, column=6)

#-----------------------------------------------------------------------------#
##   Quit / reset / help Buttons    ##

def reset_defaults():
   e1.delete(0,tk.END)
   e2.delete(0,tk.END)
   e3.delete(0,tk.END)
   e4.delete(0,tk.END)
   e1.insert(10, "Start")
   e2.insert(10,"End")
   e3.insert(10,"1")
   e4.insert(10, "Name")
   var.set(2) #default set as IV scan

quit_buttn = tk.Button(master, text='Quit', command=master.quit).grid(row=0, column=0, 
         sticky=tk.W, pady=1, padx=1)

reset_buttn = tk.Button(master, text='Reset', command=reset_defaults).grid(row=0, column=8, 
         sticky=tk.W, pady=1, padx=1)

def HelpCallBack():
   call = msg.showinfo( "Instructions", "Please insert your username, measurement type and Voltage settings.")
   return call
help_buttn = tk.Button(master, text = "Help", command = HelpCallBack).grid(row=0, 
             column=7, sticky=tk.W, pady=1, padx=4)

#-----------------------------------------------------------------------------#
##   Configure / Start / Abort    ##

def config(): 
    Data = [e1.get(), e2.get(), e3.get()]
    for i in range(3):
        D = Data[i]
        try :
            int(D)
        except ValueError :
            def Error():
                call = msg.showinfo( "Error", "Only use integers for Voltage settings")
                return call
            Error()
            return

    def Configure():
        call = msg.showinfo( "Configuration", "VALUES CHOSEN \n\nUser: %s \nMeasurement type: %s \nStart Voltage: %s \nEnd Voltage: %s\nStep Size: %s" % (e4.get(), calcmeastype(), e1.get(), e2.get(), e3.get()))
        return call
    Configure()
    pass
config_buttn = tk.Button(frame, text='Configure', command=config).grid(row=5, column=2, sticky=tk.W, pady=4, padx=4)

def start():    
    subprocess.call(['python', 'Run_IV.py', e1.get(), e2.get(), e3.get()])
    #show should be float, dont allow letters
    #show on screen that system is running by a pop up? that could show how long it will take and if it is running properly.
    pass
start_buttn = tk.Button(frame, text="START", command=start, bg="green").grid(row=5, 
                       column=3, sticky=tk.W, pady=15, padx=5)

def abort():
    sys.exit(0)
    #produce message showing it is aborting
    pass
abort_buttn = tk.Button(frame, text="ABORT", command=abort, bg="red").grid(row=5, column=4, sticky=tk.W, pady=15, padx=5)

#-----------------------------------------------------------------------------#
master.mainloop()




