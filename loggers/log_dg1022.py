#!/usr/bin/env python3

import pyvisa
import time
import datetime
import sys
#'USB0::1024::2500::DG1F151200301\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00::0::INSTR'

#pyvisa.log_to_screen()

rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())

inst = rm.open_resource('USB0::1024::2500::DG1F151200301*::0::INSTR', open_timeout=1)

inst.timeout = 5000

def myQ(q):
    inst.write(q)
    time.sleep(0.1)
    rv = inst.read()
    time.sleep(0.1) 
    return rv.strip()

def myW(m):
    inst.write(m)
    time.sleep(0.1)

print(myQ("*IDN?"))

#myW('FUNC RAMP')
#myW('APPLY:SIN 1000,1,1')
myW('OUTP OFF')
myW('OUTP:CH2 OFF')
myW('COUN ON')
myW('COUN:COUP AC')
print(myQ('COUN:COUP?'))
myW('COUN:SENS LOW')
print(myQ('COUN:SENS?'))
myW('COUN:TLEV 71')
print(myQ('COUN:TLEV?'))
myW('COUN:HFRS ON')
print(myQ('COUN:HFRS?'))
print(myQ('COUN:FREQ?'))

with open("data.txt", "a") as ofh:
    last_freq = 'boop'
    while True:
        freq = myQ('COUN:FREQ?')
        if freq != last_freq:
            out = f'{time.time()},{freq}\n'
            sys.stdout.write(out)
            ofh.write(out)
            last_freq = freq


