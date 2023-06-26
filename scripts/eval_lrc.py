import os
import time
from lib import functions as func
from config import constants as const
import sys

def main():
    # func.Recalibrate()
    if len(sys.argv)-1 < 3:
        print("python scripts/eval_xxxx.py [k] [l] [r]")
        exit(0)
    k = int(sys.argv[1])
    l = int(sys.argv[2])
    r = int(sys.argv[3])
    p = 1

    # Generate throughput data.
    print(f"Generating Data for ({k},{l},{r})\n")
    func.RunBenchmarkLRC(k, l, r, 1)
    throughput = func.ReadData()
    os.remove(const.THROUGHPUT_FILE)

    print("throughput_result: {}".format(throughput))
    


if __name__ == "__main__":
    main()
