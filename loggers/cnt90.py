#!/usr/bin/env python3

import pyvisa
import sys
import time

# VISA instrument id for CNT-90
INSTR_ID = "5355::144"

def get_instr():
    rm = pyvisa.ResourceManager()
    instrs = rm.list_resources()
    print(f"All instruments: {instrs}")
    matches = [i for i in instrs if INSTR_ID in i]
    if len(matches) != 1:
        print(f"can't find right instrument with ID {INSTR_ID}")
        sys.exit(1)
    instr_name = matches[0]
    print(f"Instrument found: {instr_name}")
    instr = rm.open_resource(instr_name)
    del instr.timeout
    print(instr.query("*IDN?"))
    return instr

def main():
    if not len(sys.argv) == 2:
        print(f"Usage: {sys.argv[0]} logfile-prefix")
        sys.exit(1)

    fn = f"{sys.argv[1]}_{round(time.time())}.csv"
    print(f"Writing to {fn}")

    instr = get_instr()
    with open(fn, "a") as outfile:
        while True:
            val = instr.query("MEAS:FREQ?").strip()
            out = f"{time.time():.6f},{val}\n"
            sys.stdout.write(out)
            outfile.write(out)

if __name__ == "__main__":
    main()
