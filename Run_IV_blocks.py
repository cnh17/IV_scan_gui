import visa
import sys
import time
import datetime
from panel import e1, e2, e3, e4, e5, e6, calcmeastype, sweepback_val, terminal_val

###############################################################################
# MESSAGING
###############################################################################
### function to print with timestamp
def msg(x):
    return "[%s] %s" % (datetime.datetime.now().strftime("%H:%M:%S"), x)

###############################################################################
# RAMPING
###############################################################################
### function to ramp voltage up/down
def ramp(smu, v_end, speed):
    v = int(float(smu.query(':SOUR:VOLT?'))) # v now
    if v < v_end: # ramp up
        while v < v_end:
            v += 1
            time.sleep(speed)
            print (msg("ramping voltage to %s V" % v))
            smu.write(':SOUR:VOLT %s' % v)
    if v > v_end: # ramp down
        while v > v_end:
            v -= 1
            time.sleep(speed)
            print (msg("ramping voltage to %s V" % v))
            smu.write(':SOUR:VOLT %s' % v)

###############################################################################
### parse the given script arguments
#parser = argparse.ArgumentParser()

# required arguments
#parser.add_argument("start", type=int)
#parser.add_argument("stop",  type=int)
#parser.add_argument("step",  type=int)

# optional arguments
#parser.add_argument("--number_meas", type=  int, default=10)
#parser.add_argument("--time_delay",  type=float, default=10)
#parser.add_argument("--meas_speed",  type=float, default= 1)
#parser.add_argument("--ramp_speed",  type=float, default= 1)
#parser.add_argument("--sweep_back",  action="store_true") #take vlaues on way back
#parser.add_argument("--rear_terms",  action="store_true") #say if front or back terminals used
#parser.add_argument("--NPLC",        default="1") #no. of power line cycles
#parser.add_argument("--output_name", default="output") #for text file

#args = parser.parse_args()

### sanity checks - just to be sure!
#ok = raw_input("are you sure you want to continue? [Y/N]\n")
#if ok != "Y":
#    sys.exit(0)


###############################################################################
# CONFIGURE
###############################################################################
### prepare a list of voltage points

def volt_list():
    list_volt = []
    x = e1.get()
    
    ## change to have this in pop up config ##
    if e3.get() <= 0:
        sys.exit("step size must be > 0")
        
    if e1.get() < e2.get():
        while x <= e2.get():
            list_volt.append(x)
            x = (x + e3.get())
    else:
        while x >= e2.get():  
            list_volt.append(x)
            x = (x - e3.get())
    
    if sweepback_val() is "ON":   #check
        list_volt += list_volt[:-1][::-1]
    pass

### configure the smu
def init():
    rm = visa.ResourceManager()
    smu = rm.open_resource("ASRL/dev/cu.usbserial-FT0KNCGK::INSTR")
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
    if terminal_val() is "rear":
        smu.write(':ROUT:TERM REAR')
    smu.write(':FORM:ELEM VOLT, CURR')
    pass

###############################################################################
# START
###############################################################################
### perform sweep and take readings

def start():
    smu.write(':OUTP ON')
    raw_data = []
    for x in list_volt:
        print (msg("preparing for measurement(s) at %s V" % x))
        ramp(smu, x, args.ramp_speed)
        time.sleep(args.time_delay)
        for n in range(args.number_meas):
            print (msg("taking measurement"))
            data_str = "%s,%s" % (datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), smu.query(':READ?'))
            raw_data.append(data_str)
            time.sleep(args.meas_speed)
    ramp(smu, 0, args.ramp_speed) # ramp down to 0 V
    smu.write(':OUTP OFF')
    
    #write text file
    def text():
        text_file = open(args.output_name+".text","w")
        text_file.write("name: %s\n" % sys.argv[0]) 
        text_file.write("args: %s\n\n" % args) 
        text_file.write("%-10s %-8s  %-13s  %-13s\n" % ("Date","Time","Voltage [V]","Current [I]"))
        for x in raw_data:
            x = x.replace(",","  ")
            text_file.write(x)
            text_file.close()
        pass
    pass

###############################################################################
# ABORT
###############################################################################
def abort():
    print (" aborted")
    ramp(smu, 0, args.ramp_speed)
    smu.write(':OUTP OFF')
#    sys.exit(0)
    pass

###############################################################################
# WRITE OUTPUT
###############################################################################
### write the results to a text file

#def text():
#    text_file = open(args.output_name+".text","w")
 #   text_file.write("name: %s\n" % sys.argv[0]) 
 ##   text_file.write("args: %s\n\n" % args) 
  #  text_file.write("%-10s %-8s  %-13s  %-13s\n" % ("Date","Time","Voltage [V]","Current [I]"))
 #   for x in raw_data:
 ##       x = x.replace(",","  ")
 #       text_file.write(x)
 #   text_file.close()
 #   pass






