import os
import argparse
import re
import time
from os.path import exists

chunksize = 128
throughput_filename = "throughput.log"

def run_benchmark(net_n=16, net_k=2, loc_n=8, loc_k=2):
    """
    Runs ISA-L code for throughput calculation.
    """
    os.system(f"cd isa-l; ../run_benchmark.sh -a {net_n} -b {net_k} -n {loc_n} -k {loc_k} -c {chunksize} -m i -f {throughput_filename} -e m; cd ..")

def point_throughput():
    """
    Reads throughput file and returns throughput value.
    """
    with open("./isa-l/" + throughput_filename, "r") as f:
        lines = f.readlines()
    for key, line in enumerate(lines):
        if ("Overall Throughput" in line):
            desired_line = lines[key].split("Overall Throughput: ")[1].split(" MB/s")[0]
    throughput = float(re.sub("[^0-9.]", "", desired_line))
    return throughput

def throughput_test():
    """
    Measures throughput performance.
    """
    print("Calculating Throughput...\n")
    run_benchmark()
    before = point_throughput()

    print("Compiling...\n")
    os.system("cd isa-l; make perfs; cd ..")

    print("\nCalculating Throughput...\n")
    run_benchmark()
    after = point_throughput()

    difference = after - before
    if (before == 0):
        change = 0
    else:
        change = (difference / before) * 100

    print("Old Throughput: " + str(before) + " MB/s\n")
    print("New Throughput: " + str(after) + " MB/s\n")

    if (difference >= 0):
        print("Difference in Throughput: +" + "{:.2f}".format(difference) + " MB/s\n")
        print("Percent Increase in Throughput: +" + "{:.4f}".format(change) + "%\n")
    else:
        print("Difference in Throughput: " + "{:.2}".format(difference) + " MB/s\n")
        print("Percent Increase in Throughput: " + "{:.4f}".format(change) + "%\n")

def main():
    throughput_test()

if __name__ == "__main__":
    main()