import os
import argparse
import numpy as np
import seaborn as sns; sns.set_theme()
import matplotlib.pylab as plt
from matplotlib.colors import LinearSegmentedColormap
import re

max_n = 17
max_k = 3
mode = "i"
throughput_filename = "throughput"
heatmap_filename = "heatmap"

def run_benchmark(n, k):
    os.system("../run_benchmark.sh -n " + str(n) + " -k " + str(k) + " -m " + mode + " -f " + throughput_filename)

def create_array():
    array = [[np.nan for n in range(max_n + 1)] for k in range(max_k + 1)]
    return array

def generate_single_point(n, k, data):
    with open(throughput_filename) as f:
        lines = f.readlines()
    for key, line in enumerate(lines):
        if ((mode == "i") and ("runtime" in line)):
            desired_line = lines[key].split("in")[1].split("sec")[1].lstrip()
            desired_line = desired_line.split("=")[1].split("MB/s")[0]
            desired_line = desired_line.lstrip().rstrip()
        if ((mode == "j") and ("Summary:" in line)):
            desired_line = lines[key + 2]
    throughput = float(re.sub("[^0-9.]", "", desired_line))
    data[k+1][n+1] = throughput

def generate_data(data):
    if (mode == "i"):
        os.chdir("isa-l")
    else:
        os.chdir("JavaReedSolomon")

    for n in range(max_n):
        for k in range(max_k):
            print("Generating Data for: " + str(n+1) + "+" + str(k+1) + "\n")
            run_benchmark(n+1, k+1)
            generate_single_point(n, k, data)
            os.remove(throughput_filename)

def generate_heatmap(data):
    array = np.array(data, dtype=float)
    myColors = ("Black", "Purple", "Blue", "Red", "Pink", "Orange", "Yellow", "Green")
    cmap = LinearSegmentedColormap.from_list("Custom", myColors, len(myColors))
    mask = np.isnan(array)
    ax = sns.heatmap(array, cmap=cmap, mask=mask, linewidths=0.5, cbar_kws={"label": "Throughput (MB/s)"})

    # X-Y axis labels
    ax.set_ylabel("Parity Units K")
    ax.set_xlabel("Data Units N")
    ax.invert_yaxis()


def parse_args():
    global max_n
    global max_k
    global mode
    global throughput_filename
    global heatmap_filename
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="Number of data shards", default=max_n, type=int)
    parser.add_argument("-k", help="Number of parity shards", default=max_k, type=int)
    parser.add_argument("-m", help="EC mode (i for ISA-L, j for JavaReedSolomon)", default=mode, type=str)
    parser.add_argument("-b", help="Output filename for throughput benchmark", default=throughput_filename, type=str)
    parser.add_argument("-o", help="Output filename for heatmap", default=heatmap_filename, type=str)
    args = parser.parse_args()
    max_n = args.n
    max_k = args.k
    mode = args.m
    throughput_filename = args.b + ".log"
    heatmap_filename = args.o + ".png"

def main():
    parse_args()
    data = create_array()
    generate_data(data)
    os.system("cd ..")
    generate_heatmap(data)
    plt.show()

if __name__ == "__main__":
    main()