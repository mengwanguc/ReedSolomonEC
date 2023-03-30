import os
import time
from lib import functions as func
from config import constants as const
import numpy as np

def GenerateData():
    """
    Generates LRC throughput data.
    """

    # Ensure that first line in output file gives correct csv labels.
    with open(const.OUTPUT_PATH, "a+") as f:
        f.seek(0)
        firstline = f.readline().rstrip()
        if firstline != "k,l,r,p,throughput":
            f.write("k,l,r,p,throughput\n")

    l = 2
    p = 1
    # Loop through configurations.
    for k in range(1, const.MAX_LRC_K + 1):
        for r in range(1, const.MAX_LRC_R + 1):
            # Check if LRC configuration data already calculated.
            config_exists = func.ConfigExistsLRC(k, l, r, p)
            if config_exists:
                continue

            # Check if LRC configuration is convertible.
            if not func.Convertible(k, l, r):
                print(f"Configuration ({k}, {l}, {r}, {p}) is not convertible\n")
                with open(const.OUTPUT_PATH, "a+") as f:
                    f.seek(0, 2)
                    f.write(f"{k},{l},{r},{p},{np.nan}\n")
                continue

            start_time = time.time()

            # Generate LRC throughput data.
            print(f"Generating Data for: ({k}, {l}, {r}, {p})\n")
            func.RunBenchmarkLRC(k, l, r, p)
            throughput = func.ReadData()
            os.remove(const.THROUGHPUT_FILE)

            # Write LRC throughput data.
            with open(const.OUTPUT_PATH, "a+") as f:
                f.seek(0, 2)
                f.write(f"{k},{l},{r},{p},{throughput}\n")
            print(f"Configuration: ({k}, {l}, {r}, {p})\tThroughput: {throughput}\n")

            print("--- %s seconds elapsed in calculation ---\n" % (time.time() - start_time))


def main():
    func.Recalibrate()
    GenerateData()


if __name__ == "__main__":
    main()
