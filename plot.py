#!/usr/bin/env python3

import matplotlib.pyplot as plt
import os
import pandas as pd
import pathlib
import sys

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

def compare(dfs):
    # Rename each 'freq' column to have a unique name based on the
    # original file's filename
    colnames = []
    for i, df in enumerate(dfs):
        newcolname = pathlib.Path(df.attrs['filename']).stem
        colnames.append(newcolname)
        dfs[i] = df.rename({'freq': newcolname}, axis=1)

    # Merge all the dataframes
    merged = dfs[0]
    for df in dfs[1:]:
        merged = pd.merge_asof(
            left=merged,
            right=df,
            on='time',
            direction='nearest',
            tolerance=pd.Timedelta('5s'),
        )

    # Drop the non-matching rows and apply a rolling average
    merged = merged.dropna()
    for col in colnames:
        merged[col] = merged[col].rolling(30, center=True).mean()

    # Plot the portions that match
    fig, ax = plt.subplots(figsize=(20, 10))
    merged.plot(
        ax=ax,
        x='time',
        y=colnames,
        grid=True,
    )
    ax.set(
        xlabel="Time",
        ylabel="Frequency (hz)",
    )
    fig.tight_layout()
    fn = f"comparison-{'-'.join(colnames)}-timeseries.png"
    fig.savefig(fn)
    print(f"Wrote {fn}")

    # compute differences
    diffs = merged[colnames[0]] - merged[colnames[1]]
    diffs = diffs.dropna()
    # Plot the portions that match
    fig, ax = plt.subplots(figsize=(20, 10))
    diffs.plot(
        ax=ax,
        x='time',
        grid=True,
    )
    ax.set(
        xlabel="Time",
        ylabel=f"Frequency Difference Between {colnames[0]} and {colnames[1]}",
    )
    fig.tight_layout()
    fn = f"freqdiff-{'-'.join(colnames)}-timeseries.png"
    fig.savefig(fn)
    print(f"Wrote {fn}")

def read(filename):
    df = pd.read_csv(filename, header=None)
    df = df.rename({0: 'time', 1: 'freq'}, axis=1)
    df['time'] = pd.to_datetime(df['time'], unit='s').dt.tz_localize('UTC')
    df['time'] = df['time'].dt.tz_convert('US/Pacific')
    df.attrs['filename'] = filename
    return df

def main():
    if len(sys.argv) == 1:
        print("provide input filename as argument, or more than one to compare")
        sys.exit(1)

    elif len(sys.argv) == 2:
        df = read(sys.argv[1])
        print(df)
        plot(df)

    else:
        dfs = [read(fn) for fn in sys.argv[1:]]
        compare(dfs)

if __name__ == "__main__":
    main()
