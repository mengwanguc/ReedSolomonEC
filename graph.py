import os
import sys
import argparse
import re
import time
import numpy as np
import matplotlib.pyplot as plt
from os.path import exists

chunksize = 128
throughput_filename = "throughput.log"
input_file = "input.log"
plot_name = "scatterplot.png"

def run_benchmark(data, parity, mode):
    assert len(data) == len(parity)
    if len(data) == 2:
        net_n = data[0]
        loc_n = data[1]
        net_k = parity[0]
        loc_k = parity[1]
        os.system(f"../run_benchmark.sh -a {net_n} -b {net_k} -n {loc_n} -k {loc_k} -c {chunksize} -m {mode} -f {throughput_filename} -e m")
    elif len(data) == 1:
        loc_n = data[0]
        loc_k = parity[0]
        os.system(f"../run_benchmark.sh -n {loc_n} -k {loc_k} -c {chunksize} -m {mode} -f {throughput_filename} -e s")
    else:
        print("ERROR: Incorrect data/parity shard types\n")
        exit()

def point_throughput(mode):
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
    return throughput

def generate_data(mode):
    s_dur = []
    s_through = []
    m_dur = []
    m_through = []

    with open(input_file) as ifile:
        lines = ifile.readlines()

    if (mode == "i"):
        os.chdir("isa-l")
    elif (mode == "j"):
        os.chdir("JavaReedSolomon")
    else:
        print("ERROR: Incorrect mode\n")
        exit()
        
    for line in lines:
        start_time = time.time()
        line = line.split()
        if len(line) == 5:
            net_n, net_k, loc_n, loc_k, durability = line
            data = [net_n, loc_n]
            parity = [net_k, loc_k]
            print(f"Generating Data for: ({net_n}+{net_k})({loc_n}+{loc_k})\n")
            run_benchmark(data, parity, mode)
            throughput = point_throughput(mode)
            os.remove(throughput_filename)
            m_dur.append(float(durability))
            m_through.append(throughput)
        elif len(line) == 3:
            n, k, durability = line
            data = [n]
            parity = [k]
            print(f"Generating Data for: ({n}+{k})\n")
            run_benchmark(data, parity, mode)
            throughput = point_throughput(mode)
            os.remove(throughput_filename)
            s_dur.append(float(durability))
            s_through.append(throughput)
        else:
            print("ERROR: Incomplete/Incorrect data in input file\n")
            exit()
        print("--- %s seconds elapsed in calculation ---\n" % (time.time() - start_time))
    os.chdir("..")

    assert len(s_dur) == len(s_through)
    assert len(m_dur) == len(m_through)

    single = (s_dur, s_through)
    multi = (m_dur, m_through)

    return single, multi

def generate_scatterplot(isa_s, isa_m, java_s, java_m):
    isa_s_dur, isa_s_through = isa_s
    isa_m_dur, isa_m_through = isa_m
    java_s_dur, java_s_through = java_s
    java_m_dur, java_m_through = java_m
    plt.plot(isa_s_dur, isa_s_through, c ="red", label="ISA-L single-level")
    plt.plot(isa_m_dur, isa_m_through, c ="blue", label="ISA-L multi-level")
    plt.plot(java_s_dur, java_s_through, c ="orange", label="JavaRS single-level")
    plt.plot(java_m_dur, java_m_through, c ="green", label="JavaRS multi-level")
    plt.xlabel("Durability (nines)")
    plt.ylabel("Throughput (MB/s)")
    plt.legend(loc='upper right')

def parse_args():
    global chunksize
    global input_file
    global plot_name
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="Chunksize in KB", default=chunksize, type=int)
    parser.add_argument("-i", help="Input log file name.", default=input_file, type=str)
    parser.add_argument("-o", help="Output image file name.", default=plot_name, type=str)
    args = parser.parse_args()
    chunksize = args.c
    input_file = args.i
    plot_name = args.o

def main():
    parse_args()
    isa_s, isa_m = generate_data("i")
    java_s, java_m = generate_data("j")
    generate_scatterplot(isa_s, isa_m, java_s, java_m)
    plt.savefig(f"../{plot_name}")
    plt.show()

if __name__ == "__main__":
    main()