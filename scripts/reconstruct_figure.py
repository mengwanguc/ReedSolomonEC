import matplotlib.pyplot as plt
from lib import functions as func
from config import constants as const


def ReadFigureData():
    """
    Reads the appropriate figure data.
    """
    data = []
    configs = []

    # Read data.
    with open(const.ISA_L_SLEC, "r") as file:
        lines = file.readlines()[1:]

        for line in lines:
            n, k, throughput = line.split(",")
            throughput, _ = throughput.split("\n")

            # Write data.
            data.append(float(throughput))
            configs.append(n)

    return data, configs


def GeneratePlot(data, configs):
    """
    Reconstructs figure 1 from the ECWide paper.
    """
    plt.plot(configs, data, "-o", c="red", label="ISA-L SLEC", marker="s")
    plt.ylim(ymin=0)
    plt.xlabel("k")
    plt.ylabel("Throughput (MB/s)")
    plt.legend(loc="upper right")

    title = "SLEC Throughput vs Number of Data Chunks for Chunk Size of 64 MB and n-k = 4"
    plt.title(title)

    plt.savefig(f"{const.OUTPUT_PATH}")
    plt.show()


def main():
    data, configs = ReadFigureData()
    GeneratePlot(data, configs)


if __name__ == "__main__":
    main()
