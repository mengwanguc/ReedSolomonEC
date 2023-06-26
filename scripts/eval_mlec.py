import os
import time
from lib import functions as func
from config import constants as const
import sys

def main():
    # func.Recalibrate()
    if len(sys.argv)-1 < 4:
        print("python scripts/eval_xxxx.py [net_k] [net_p] [local_k] [local_p]")
        exit(0)
    net_k = int(sys.argv[1])
    net_p = int(sys.argv[2])
    local_k = int(sys.argv[3])
    local_p = int(sys.argv[4])

    # Generate throughput data.
    print(f"Generating Data for ({net_k}+{net_p})({local_k}+{local_p})\n")
    func.RunBenchmarkMLEC(net_k, net_p, local_k, local_p)
    throughput = func.ReadData()
    os.remove(const.THROUGHPUT_FILE)

    print("throughput_result: {}".format(throughput))
    


if __name__ == "__main__":
    main()
