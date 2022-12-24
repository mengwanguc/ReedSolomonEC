import os
import time
import functions as func
import constants as const

output_path = "data/total_isa-l_sleconst.csv"

def GenerateData():
    """
    Generates SLEC data given configurations.
    """

    # Ensure that first line in output file gives correct csv labels.
    with open(const.OUTPUT_PATH, "a+") as f:
        f.seek(0)
        firstline = f.readline().rstrip()
        if firstline != "data,parity,throughput":
            f.write("data,parity,throughput\n")

    # Loop through configurations.
    for n in range(1, const.MAX_N + 1):
        for k in range(1, const.MAX_K + 1):

            # Skip this configuration if it has already been calculated.
            config_exists = ConfigExistsSLEC(n, k)
                if config_exists:
                    continue

            start_time = time.time()

            # Generate throughput data.
            print(f"Generating Data for ({n}+{k})\n")
            func.RunBenchmarkSLEC(n, k)
            throughput = func.ReadData()
            os.remove(const.THROUGHPUT_FILE)

            # Write throughput data to outptu file.
            with open(const.OUTPUT_PATH, "a+") as f:
                f.seek(0, 2)
                f.write(f"{n},{k},{throughput}\n")

            print("--- %s seconds elapsed in calculation ---\n" % (time.time() - start_time))

def main():
    Recalibrate
    GenerateData()

if __name__ == "__main__":
    main()
