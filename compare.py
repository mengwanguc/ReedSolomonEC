import os
import argparse
import re
import time
import matplotlib.pyplot as plt
from os.path import exists

chunksize = 128
throughput_filename = "throughput.log"
lrc_file = "randomized_data.log"
plot_name = "compare.png"
slec_file = "data/" + "compare_slec.csv"
mlec_file = "data/" + "compare_mlec.csv"
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

def convert_lrc(k, l, r, p, ec_type):
    if ec_type == "s":
        global_slec = [k, r]
        local_slec = [int(k / l), p]
        return global_slec, local_slec
    elif ec_type == "m":
        network = [l, int(r / (k / l))]
        local = [int(k / l), p]
        return network, local
    else:
        print("Error: Incorrect EC conversion type\n")
        exit()

def generate_data(mode):
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

        global_slec, local_slec = convert_lrc(int(k), int(l), int(r), int(p), ec_type="s")
        g_n, g_k = global_slec
        l_n, l_k = local_slec
        network, local = convert_lrc(int(k), int(l), int(r), int(p), ec_type="m")
        net_n, net_k = network
        loc_n, loc_k = local

        # config_exists = False
        # slec_file_exists = exists("../" + slec_file)
        # mlec_file_exists = exists("../" + mlec_file)
        # if slec_file_exists and mlec_file_exists:
        #     with open("../" + slec_file, "r") as s_file, open("../" + mlec_file, "r") as m_file:
        #         s_lines = s_file.readlines()
        #         m_lines = m_file.readlines()
        #         for s_line, m_line in zip(s_lines, m_lines):
        #             s = s_line.split(",")
        #             m = m_line.split(",")
        #             s_net_check = (s[0] == str(g_n)) and (s[1] == str(g_k))
        #             s_loc_check = (s[2] == str(l_n)) and (s[3] == str(l_k))
        #             m_net_check = (m[0] == str(net_n)) and (m[1] == str(net_k))
        #             m_loc_check = (m[2] == str(loc_n)) and (m[3] == str(loc_k))
        #             s_check = (s_net_check and s_loc_check)
        #             m_check = (m_net_check and m_loc_check)
        #             if (s_check or m_check):
        #                 if (s_check and m_check):
        #                     config_exists = True
        #                     break
        #                 else:
        #                     print(f"Error: Configuration inconsistency in files.")
        #                     exit()
        # if config_exists:
        #     print(f"Data for LRC configuration ({k}, {l}, {r}, {p}) already exists\n")
        #     continue

        print(f"Generating data for LRC configuration: ({k}, {l}, {r}, {p})\n")
        print(f"Comparable SLEC configuration: ({g_n}+{g_k}),({l_n}+{l_k})")
        print(f"Comparable MLEC configuration: ({net_n}+{net_k})({loc_n}+{loc_k})")

        ### SLEC ###

        # run_benchmark(network, "s", mode)
        # a = point_throughput(mode)
        # print(f"SLEC Throughput A: {str(a)}\n")
        # os.remove(throughput_filename)

        # run_benchmark(local, "s", mode)
        # b = point_throughput(mode)
        # print(f"SLEC Throughput B: {str(b)}\n")
        # os.remove(throughput_filename)

        # # 1/(1/a + 1/b)
        # slec_throughput = (a * b) / (a + b)
        # print(f"Overall SLEC Throughput: {str(slec_throughput)}\n")

        # with open("../" + slec_file, "a+") as s_file:
        #     s_file.seek(0)
        #     s_firstline = s_file.readline().rstrip()
        #     s_label = "global data,global parity,local data,local parity,throughput"
        #     if s_firstline != s_label:
        #         s_file.write(s_label + "\n")
        #     s_file.seek(0, 2)
        #     s_file.write(f"{g_n},{g_k},{l_n},{l_k},{slec_throughput}\n")

        ### MLEC ###

        config = [net_n, net_k, loc_n, loc_k]
        run_benchmark(config, "m", mode)
        mlec_throughput = point_throughput(mode)
        print(f"MLEC Throughput: {str(mlec_throughput)}\n")
        os.remove(throughput_filename)

        with open("../" + mlec_file, "a+") as m_file:
            m_file.seek(0)
            m_firstline = m_file.readline().rstrip()
            m_label = "network data,network parity,local data,local parity,throughput"
            if m_firstline != m_label:
                m_file.write(m_label + "\n")
            m_file.seek(0, 2)
            m_file.write(f"{net_n},{net_k},{loc_n},{loc_k},{mlec_throughput}\n")

        print("--- %s seconds elapsed in calculation ---\n" % (time.time() - start_time))

    os.chdir("..")

def generate_configs(configs):
    lrc_configs, slec_configs, mlec_configs = configs
    assert len(lrc_configs) == len(slec_configs) == len(mlec_configs)
    configurations = []
    for lrc_config, slec_config, mlec_config in zip(lrc_configs, slec_configs, mlec_configs):
        k, l, r, p = lrc_config
        s_g_n, s_g_k, s_l_n, s_l_k = slec_config
        m_g_n, m_g_k, m_l_n, m_l_k = mlec_config
        configuration = f"LRC: ({k}, {l}, {r}, {p})\nSLEC: ({s_g_n}+{s_g_k}),({s_l_n}+{s_l_k})\nMLEC: ({m_g_n}+{m_g_k})({m_l_n}+{m_l_k})"
        configurations.append(configuration)
    return configurations

def read_data():
    lrc_data = []
    slec_data = []
    mlec_data = []
    lrc_configs = []
    slec_configs = []
    mlec_configs = []

    with open(lrc_file, 'r') as l_file, open(slec_file, 'r') as s_file, open(mlec_file, 'r') as m_file:
        lrc_lines = l_file.readlines()
        slec_lines = s_file.readlines()[1:]
        mlec_lines = m_file.readlines()[1:]

    for lrc_line, slec_line, mlec_line in zip(lrc_lines, slec_lines, mlec_lines):

        lrc_config, lrc_throughput = lrc_line.split("\t")
        lrc_throughput, _ = lrc_throughput.split("\n")
        _, k, l, r, p, _ = re.split(r'\D+', lrc_config)

        s_g_n, s_g_k, s_l_n, s_l_k, slec_throughput = slec_line.split(",")
        slec_throughput, _ = slec_throughput.split("\n")

        m_g_n, m_g_k, m_l_n, m_l_k, mlec_throughput = mlec_line.split(",")
        mlec_throughput, _ = mlec_throughput.split("\n")

        lrc_data.append(float(lrc_throughput))
        slec_data.append(float(slec_throughput))
        mlec_data.append(float(mlec_throughput))
        lrc_configs.append((k, l, r, p))
        slec_configs.append((s_g_n, s_g_k, s_l_n, s_l_k))
        mlec_configs.append((m_g_n, m_g_k, m_l_n, m_l_k))

    data_lengths = len(lrc_data) == len(slec_data) == len(mlec_data)
    config_lengths = len(lrc_configs) == len(slec_configs) == len(mlec_configs)
    assert (data_lengths and config_lengths)
    return (lrc_data, slec_data, mlec_data), (lrc_configs, slec_configs, mlec_configs)

def generate_plot(data, configurations):
    lrc_data, slec_data, mlec_data = data
    plt.scatter(configurations, lrc_data, c="green", label="LRC", marker="s")
    plt.scatter(configurations, slec_data, c="blue", label="SLEC", marker="o")
    plt.scatter(configurations, mlec_data, c="red", label="MLEC", marker="D")
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
    plot_name = "figures/" + args.o
    lrc_file = "data/" + args.i

def use_data():
    data, configs = read_data()
    configurations = generate_configs(configs)
    generate_plot(data, configurations)

def main():
    parse_args()
    # generate_data("j")
    use_data()

if __name__ == "__main__":
    main()