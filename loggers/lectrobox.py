#!/usr/bin/env python3

import argparse
import os
import serial
import sys
import time

def _read(portname, outfile):
    timestamper = serial.Serial(portname, 1000000)
    prev_timestamp = None
    prev_print_time = None

    while True:
        line = timestamper.readline()
        now = time.time()
        line = line.decode('ascii', errors='ignore').strip()
        (channel, timestamp) = line.split()
        if outfile:
            outfile.write(f"{now:.6f} {timestamp}\n")

        timestamp = float(timestamp)
        if prev_timestamp:
            freq = 1 / (timestamp - prev_timestamp)
            if not prev_print_time or int(now) > int(prev_print_time):
                sys.stdout.write(f"{now:.6f} {freq:.9}\n")
                sys.stdout.flush()
                if outfile:
                    outfile.flush()
                prev_print_time = now
        prev_timestamp = timestamp

def read(portname, outfilename):
    if outfilename:
        if os.path.exists(outfilename):
            sys.exit(f"FATAL: {outfilename} already exists")

        outfile = open(outfilename, "w")
    else:
        outfile = None

    while True:
        try:
            _read(portname, outfile)
        except Exception as e:
            print(f"error: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--device',
        help='Serial port to read',
        default='/dev/ttyUSB0',
    )
    parser.add_argument(
        '--no-write',
        help='Print to screen only, do not generate output file',
        action='store_true',
    )
    args = parser.parse_args(sys.argv[1:])

    if args.no_write:
        fn = None
    else:
        fn = f"mains_freq_{int(time.time())}.txt"
    read(args.device, fn)

if __name__ == "__main__":
    main()
    
