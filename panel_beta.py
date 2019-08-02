import tkinter as tk
from tkinter import messagebox as msg
#import Run_IV.py as Run
import sys
import subprocess

master = tk.Tk()

master.title("NBI: IV / CV scan")
#master.geometry('1000x600')
frame = tk.Frame(master, bg='pink')
frame.grid(row=1, rowspan = 3, column=1, columnspan = 5, sticky = tk.W+tk.E)

tk.Label(master, text="MODULE TESTING", font='Helvetica 18 bold').grid(row=0, column=1, columnspan = 6, sticky = tk.W+tk.E, pady=4)

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
var.set(2)

## Placing value boxes ##
e1.grid(row=3, column=2)
e2.grid(row=3, column=4)
e3.grid(row=3, column=6)

#-----------------------------------------------------------------------------#
##   Additional settings / column left  ##

tk.Label(frame, text="Additional Settings (Default values set)", font='Helvetica 14 bold').grid(row=4, column=1, columnspan = 6, sticky = tk.W+tk.E, pady=4)

## SWEEP BACK
tk.Label(frame, text="Sweep back:", bg='pink').grid(row=5, column=1)
var2 = tk.IntVar()
OFF = tk.Radiobutton(frame, text = "OFF", variable = var2, value = 1, bg='pink').grid(row=5, column=2)
ON = tk.Radiobutton(frame, text = "ON", variable = var2, value = 2, bg='pink').grid(row=5, column=3)
var2.set(1)

def sweepback_val():
    if var2.get() > 1.5:
        MeasType = 'ON'
    else:
        MeasType = 'OFF'
    return MeasType

## TERMINALS
tk.Label(frame, text="Terminals:", bg='pink').grid(row=6, column=1)
var3 = tk.IntVar()
OFF = tk.Radiobutton(frame, text = "front", variable = var3, value = 1, bg='pink').grid(row=6, column=2)
ON = tk.Radiobutton(frame, text = "rear", variable = var3, value = 2, bg='pink').grid(row=6, column=3)
var3.set(1)

def terminal_val():
    if var3.get() > 1.5:
        MeasType = 'rear'
    else:
        MeasType = 'front'
    return MeasType

## NPLC
tk.Label(frame, text="NPLC:", bg='pink').grid(row=7, column=1)
e5 = tk.Entry(frame, width=10, bg='DarkSeaGreen1') 
e5.insert(10,"1")
e5.grid(row=7, column=2)

## Output Filename ##
tk.Label(frame, text="Output filename:", bg='pink').grid(row=8, column=1)
e6 = tk.Entry(frame, width=10, bg='DarkSeaGreen1') 
e6.insert(10,"output")
e6.grid(row=8, column=2)

#-----------------------------------------------------------------------------#
##   Additional settings / column right  ##

## no. of Measurements
tk.Label(frame, text="No. of Measurements:", bg='pink').grid(row=5, column=4, columnspan=2, sticky=tk.E)
e7 = tk.Entry(frame, width=10, bg='DarkSeaGreen1') 
e7.insert(10,"10")
e7.grid(row=5, column=6)

## time delay
tk.Label(frame, text="Time Delay:", bg='pink').grid(row=6, column=5)
e8 = tk.Entry(frame, width=10, bg='DarkSeaGreen1') 
e8.insert(10,"10")
e8.grid(row=6, column=6)

## Measurement speed
tk.Label(frame, text="Measurement Speed:", bg='pink').grid(row=7, column=4, columnspan=2, sticky=tk.E)
e9 = tk.Entry(frame, width=10, bg='DarkSeaGreen1') 
e9.insert(10,"1")
e9.grid(row=7, column=6)

## ramp speed
tk.Label(frame, text="Ramp Speed:", bg='pink').grid(row=8, column=5)
e10 = tk.Entry(frame, width=10, bg='DarkSeaGreen1') 
e10.insert(10,"1")
e10.grid(row=8, column=6)

#-----------------------------------------------------------------------------#
##   Quit / reset / help Buttons    ##

def reset_defaults():
   e1.delete(0,tk.END)
   e2.delete(0,tk.END)
   e3.delete(0,tk.END)
   e4.delete(0,tk.END)
   e5.delete(0,tk.END)
   e6.delete(0,tk.END)
   e7.delete(0,tk.END)
   e8.delete(0,tk.END)
   e9.delete(0,tk.END)
   e10.delete(0,tk.END)
   e1.insert(10, "Start")  #start voltage
   e2.insert(10,"End")     #end voltge
   e3.insert(10,"1")       #V step size
   e4.insert(10, "Name")   #username
   e5.insert(10, "1")      #NPLC
   e6.insert(10, "output") #text file name
   e7.insert(10, "10")     #no. of measurements
   e8.insert(10, "10")     #time delay
   e9.insert(10, "1")      #measurement speed
   e10.insert(10, "1")     #ramp speed
   var.set(2)              #IV default
   var2.set(1)             #sweep back off default
   var3.set(1)             #front terminal default

quit_buttn = tk.Button(master, text='Quit', command=master.quit).grid(row=0, column=0, 
         sticky=tk.W, pady=1, padx=1)

reset_buttn = tk.Button(master, text='Reset', command=reset_defaults).grid(row=0, column=8, 
         sticky=tk.W, pady=1, padx=1)

def HelpCallBack():
   call = msg.showinfo( "Instructions", "Please insert your username, measurement type and Voltage settings. Additional setting options are set at default values.")
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
        call = msg.showinfo( "Configuration", "VALUES CHOSEN \n\nUser: %s \nMeasurement type: %s \nStart Voltage: %s \nEnd Voltage: %s\nStep Size: %s \n \nADDITIONAL SETTINGS \nSweep Back: %s \nTerminals: %s \nNPLC: %s \nOutput Filename: %s \nNo. of Measurements: %s \nTime Delay: %s \nMeasurement Speed: %s \nRamp Speed: %s" % (e4.get(), calcmeastype(), e1.get(), e2.get(), e3.get(), sweepback_val(), terminal_val(), e5.get(), e6.get(), e7.get(), e8.get(), e9.get(), e10.get() ))
        return call
    Configure()
    pass
config_buttn = tk.Button(master, text='Configure', command=config).grid(row=10, column=2, sticky=tk.W, pady=4, padx=4)

def start():    
    subprocess.call(['python', 'Run_IV.py', e1.get(), e2.get(), e3.get()])
    #subprocess.Popen(["python", "RUN_IV.py", e1.get(), e2.get(), e3.get()])
    #show should be float, dont allow letters
    #show on screen that system is running by a pop up? that could show how long it will take and if it is running properly.
    pass
start_buttn = tk.Button(master, text="START", command=start, bg="green").grid(row=10, 
                       column=3, sticky=tk.W, pady=15, padx=5)

def abort():
    #sys.exit(0)
    #produce message showing it is aborting
    pass
abort_buttn = tk.Button(master, text="ABORT", command=abort, bg="red").grid(row=10, column=4, sticky=tk.W, pady=15, padx=5)

#-----------------------------------------------------------------------------#
master.mainloop()




