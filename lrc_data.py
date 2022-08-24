import os
import argparse
import re
import time
from os.path import exists

max_k = 10
max_parity = 4
chunksize = 128
mode = "j"
throughput_filename = "throughput.log"
javars_output_filename = "data/javars_opt_lrc.csv"
isa_l_output_filename = "data/isa-l_opt_lrc.csv"
opt = 1 # 0 for LRC, 1 for Optimal LRC

def run_benchmark(k, l, r, p, mode, opt):
    os.system(f"../run_benchmark.sh -k {k} -l {l} -r {r} -p {p} -c {chunksize} -m {mode} -f {throughput_filename} -e l -t {opt}")

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

def convertible(k, l, r):
    if (k % l != 0):
        return False
    local_group = k/l
    if (r % local_group != 0):
        return False
    return True

def generate_data(mode, opt):

    if (mode == "i"):
        os.chdir("isa-l")
    elif (mode == "j"):
        os.chdir("JavaReedSolomon")
    else:
        print("ERROR: Incorrect mode\n")
        exit()
    for k in range(1, max_k + 1):
        for l in range(1, int(k / 2) + 1):
            for r in range(1, max_parity + 1):
                if not convertible(k, l, r):
                    continue
                    # print("Error: LRC incovertable")
                    # exit()
                for p in range(1, max_parity + 1):
                    config_exists = False
                    file_exists = exists("../" + output_file)
                    if file_exists:
                        with open("../" + output_file, "r") as f:
                            lines = f.readlines()
                            for line in lines:
                                content = line.split(",")
                                if (content[0] == str(k) and content[1] == str(l) and
                                    content[2] == str(r) and content[3] == str(p)):
                                    config_exists = True
                                    break
                    if config_exists:
                        print(f"Data for configuration ({k}, {l}, {r}, {p}) already exists\n")
                        continue
                    start_time = time.time()
                    print(f"Generating Data for: ({k}, {l}, {r}, {p})\n")
                    run_benchmark(k, l, r, p, mode, opt)
                    throughput = point_throughput(mode)
                    os.remove(throughput_filename)
                    with open("../" + output_file, "a+") as f:
                        f.seek(0)
                        firstline = f.readline().rstrip()
                        if firstline != "k,l,r,p,throughput":
                            f.write("k,l,r,p,throughput\n")
                        f.seek(0, 2)
                        f.write(f"{k},{l},{r},{p},{throughput}\n")
                    print(f"Configuration: ({k}, {l}, {r}, {p})\tThroughput: {throughput}\n")
                    print("--- %s seconds elapsed in calculation ---\n" % (time.time() - start_time))
    os.chdir("..")

def parse_args():
    global chunksize
    global output_file
    global mode
    global opt
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="Chunksize in KB", default=chunksize, type=int)
    parser.add_argument("-m", help="Mode", default=mode, type=str)
    parser.add_argument("-o", help="Option", default=opt, type=str)
    args = parser.parse_args()
    chunksize = args.c
    mode = args.m
    opt = args.o
    if mode == "i":
        output_file = isa_l_output_filename
    elif mode == "j":
        output_file = javars_output_filename
    else:
        print("ERROR: Incorrect mode\n")
        exit()

def main():
    parse_args()
    generate_data(mode, opt)

if __name__ == "__main__":
    main()