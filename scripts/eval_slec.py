import os
import time
from lib import functions as func
from config import constants as const
import sys

def main():
    # func.Recalibrate()
    if len(sys.argv)-1 < 2:
        print("python scripts/eval_xxxx.py [num_data_chunks] [num_parity_chunks]")
        exit(0)
    k = int(sys.argv[1])
    p = int(sys.argv[2])

    # Generate throughput data.
    print(f"Generating Data for ({k}+{p})\n")
    func.RunBenchmarkSLEC(k, p)
    throughput = func.ReadData()
    os.remove(const.THROUGHPUT_FILE)

    print("throughput_result: {}".format(throughput))
    


if __name__ == "__main__":
    main()
