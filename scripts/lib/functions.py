import os
import re
from config import constants as const
from config.constants import ISA_L, JAVA_RS, SLEC, MLEC


def Recalibrate():
    """
    Updates repository and all submodules.
    """
    os.chdir("../isa-l")
    os.system("git pull")
    os.chdir("../JavaReedSolomon")
    os.system("git pull")
    os.chdir("..")
    os.system("git pull")


def RunBenchmarkSLEC(n, k):
    """
    Perform single-level erasure coding on:
        n   data chunks
        k   parity chunks
    """
    os.system(f"./run_benchmark.sh -n {n} -k {k} -c {const.CHUNKSIZE} -m {const.MODE} -e {const.SLEC} -f {const.THROUGHPUT_FILE}")


def RunBenchmarkMLEC(net_n, net_k, loc_n, loc_k):
    """
    Perform multi-level erasure coding on:
        net_n   network data chunks
        net_k   network parity chunks
        loc_n   local data chunks
        loc_k   local parity chunks
    """
    os.system(f"./run_benchmark.sh -a {net_n} -b {net_k} -n {loc_n} -k {loc_k} -c {const.CHUNKSIZE} -m {const.MODE} -e {const.MLEC} -f {const.THROUGHPUT_FILE}")


def RunBenchmarkLRC(k, l, r, p):
    """
    Performs local reconstuction codes erasure coding on:
        k   global data chunks
        l   local groups
        r   global parity chunks
        p   local parity chunks
    """
    os.system(f"../run_benchmark.sh -k {k} -l {l} -r {r} -p {p} -c {const.CHUNKSIZE} -m {const.MODE} -e {const.LRC} -f {const.THROUGHPUT_FILE} -e l -t {const.LRC_OPT}")


def ReadData():
    """
    Retrieves calculated throughput data.
    """
    with open(const.THROUGHPUT_FILE, "r") as file:
        lines = file.readlines()
    for key, line in enumerate(lines):
        if ((const.MODE == ISA_L) and ("Overall Throughput" in line)):
            desired_line = lines[key].split("Overall Throughput: ")[
                1].split(" MB/s")[0]
        elif ((const.MODE == JAVA_RS) and ("Summary:" in line)):
            desired_line = lines[key + 2]
        else:
            print("ERROR: Incorrect mode\n")
            os.EXIT_CONFIG
    throughput = float(re.sub("[^0-9.]", "", desired_line))
    return throughput


def GetLines():
    """
    Fetches the lines in the output file.
    """
    file_exists = os.path.exists(const.OUTPUT_PATH)
    if file_exists:
        with open(const.OUTPUT_PATH, "r") as f:
            lines = f.readlines()
            return lines


def ConfigExistsSLEC(n, k):
    """
    Checks if an SLEC configuration already exists in the output file.
    """
    lines = GetLines()
    for line in lines:
        content = line.split(",")
        if (content[0] == str(n) and content[1] == str(k)):
            print(f"Data for SLEC configuration ({n}+{k}) already exists\n")
            return True
    return False


def ConfigExistsMLEC(net_n, net_k, loc_n, loc_k):
    """
    Checks if an MLEC configuration already exists in the output file.
    """
    lines = GetLines()
    for line in lines:
        content = line.split(",")
        net_check = (content[0] == str(net_n)) and (content[1] == str(net_k))
        loc_check = (content[2] == str(loc_n)) and (content[3] == str(loc_k))
        if (net_check and loc_check):
            print(f"Data for MLEC configuration ({net_n}+{net_k})({loc_n}+{loc_k}) already exists\n")
            return True
    return False


def ConfigExistsLRC(k, l, r, p):
    """
    Checks if an LRC configuration already exists in the output file.
    """
    lines = GetLines()
    for line in lines:
        content = line.split(",")
        first_check = (content[0] == str(k)) and (content[1] == str(l))
        second_check = (content[2] == str(r) and content[3] == str(p))
        if (first_check and second_check):
            print(f"Data for configuration ({k}, {l}, {r}, {p}) already exists\n")
            return True
    return False


def Convertible(k, l, r):
    """
    Checks whether an LRC configuration is convertible or not.
    """

    # Check number of local groups.
    if (k % l != 0):
        return False

    # Check number of global parities.
    local_group = k / l
    if (r % local_group != 0):
        return False
    return True


def ConvertLRC(k, l, r, p, ec_type):
    """
    Converts between MLEC/SLEC and MLEC configurations.
    """
    if ec_type == SLEC:
        global_slec = [k, r]
        local_slec = [int(k / l), p]
        return global_slec, local_slec
    elif ec_type == MLEC:
        network = [l, int(r / (k / l))]
        local = [int(k / l), p]
        return network, local
    else:
        print("Error: Incorrect EC conversion type\n")
        os.EXIT_CONFIG


def FindDelta(old, new):
    """
    Calculates the difference between two values.
    """
    difference = new - old
    if (old == 0):
        change = 0
    else:
        change = (difference / old) * 100
    return (difference, change)
