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
isa_l_olrc_df = pd.read_csv("data/isa-l_opt_lrc.csv")

# Instantiate data and configuration arrays
isa_l_mlec_data = []
javars_mlec_data = []
isa_l_lrc_data = []
javars_lrc_data = []
isa_l_slec_data = []
javars_slec_data = []
isa_l_olrc_data = []
isa_l_mlec_configs = []
javars_mlec_configs = []
isa_l_lrc_configs = []
javars_lrc_configs = []
isa_l_slec_configs = []
javars_slec_configs = []
isa_l_olrc_configs = []

k_fixed = 6
l_fixed = 2
r_fixed = 3
p_fixed = 1

mlec_index = []

# Pull desired ISA-L LRC data
for index, row in isa_l_lrc_df.iterrows():
    throughput = float(row["throughput"])
    k = int(row["k"])
    l = int(row["l"])
    r = int(row["r"])
    p = int(row["p"])
    if (l == l_fixed and r == r_fixed and k == k_fixed):
        mlec_index.append(index)
        isa_l_lrc_data.append(throughput)
        isa_l_lrc_configs.append((k, l, r, p))
assert (len(isa_l_lrc_data) == len(isa_l_lrc_configs))

# Pull desired ISA-L Optimal LRC data
for index, row in isa_l_olrc_df.iterrows():
    throughput = float(row["throughput"])
    k = int(row["k"])
    l = int(row["l"])
    r = int(row["r"])
    p = int(row["p"])
    if (l == l_fixed and r == r_fixed and k == k_fixed):
        isa_l_olrc_data.append(throughput)
        isa_l_olrc_configs.append((k, l, r, p))
assert (len(isa_l_olrc_data) == len(isa_l_olrc_configs))

# Pull desired ISA-L MLEC data
for index, row in isa_l_mlec_df.iterrows():
    throughput = float(row["throughput"])
    n_net = int(row["network data"])
    k_net = int(row["network parity"])
    n_loc = int(row["local data"])
    k_loc = int(row["local parity"])
    if ((n_net == 2) and (k_net == 1) and (n_loc == 3)):
        isa_l_mlec_data.append(throughput)
        isa_l_mlec_configs.append((n_net, k_net, n_loc, k_loc))
assert (len(isa_l_mlec_data) == len(isa_l_mlec_configs))

# zipped = zip(isa_l_lrc_data, isa_l_mlec_data, isa_l_olrc_data,
#              isa_l_lrc_configs, isa_l_olrc_configs, isa_l_mlec_configs)
# sorted_pairs = sorted(zipped)
# tuples = zip(*sorted_pairs)
# isa_l_lrc_data, isa_l_mlec_data, isa_l_olrc_data, isa_l_lrc_configs, isa_l_olrc_configs, isa_l_mlec_configs = [
#     list(tuple) for tuple in tuples
# ]

configurations = []
for lrc_config, olrc_config, mlec_config in zip(isa_l_lrc_configs, isa_l_olrc_configs, isa_l_mlec_configs):
    k, l, r, p = lrc_config
    o_k, o_l, o_r, o_p = olrc_config
    m_g_n, m_g_k, m_l_n, m_l_k = mlec_config
    config1 = f"O-LRC: ({o_k}, {o_l}, {o_r}, {o_p})\n"
    config2 = f"LRC: ({k}, {l}, {r}, {p})\n"
    config3 = f"MLEC: ({m_g_n}+{m_g_k})({m_l_n}+{m_l_k})"
    configuration = config1 + config2 + config3
    configurations.append(configuration)

plt.scatter(configurations, isa_l_lrc_data,
            c="blue", label="ISA-L LRC", marker="s")
plt.scatter(configurations, isa_l_olrc_data,
            c="green", label="ISA-L Optimal LRC", marker="s")
plt.scatter(configurations, isa_l_mlec_data,
            c="red", label="ISA-L MLEC", marker="D")
plt.ylim(ymin=0)

plt.xlabel("Configuration")
plt.ylabel("Throughput (MB/s)")
plt.legend(loc="upper right")
plt.title(
    "LRC vs Optimal LRC vs MLEC for (6, 2, 3, x) Where Local Parity x Increases")

plt.show()
