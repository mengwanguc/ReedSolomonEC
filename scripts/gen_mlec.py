import os
import time
from lib import functions as func
from config import constants as const

output_path = "data/total_isa-l_mlec.csv"


def GenerateData():
    """
    Generates MLEC data given configurations.
    """

    # Ensure that first line in output file gives correct csv labels.
    with open(const.OUTPUT_PATH, "a+") as f:
        f.seek(0)
        firstline = f.readline().rstrip()
        if firstline != "network_data,network_parity,local_data,local_parity,throughput":
            f.write("network_data,network_parity,local_data,local_parity,throughput\n")

    net_n = 5
    net_k = 1
    # Loop through configurations.
    for loc_n in range(1, const.MAX_LOC_N + 1):
        for loc_k in range(1, const.MAX_LOC_K + 1):

            # Skip this configuration if it has already been calculated.
            config_exists = func.ConfigExistsMLEC(net_n, net_k, loc_n, loc_k)
            if config_exists:
                continue

            start_time = time.time()

            # Generate throughput data.
            print(f"Generating Data for ({net_n}+{net_k})({loc_n}+{loc_k})\n")
            func.RunBenchmarkMLEC(net_n, net_k, loc_n, loc_k)
            throughput = func.ReadData()
            os.remove(const.THROUGHPUT_FILE)

            # Write throughput data to outptu file.
            with open(const.OUTPUT_PATH, "a+") as f:
                f.seek(0, 2)
                f.write(f"{net_n},{net_k},{loc_n},{loc_k},{throughput}\n")

            print("--- %s seconds elapsed in calculation ---\n" % (time.time() - start_time))


def main():
    func.Recalibrate()
    GenerateData()


if __name__ == "__main__":
    main()
