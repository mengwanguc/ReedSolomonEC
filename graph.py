import os
import argparse
import re
import time
import numpy as np
import matplotlib.pyplot as plt

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
    dur = []
    through = []

    with open(input_file) as ifile:
        lines = ifile.readlines()
        
    for line in lines:
        line = line.split()
        n, k, durability = line
        data = [n]
        parity = [k]
        print(f"Generating Data for: ({n}+{k})\n")

        if mode == "i":
            os.chdir("isa-l")
            print("Running ISA-L benchmark")
            start_time = time.time()
            run_benchmark(data, parity, "i")
            print("--- %f seconds elapsed in calculation ---\n" % (time.time() - start_time))
            throughput = point_throughput("i")
            os.remove(throughput_filename)
            dur.append(float(durability))
            through.append(throughput)
            print("Throughput: " + str(throughput))
        elif mode == "j":
            os.chdir("JavaReedSolomon")
            print("Running JRS benchmark")
            start_time = time.time()
            run_benchmark(data, parity, "j")
            throughput = point_throughput("j")
            print("--- %f seconds elapsed in calculation ---\n" % (time.time() - start_time))
            os.remove(throughput_filename)
            dur.append(float(durability))
            through.append(throughput)
            print("Throughput: " + str(throughput))
        else:
            print("ERROR: Incorrect mode given.\n")
            exit()
        os.chdir("..")

    assert len(dur) == len(through)

    return dur, through

def generate_scatterplot(isa_dur, isa_through, jrs_dur, jrs_through):
    plt.plot(isa_dur, isa_through, c ="red", marker="s", label="ISA-L")
    plt.plot(jrs_dur, jrs_through, c ="blue", marker="o", label="JavaRS")
    plt.title("Java Reed Solomon vs ISA-L EC Benchmarking for Configurations With Equal Overhead")
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
    isa_dur, isa_through = generate_data("i")
    jrs_dur, jrs_through = generate_data("j")
    generate_scatterplot(isa_dur, isa_through, jrs_dur, jrs_through)
    plt.savefig(f"../{plot_name}")
    plt.show()

if __name__ == "__main__":
    main()