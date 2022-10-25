import argparse
import matplotlib.pyplot as plt

throughput_filename = "throughput.log"
slec_file = "data/ecwide_figure1.csv"
mode = "i"
plot_name = "compare.png"
title = "SLEC Throughput vs Number of Data Chunks for Chunk Size of 64 MB and n-k = 4"


def read_data():
    data = []
    configs = []

    with open(slec_file, "r") as isa_l_slec_f:
        isa_l_slec_lines = isa_l_slec_f.readlines()[1:]

    for isa_l_slec_line in isa_l_slec_lines:

        n, k, isa_l_slec_throughput = isa_l_slec_line.split(",")
        isa_l_slec_throughput, _ = isa_l_slec_throughput.split("\n")

        data.append(float(isa_l_slec_throughput))
        configs.append(n)
    return data, configs


def generate_plot(data, configs):
    plt.plot(configs, data, "-o", c="red", label="ISA-L SLEC", marker="s")
    plt.ylim(ymin=0)

    plt.xlabel("k")
    plt.ylabel("Throughput (MB/s)")
    plt.legend(loc="upper right")
    plt.title(title)

    plt.savefig(f"{plot_name}")
    plt.show()


def parse_args():
    global plot_name
    global mode

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="Output graph file name.",
                        default=plot_name, type=str)
    parser.add_argument("-m", help="Mode", default=mode, type=str)

    args = parser.parse_args()
    plot_name = "figures/" + args.o
    mode = args.m


def use_data():
    data, configs = read_data()
    generate_plot(data, configs)


def main():
    parse_args()
    use_data()


if __name__ == "__main__":
    main()
