import os
import argparse
import numpy as np
import seaborn as sns; sns.set_theme()
import matplotlib.pylab as plt
from matplotlib.colors import LinearSegmentedColormap
import re

# net = network.
# loc = local.
# n = data shards.
# k = parity shards.
max_net_n = 2
max_net_k = 1
max_loc_n = 4
max_loc_k = 2
chunksize = 128
mode = "i"
throughput_filename = "throughput.log"
heatmap_filename = "heatmap.png"

def run_benchmark(net_n, net_k, loc_n, loc_k):
    os.system(f"../run_benchmark.sh -net_n {net_n} -net_k {net_k} -loc_n {loc_n} -loc_k {loc_k} -c {chunksize} -m {mode} -f {throughput_filename}")

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
            print(f"Generating Data for: {n+1}+{k+1}\n")
            run_benchmark(n+1, k+1)
            generate_single_point(n, k, data)
            os.remove(throughput_filename)

def generate_scatterplot(data):
    ...

def parse_args():
    max_net_n = args.nd
    max_net_k = args.np
    max_loc_n = args.ld
    max_loc_k = args.lp
    throughput_filename = args.b + ".log"
    plot_filename = args.o + ".png"

def parse_args():
    global max_net_n
    global max_net_k
    global max_loc_n
    global max_loc_k
    global chunksize
    global mode
    global heatmap_filename
    parser = argparse.ArgumentParser()
    parser.add_argument("-net_n", help="Number of network data shards", default=max_net_n, type=int)
    parser.add_argument("-net_k", help="Number of network parity shards", default=max_net_k, type=int)
    parser.add_argument("-loc_n", help="Number of local data shards", default=max_loc_n, type=int)
    parser.add_argument("-loc_k", help="Number of local parity shards", default=max_loc_k, type=int)
    parser.add_argument("-c", help="Chunksize in KB", default=chunksize, type=int)
    parser.add_argument("-m", help="EC mode (i for ISA-L, j for JavaReedSolomon)", default=mode, type=str)
    parser.add_argument("-o", help="Output filename for heatmap", default=heatmap_filename, type=str)
    args = parser.parse_args()
    max_net_n = args.net_n
    max_net_k = args.net_k
    max_loc_n = args.loc_n
    max_loc_k = args.loc_k
    chunksize = args.c
    mode = args.m
    heatmap_filename = args.o

def main():
    parse_args()
    data = generate_data()
    os.system("cd ..")
    generate_scatterplot(data)
    plt.savefig("../" + heatmap_filename)
    plt.show()

if __name__ == "__main__":
    main()