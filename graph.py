import os
import sys
import argparse
import re
import time
import numpy as np
import matplotlib.pyplot as plt
from os.path import exists

chunksize = 128
mode = "j"
throughput_filename = "throughput.log"
input_file = "input.log"
plot_name = "scatterplot.png"

def run_benchmark(data, parity):
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

def point_throughput(data, parity):
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

def generate_data():
    s_dur = []
    s_through = []
    s_lab = []
    m_dur = []
    m_through = []
    m_lab = []

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
            run_benchmark(data, parity)
            throughput = point_throughput(data, parity)
            os.remove(throughput_filename)
            m_dur.append(float(durability))
            m_through.append(throughput)
            m_string = f"({net_n}+{net_k})({loc_n}+{loc_k})"
            m_lab.append(m_string)
        elif len(line) == 3:
            n, k, durability = line
            data = [n]
            parity = [k]
            print(f"Generating Data for: ({n}+{k})\n")
            run_benchmark(data, parity)
            throughput = point_throughput(data, parity)
            os.remove(throughput_filename)
            s_dur.append(float(durability))
            s_through.append(throughput)
            s_string = f"({n}+{k})"
            s_lab.append(s_string)
        else:
            print("ERROR: Incomplete/Incorrect data in input file\n")
            exit()
        print("--- %s seconds elapsed in calculation ---\n" % (time.time() - start_time))

    assert len(s_dur) == len(s_through) == len(s_lab)
    assert len(m_dur) == len(m_through) == len(m_lab)

    return s_dur, s_through, s_lab, m_dur, m_through, m_lab

def generate_scatterplot(s_dur, s_through, s_lab, m_dur, m_through, m_lab):
    plt.scatter(s_dur, s_through, c ="red", marker="s")
    for i, txt in enumerate(s_lab):
        plt.annotate(txt, (s_dur[i], s_through[i]), xytext=(s_dur[i] + 0.25, s_through[i] + 7.5))
    plt.scatter(m_dur, m_through, c ="blue", marker="o")
    for i, txt in enumerate(m_lab):
        plt.annotate(txt, (m_dur[i], m_through[i]), xytext=(m_dur[i] + 0.25, m_through[i] + 7.5))
    plt.xlabel("Durability (nines)")
    plt.ylabel("Throughput (MB/s)")

def parse_args():
    global chunksize
    global mode
    global input_file
    global plot_name
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="Chunksize in KB", default=chunksize, type=int)
    parser.add_argument("-m", help="EC mode (i for ISA-L, j for JavaReedSolomon)", default=mode, type=str)
    parser.add_argument("-i", help="Input log file name.", default=input_file, type=str)
    parser.add_argument("-o", help="Output image file name.", default=plot_name, type=str)
    args = parser.parse_args()
    chunksize = args.c
    mode = args.m
    input_file = args.i
    plot_name = args.o

def main():
    parse_args()
    s_dur, s_through, s_lab, m_dur, m_through, m_lab = generate_data()
    generate_scatterplot(s_dur, s_through, s_lab, m_dur, m_through, m_lab)
    plt.savefig(f"../{plot_name}")
    plt.show()

if __name__ == "__main__":
    main()