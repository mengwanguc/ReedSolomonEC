import os
import time
from lib import functions as func
from config import constants as const


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

    # Loop through configurations.
    for k in range(const.MAX_LRC_K):
        for l in range(const.MAX_LRC_L):
            for r in range(const.MAX_LRC_R):

                # Check if LRC configuration is convertible.
                if not func.Convertible(k, l, r):
                    continue
                for p in range(const.MAX_LRC_P):

                    # Check if LRC configuration data already calculated.
                    config_exists = func.ConfigExistsLRC(k, l, r, p)
                    if config_exists:
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
