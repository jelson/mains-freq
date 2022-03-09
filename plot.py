#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot(df):
    # plot timeseries
    fig, ax = plt.subplots(figsize=(20, 10))
    df.plot(
        ax=ax,
        x='time',
        y=['freq'],
        grid=True,
    )
    fig.savefig(f"{df.attrs['filename']}.timeseries.png")

    # plot histogram
    fig, ax = plt.subplots(figsize=(20, 10))
    df['freq'].hist(
        ax=ax,
        bins=40,
        grid=True,
        rwidth=0.9,
    )
    fig.savefig(f"{df.attrs['filename']}.hist.png")

def read(filename):
    df = pd.read_csv(filename, header=None)
    df = df.rename({0: 'time', 1: 'freq'}, axis=1)
    df['time'] = pd.to_datetime(df['time'], unit='s').dt.tz_localize('UTC')
    df['time'] = df['time'].dt.tz_convert('US/Pacific')
    df.attrs['filename'] = filename
    return df
    
def main():
    if len(sys.argv) != 2:
        print("provide input filename as argument")
        sys.exit(1)

    df = read(sys.argv[1])
    print(df)
    plot(df)

if __name__ == "__main__":
    main()
    
