import os
import matplotlib.pyplot as plt
from config import constants as const
from lib import functions as func
from config.constants import MLEC, SLEC, ISA_L, JAVA_RS


def ReadDurability(ec_type):
    """
    Reads durability data.
    """
    durabilities = []

    if (ec_type == SLEC):
        input_file = const.SLEC_DURABILITY
    elif (ec_type == MLEC):
        input_file = const.MLEC_DURABILITY
    else:
        print("ERROR: Incorrect EC type\n")
        os.EX_CONFIG
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            durability = line.split(",")[-1]
            durabilities.append(durability)
    return durabilities


def ReadThroughput(mode, ec_type):
    """
    Reads throughput data.
    """
    throughputs = []

    if (ec_type == SLEC):
        if (mode == ISA_L):
            input_file = const.ISA_L_SLEC
        elif (mode == JAVA_RS):
            input_file = const.JAVA_RS_SLEC
        else:
            print("ERROR: Incorrect EC mode\n")
            os.EX_CONFIG
    elif (ec_type == MLEC):
        if (mode == ISA_L):
            input_file = const.ISA_L_MLEC
        elif (mode == JAVA_RS):
            input_file = const.JAVA_RS_MLEC
        else:
            print("ERROR: Incorrect EC mode\n")
            os.EX_CONFIG
    else:
        print("ERROR: Incorrect EC type\n")
        os.EX_CONFIG

    with open(input_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            throughput = line.split(",")[-1]
            throughputs.append(throughput)
    return throughputs


def GenerateScatterplot():
    """
    Generates a scatter plot that plots SLEC and MLEC
    throughput vs durability for both ISA-L and Java Reed-Solomon.
    """

    # Collect durability data.
    slec_durability = ReadDurability(SLEC)
    mlec_durability = ReadDurability(MLEC)

    # Collect throughput data.
    isa_s_throughput = ReadThroughput(ISA_L, SLEC)
    javars_s_throughput = ReadThroughput(JAVA_RS, SLEC)
    isa_m_throughput = ReadThroughput(ISA_L, MLEC)
    javars_m_throughput = ReadThroughput(JAVA_RS, MLEC)

    # Plot durability vs throughput.
    plt.plot(slec_durability, isa_s_throughput, c="red", label="ISA-L SLEC")
    plt.plot(mlec_durability, isa_m_throughput, c="blue", label="ISA-L MLEC")
    plt.plot(slec_durability, javars_s_throughput, c="orange", label="JavaRS SLEC")
    plt.plot(mlec_durability, javars_m_throughput, c="green", label="JavaRS MLEC")

    # Graph labels.
    plt.xlabel("Durability (nines)")
    plt.ylabel("Throughput (MB/s)")
    plt.legend(loc='upper right')

    # Save and show graph.
    plt.savefig(f"{const.OUTPUT_PATH}")
    plt.show()


def main():
    func.Recalibrate()
    GenerateScatterplot()


if __name__ == "__main__":
    main()
