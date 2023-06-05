#!/usr/bin/python3

import argparse
import csv
import matplotlib.pyplot as plt
import toml

def main(logfile: str, cfgfile: str):
    # read the csv
    data = dict()
    with open(logfile, "r") as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            for key in row:
                try:
                    val = int(row[key])
                except ValueError:
                    try:
                        val = float(row[key])
                    except:
                        # screw it, must be a string
                        val = row[key]
                if key not in data:
                    data[key] = [val]
                else:
                    data[key].append(val)

    # read the config
    with open(cfgfile, "r") as fin:
        cfg = toml.load(fin)

    # plot!
    for w in cfg:
        fig, axes = plt.subplots(len(cfg[w]), sharex=True)
        axes[-1].set_xlabel("time [s]")
        fig.suptitle(w)
        for i, s in enumerate(cfg[w]):
            axes[i].set_ylabel(s)
            for t in cfg[w][s]:
                axes[i].plot(data["time"], data[t])
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="AltOS Postflight Plotter",
    )
    parser.add_argument("logfile")
    parser.add_argument("cfgfile")
    args = parser.parse_args()

    main(
        logfile=args.logfile,
        cfgfile=args.cfgfile
    )
