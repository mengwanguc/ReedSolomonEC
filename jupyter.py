import pandas as pd
import matplotlib.pyplot as plt

# Convert between LRC and MLEC/SLEC


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


# Read data frames
isa_l_mlec_df = pd.read_csv("data/isa-l_compare_mlec.csv")
javars_mlec_df = pd.read_csv("data/javars_compare_mlec.csv")
isa_l_lrc_df = pd.read_csv("data/total_isa-l_lrc.csv")
javars_lrc_df = pd.read_csv("data/total_javars_lrc.csv")
isa_l_slec_df = pd.read_csv("data/total_isa-l_slec.csv")
javars_slec_df = pd.read_csv("data/total_javars_slec.csv")

# Instantiate data and configuration arrays
isa_l_mlec_data = []
javars_mlec_data = []
isa_l_lrc_data = []
javars_lrc_data = []
isa_l_slec_data = []
javars_slec_data = []
isa_l_mlec_configs = []
javars_mlec_configs = []
isa_l_lrc_configs = []
javars_lrc_configs = []
isa_l_slec_configs = []
javars_slec_configs = []

# Pull desired JavaRS LRC and SLEC data
for index, row in isa_l_lrc_df.iterrows():
    throughput = float(row["throughput"])
    k = int(row["k"])
    l = int(row["l"])
    r = int(row["r"])
    p = int(row["p"])
    isa_l_lrc_data.append(throughput)
    isa_l_lrc_configs.append((k, l, r, p))
    network, local = convert_lrc(k, l, r, p, "s")
    n_net, k_net = network
    n_loc, k_loc = local
    a = 0
    b = 0
    a_check = 0
    b_check = 0
    for i, line in isa_l_slec_df.iterrows():
        throughput = float(line["throughput"])
        n = int(line["data"])
        k = int(line["parity"])
        if (n == n_net and k == k_net):
            a = throughput
            a_check += 1
        if (n == n_loc and k == k_loc):
            b = throughput
            b_check += 1
        if (a_check + b_check == 2):
            break
    if (a_check + b_check != 2):
        print("ERROR: SLEC configurations not found\n")
        exit()
    # 1/(1/a + 1/b)
    slec_throughput = (a * b) / (a + b)
    isa_l_slec_data.append(slec_throughput)
    isa_l_slec_configs.append(({n_net}, {k_net}, {n_loc}, {k_loc}))

assert (len(isa_l_slec_data) == len(isa_l_slec_configs)
        == len(isa_l_lrc_data) == len(isa_l_lrc_configs))

zipped2 = zip(isa_l_lrc_data, isa_l_slec_data,
              isa_l_lrc_configs, isa_l_slec_configs)
sorted_pairs2 = sorted(zipped2)
tuples2 = zip(*sorted_pairs2)
isa_l_lrc_data, isa_l_slec_data, isa_l_lrc_configs, isa_l_slec_configs = [
    list(tuple) for tuple in tuples2]

configurations = []
for lrc_config, slec_config in zip(isa_l_lrc_configs, isa_l_slec_configs):
    k, l, r, p = lrc_config
    net_n, net_k, loc_n, loc_k = slec_config
    configuration = f"LRC: ({k}, {l}, {r}, {p})\SLEC: ({net_n}+{net_k})({loc_n}+{loc_k})"
    configurations.append(configuration)

plt.scatter(configurations, isa_l_lrc_data,
            c="green", label="ISA-L LRC", marker="s")
plt.scatter(configurations, isa_l_slec_data,
            c="blue", label="ISA-L SLEC", marker="o")
plt.ylim(ymin=0)

plt.xlabel("Configuration")
plt.ylabel("Throughput (MB/s)")
plt.legend(loc="upper right")
plt.title("ISA-L LRC vs SLEC for all Configurations")

plt.show()
