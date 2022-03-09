#!/usr/bin/env python3

import pyvisa
import sys
import time

def get_instr():
    rm = pyvisa.ResourceManager()
    instrs = rm.list_resources()
    print(f"All instruments: {instrs}")
    usb_instrs = [i for i in instrs if 'USB' in i]
    print(f"USB instruments: {usb_instrs}")
    if len(usb_instrs) != 1:
        print("can't find right instrument")
        sys.exit(1)
    instr = rm.open_resource(usb_instrs[0])
    del instr.timeout
    print(instr.query("*IDN?"))
    return instr

def main():
    instr = get_instr()
    with open("data.txt", "a") as outfile:
        while True:
            val = instr.query("MEAS:FREQ?")
            out = f"{time.time()},{val}"
            sys.stdout.write(out)
            outfile.write(out)

if __name__ == "__main__":
    main()
