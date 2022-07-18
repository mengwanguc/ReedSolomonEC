import os
import argparse
import re
import time
import matplotlib.pyplot as plt

chunksize = 128
throughput_filename = "throughput.log"
lrc_file = "data.log"
plot_name = "compare.png"
slec_file = "data/" + "slec.log"
title = "LRC Throughput vs Comparable SLEC Throughput for Increasing Local Parity"

def run_benchmark(data, ec_type, mode):
    if ec_type == "s":
        n, k = data
        os.system(f"../run_benchmark.sh -n {n} -k {k} -c {chunksize} -m {mode} -f {throughput_filename} -e s")
    elif ec_type == "m":
        net_n, net_k, loc_n, loc_k = data
        os.system(f"../run_benchmark.sh -a {net_n} -b {net_k} -n {loc_n} -k {loc_k} -c {chunksize} -m {mode} -f {throughput_filename} -e m")
    else:
        print("Error: Incorrect EC type given")
        exit()

def point_throughput(mode):
    with open(throughput_filename, "r") as f:
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

def convert_lrc(k, l, r, p):
    network = [k, r]
    local = [int(k / l), p]
    return network, local

def generate_data(mode):
    slec_data = []
    mlec_data = []
    configs = []

    with open(lrc_file) as ifile:
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

        config, _ = line.split("\t")
        _, k, l, r, p, _ = re.split(r'\D+', config)
        network, local = convert_lrc(int(k), int(l), int(r), int(p))
        g_n, g_k = network
        l_n, l_k = local

        print(f"Generating data for LRC configuration: ({k}, {l}, {r}, {p})\n")
        print(f"Comparable network configuration: ({g_n}+{g_k})")
        print(f"Comparable local configuration: ({l_n}+{l_k})")

        ### SLEC ###

        run_benchmark(network, "s", mode)
        a = point_throughput(mode)
        print(f"SLEC Throughput A: {str(a)}\n")
        os.remove(throughput_filename)

        run_benchmark(local, "s", mode)
        b = point_throughput(mode)
        print(f"SLEC Throughput B: {str(b)}\n")
        os.remove(throughput_filename)

        # 1/(1/a + 1/b)
        slec_throughput = (a * b) / (a + b)
        print(f"Overall SLEC Throughput: {str(slec_throughput)}\n")
        slec_data.append(slec_throughput)

        ### MLEC ###

        config = [g_n, g_k, l_n, l_k]
        run_benchmark(config, "m", mode)
        mlec_throughput = point_throughput(mode)
        print(f"MLEC Throughput: {str(mlec_throughput)}\n")
        os.remove(throughput_filename)
        mlec_data.append(mlec_throughput)
        
        configs.append((g_n, g_k, l_n, l_k))

        print("--- %s seconds elapsed in calculation ---\n" % (time.time() - start_time))

    os.chdir("..")
    return slec_data, mlec_data, configs

def generate_configs(lrc_configs, slec_configs):
    assert len(lrc_configs) == len(slec_configs)
    configurations = []
    for lrc_config, slec_config in zip(lrc_configs, slec_configs):
        k, l, r, p = lrc_config
        g_n, g_k, l_n, l_k = slec_config
        configuration = f"LRC: ({k}, {l}, {r}, {p})\nSLEC: ({g_n}+{g_k}),({l_n}+{l_k})"
        configurations.append(configuration)
    return configurations

def write_data(data):
    with open(slec_file, "a") as f:
        for datum in data:
            config, throughput = datum
            g_n, g_k, l_n, l_k = config
            f.write(f"({g_n}+{g_k}),({l_n}+{l_k})\t{throughput}\n")

def read_data():
    lrc_data = []
    slec_data = []
    lrc_configs = []
    slec_configs = []

    with open(lrc_file, 'r') as lfile, open(slec_file, 'r') as sfile:
        lrc_lines = lfile.readlines()
        slec_lines = sfile.readlines()

    for lrc_line, slec_line in zip(lrc_lines, slec_lines):

        lrc_config, lrc_throughput = lrc_line.split("\t")
        lrc_throughput, _ = lrc_throughput.split("\n")
        _, k, l, r, p, _ = re.split(r'\D+', lrc_config)

        slec_config, slec_throughput = slec_line.split("\t")
        slec_throughput, _ = slec_throughput.split("\n")
        _, g_n, g_k, l_n, l_k, _ = re.split(r'\D+', slec_config)

        lrc_data.append(float(lrc_throughput))
        slec_data.append(float(slec_throughput))
        lrc_configs.append((k, l, r, p))
        slec_configs.append((g_n, g_k, l_n, l_k))

    assert len(lrc_data) == len(slec_data) == len(lrc_configs) == len(slec_configs)
    return lrc_data, slec_data, lrc_configs, slec_configs

def generate_plot(lrc_throughput, slec_throughput, configurations):
    plt.scatter(configurations, lrc_throughput, c="red", label="LRC", marker="s")
    plt.scatter(configurations, slec_throughput, c="blue", label="SLEC", marker="o")
    plt.ylim(ymin=0)

    plt.xlabel("Configuration")
    plt.ylabel("Throughput (MB/s)")
    plt.legend(loc='upper right')
    plt.title(title)

    plt.savefig(f"../{plot_name}")
    plt.show()

def parse_args():
    global lrc_file
    global plot_name

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input log file name.", default=lrc_file, type=str)
    parser.add_argument("-o", help="Output graph file name.", default=plot_name, type=str)

    args = parser.parse_args()
    plot_name = "figure/" + args.o
    lrc_file = "data/" + args.i

def collect_data():
    slec_data = generate_data("j")
    write_data(slec_data)

def use_data():
    lrc_data, slec_data, lrc_configs, slec_configs = read_data()
    configurations = generate_configs(lrc_configs, slec_configs)
    generate_plot(lrc_data, slec_data, configurations)

def main():
    parse_args()
    # collect_data()
    use_data()

if __name__ == "__main__":
    main()