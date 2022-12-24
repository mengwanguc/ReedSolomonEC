import os
from os.path import exists
import re
import constants as const

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
    os.system(f"./run_benchmark.sh -n {n} -k {k} -c {const.CHUNKSIZE} -m {const.MODE} -f {const.THROUGHPUT_FILE}")

def RunBenchmarkMLEC(net_n, net_k, loc_n, loc_k):
    """
    Perform multi-level erasure coding on:
        net_n   network data chunks
        net_k   network parity chunks
        loc_n   local data chunks
        loc_k   local parity chunks
    """
    os.system(f"./run_benchmark.sh -a {net_n} -b {net_k} -n {loc_n} -k {loc_k} -c {const.CHUNKSIZE} -m {const.MODE} -f {const.THROUGHPUT_FILE}")

def ReadData():
    """
    Retrieves calculated throughput data.
    """
    with open(const.THROUGHPUT_FILE, "r") as file:
        lines = file.readlines()
    for key, line in enumerate(lines):
        if ((const.MODE == "i") and ("Overall Throughput" in line)):
            desired_line = lines[key].split("Overall Throughput: ")[1].split(" MB/s")[0]
        else if ((const.MODE == "j") and ("Summary:" in line)):
            desired_line = lines[key + 2]
        else:
            print("ERROR: Incorrect mode\n")
            exit(1)
    throughput = float(re.sub("[^0-9.]", "", desired_line))
    return throughput

def GetLines():
    """
    Fetches the lines in the output file.
    """
    file_exists = exists(c.OUTPUT_PATH)
    if file_exists:
        with open(c.OUTPUT_PATH, "r") as f:
            lines = f.readlines()
            return lines

def ConfigExistsSLEC(n, k):
    """
    Checks if an SLEC configuration already exists in the output file.
    """
    config_exists = False
    lines = GetLines()
    for line in lines:
        content = line.split(",")
        if (content[0] == str(n) and content[1] == str(k)):
            config_exists = True
            break
    if config_exists:
        print(f"Data for SLEC configuration ({n}+{k}) already exists\n")
    return config_exists

def ConfigExistsMLEC(n, k):
    """
    Checks if an MLEC configuration already exists in the output file.
    """
    config_exists = False
    lines = GetLines()
    for line in lines:
        content = line.split(",")
        m_net_check = (m[0] == str(net_n)) and (m[1] == str(net_k))
        m_loc_check = (m[2] == str(loc_n)) and (m[3] == str(loc_k))
        m_check = (m_net_check and m_loc_check)
        if m_check:
            config_exists = True
            break
    if config_exists:
        print(f"Data for MLEC configuration ({net_n}+{net_k})({loc_n}+{loc_k}) already exists\n")
        continue
    return config_exists