import tkinter as tk
from tkinter import messagebox as message
import visa
import sys
import time
import datetime

master = tk.Tk()

master.title("NBI: IV / CV scan")
frame = tk.Frame(master, bg='pink')
frame.grid(row=1, rowspan = 3, column=1, columnspan = 5, sticky = tk.W+tk.E)

tk.Label(master, text="MODULE TESTING", font='Helvetica 18 bold').grid(row=0, column=1, columnspan = 6, sticky = tk.W+tk.E, pady=4)

#-----------------------------------------------------------------------------#
##   User   ##

tk.Label(frame, text="User:", bg='pink').grid(row=1, column=1, pady=15)
e4 = tk.Entry(frame, width=10, bg='DarkSeaGreen1')
e4.grid(row=1, column=2)
e4.insert(10,"cern")   #Starting username

#-----------------------------------------------------------------------------#
##   Set measurement type   ##

tk.Label(frame, text="Measurement type:", bg='pink').grid(row=2, column=1)
var = tk.IntVar()
CVoltage = tk.Radiobutton(frame, text = "CV", variable = var, value = 1, bg='pink').grid(row=2, column=2)
IVoltage = tk.Radiobutton(frame, text = "IV", variable = var, value = 2, bg='pink').grid(row=2, column=3)
var.set(2)

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
   call = message.showinfo( "Instructions", "Please insert your username, measurement type and Voltage settings. \nAdditional setting options are set at default values.\nPlease note to stop data readings, press cmd+C, cmd+., or equivalent in the terminal and then click ABORT in order to safely reduce the power source voltage down to zero.")
   return call
help_buttn = tk.Button(master, text = "Help", command = HelpCallBack).grid(row=0, 
             column=7, sticky=tk.W, pady=1, padx=4)

#-----------------------------------------------------------------------------#
##   RUN_IV   //     Configure    ##

def msg(x):
    return "[%s] %s" % (datetime.datetime.now().strftime("%H:%M:%S"), x)

def ramp(smu, v_end, speed):
    v = int(float(smu.query(':SOUR:VOLT?'))) # v now
    if v < v_end: # ramp up
        while v < v_end:
            v += 1
            time.sleep(int(speed))
            print (msg("ramping voltage to %s V" % v))
            smu.write(':SOUR:VOLT %s' % v)
    if v > v_end: # ramp down
        while v > v_end:
            v -= 1
            time.sleep(int(speed))
            print (msg("ramping voltage to %s V" % v))
            smu.write(':SOUR:VOLT %s' % v)
            
def Configure():
        call = message.showinfo( "Configuration", "VALUES CHOSEN \n\nUser: %s \nMeasurement type: %s \nStart Voltage: %s \nEnd Voltage: %s\nStep Size: %s \n \nADDITIONAL SETTINGS \nSweep Back: %s \nTerminals: %s \nNPLC: %s \nOutput Filename: %s \nNo. of Measurements: %s \nTime Delay: %s \nMeasurement Speed: %s \nRamp Speed: %s" % (e4.get(), calcmeastype(), e1.get(), e2.get(), e3.get(), sweepback_val(), terminal_val(), e5.get(), e6.get(), e7.get(), e8.get(), e9.get(), e10.get() ))
        return call

rm = visa.ResourceManager()
smu = rm.open_resource("ASRL/dev/cu.usbserial-FT0KNCGK::INSTR")

### configure the smu
def init():
    smu.baud_rate = 9600
    smu.timeout = None
    
    smu.write('*RST')
    smu.write(':SOUR:FUNC VOLT')
    smu.write(':SOUR:VOLT:MODE FIXED')
    smu.write(':SOUR:VOLT:PROT 500')
    smu.write(':SOUR:VOLT:RANG MAX')
    smu.write(':SENS:FUNC "CURR"')
    smu.write(':SENS:CURR:PROT 2E-8')
    smu.write(':SENS:CURR:RANG MIN')
    smu.write(':SENS:CURR:NPLC %s' % e5.get())
    if terminal_val() is "rear":      #check
        smu.write(':ROUT:TERM REAR')
    smu.write(':FORM:ELEM VOLT, CURR')
    pass

def volt_list():
    list_volt = []
    x = int(e1.get())
    
    ## change to have this in pop up config ##
    if int(e3.get()) <= 0:
        sys.exit("step size must be > 0")
        
    if int(e1.get()) < int(e2.get()):
        while x <= int(e2.get()):
            list_volt.append(x)
            x = (x + int(e3.get()))
    else:
        while x >= int(e2.get()):  
            list_volt.append(x)
            x = (x - int(e3.get()) )
    
    if sweepback_val() is "ON":   #check
        list_volt += list_volt[:-1][::-1]
    return list_volt

def config(): 
    Data = [e1.get(), e2.get(), e3.get()]
    for i in range(3):
        D = Data[i]
        try :
            int(D)
        except ValueError :
            def Error():
                call = message.showinfo( "Error", "Only use integers for Voltage settings")
                return call
            Error()
            return

    Configure()
    init()
    volt_list()
    pass

config_buttn = tk.Button(master, text='Configure', command=config).grid(row=10, 
                        column=2, sticky=tk.W, pady=15, padx=5)
#-----------------------------------------------------------------------------#
##   RUN_IV   //     Start / Abort    ##

def start():
    smu.write(':OUTP ON')
    raw_data = []
    for x in volt_list():
        print (msg("preparing for measurement(s) at %s V" % x))
        ramp(smu, x, int(e10.get()))
        time.sleep(int(e8.get()))
        for n in range(int(e7.get())):
            print (msg("taking measurement"))
            data_str = "%s,%s" % (datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), smu.query(':READ?'))
            raw_data.append(data_str)
            time.sleep(int(e9.get()))
    ramp(smu, 0, int(e10.get()))# ramp down to 0 V
    smu.write(':OUTP OFF')
    
    #write text file
    def text():
        text_file = open(e6.get()+".text","w")
        text_file.write("Name: %s\n" % e4.get()) 
        text_file.write("Arguments: Measurement type= %s, Start Voltage: %s, End Voltage: %s, Step Size: %s, Sweep Back: %s, Terminals: %s, NPLC: %s, No. of Measurements: %s, Time Delay: %s, Measurement Speed: %s, Ramp Speed: %s \n\n" % (calcmeastype(), e1.get(), e2.get(), e3.get(), sweepback_val(), terminal_val(), e5.get(), e7.get(), e8.get(), e9.get(), e10.get() )) 
        text_file.write("%-10s %-8s  %-13s  %-13s\n" % ("Date","Time","Voltage [V]","Current [I]"))
        for y in raw_data:
            y = y.replace(",","  ")
            text_file.write(y)
        text_file.close()
        return text_file
    text()
    
    ### NEW ABORT CODE.....a start
    
 #   if KeyboardInterrupt:
#        print ("aborted", datetime.now())
 #       ramp(smu, 0, int(e10.get()))
  #      smu.write(':OUTP OFF')
 #   else:
 #       pass
    pass

def abort():
    print ("aborted")
    ramp(smu, 0, int(e10.get()))
    smu.write(':OUTP OFF')
    #sys.exit(0)
    pass


start_buttn = tk.Button(master, text="START", command=start, bg="green").grid(row=10, 
                       column=3, sticky=tk.W, pady=15, padx=5)

abort_buttn = tk.Button(master, text="ABORT", command=abort, bg="red").grid(row=10, 
                       column=4, sticky=tk.W, pady=15, padx=5)

tk.Label(master, text="To stop data readings use KeyboardInterrupt and immediately click ABORT", bg='lightgoldenrod').grid(row=10, rowspan=3, column=5, columnspan=4)

#-----------------------------------------------------------------------------#
master.mainloop()