import os
import argparse
import re
import time
from os.path import exists

max_n = 50
max_k = 10
chunksize = 128
throughput_filename = "throughput.log"
output_path = "data/total_isa-l_slec.csv"
mode = "i"


def run_benchmark(n, k, mode):
    os.system(
        f"../run_benchmark.sh -n {n} -k {k} -c {chunksize} -m {mode} -f {throughput_filename} -e s")


def point_throughput(mode):
    with open(throughput_filename, "r") as f:
        lines = f.readlines()
    for key, line in enumerate(lines):
        if ((mode == "i") and ("throughput2" in line)):
            desired_line = lines[key].split("throughput2:")[1].split("MB/s")[0]
        if ((mode == "j") and ("Summary:" in line)):
            desired_line = lines[key + 2]
    throughput = float(re.sub("[^0-9.]", "", desired_line))
    return throughput


def generate_data(mode):

    data = []

    if (mode == "i"):
        os.chdir("isa-l")
    elif (mode == "j"):
        os.chdir("JavaReedSolomon")
    else:
        print("ERROR: Incorrect mode\n")
        exit()

    for n in range(1, max_n + 1):
        for k in range(1, max_k + 1):
            config_exists = False
            file_exists = exists("../" + output_path)
            if file_exists:
                with open("../" + output_path, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        content = line.split(",")
                        if (content[0] == str(n) and content[1] == str(k)):
                            config_exists = True
                            break
                if config_exists:
                    print(f"Data for configuration ({n}+{k}) already exists\n")
                    continue
            start_time = time.time()
            print(f"Generating Data for ({n}+{k})\n")
            run_benchmark(n, k, mode)
            throughput = point_throughput(mode)
            os.remove(throughput_filename)
            with open("../" + output_path, "a+") as f:
                f.seek(0)
                firstline = f.readline().rstrip()
                if firstline != "data,parity,throughput":
                    f.write("data,parity,throughput\n")
                f.seek(0, 2)
                f.write(f"{n},{k},{throughput}\n")
            print("--- %s seconds elapsed in calculation ---\n" %
                  (time.time() - start_time))
    os.chdir("..")
    return data


def parse_args():
    global chunksize
    global output_file
    global mode
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="Chunksize in KB",
                        default=chunksize, type=int)
    parser.add_argument("-o", help="Output file name.",
                        default=output_path, type=str)
    parser.add_argument("-m", help="Mode", default=mode, type=str)
    args = parser.parse_args()
    chunksize = args.c
    output_file = "data/" + args.o
    mode = args.m


def main():
    parse_args()
    generate_data(mode)


if __name__ == "__main__":
    main()
