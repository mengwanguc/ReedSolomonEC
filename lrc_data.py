import os
import argparse
import re
import time

max_k = 12
max_parity = 4
chunksize = 128
throughput_filename = "throughput.log"
output_filename = "data.log"

def run_benchmark(k, l, r, p, mode):
    os.system(f"../run_benchmark.sh -k {k} -l {l} -r {r} -p {p} -c {chunksize} -m {mode} -f {throughput_filename} -e l")

def point_throughput(mode):
    with open(throughput_filename, "r") as f:
        lines = f.readlines()
    for key, line in enumerate(lines):
        if ((mode == "i") and ("runtime" in line)):
            desired_line = lines[key].split("in")[1].split("sec")[1].lstrip()
            desired_line = desired_line.split("=")[1].split("MB/s")[0]
            desired_line = desired_line.lstrip().rstrip()
        if ((mode == "j") and ("Summary:" in line)):
            desired_line = lines[key + 2]
    throughput = float(re.sub("[^0-9.]", "", desired_line))
    return throughput

def convertable(k, l, r):
    if (k % l != 0):
        return False
    local_group = k/l
    if (r % local_group != 0):
        return False
    return True

def generate_data(mode):

    data = []

    if (mode == "i"):
        os.chdir("isa-l")
    elif (mode == "j"):
        os.chdir("JavaReedSolomon")
    else:
        print("ERROR: Incorrect mode\n")
        exit()
        
    for k in range(1, max_k):
        for l in range(1, int(max_k / 2) + 1):
            for r in range(1, max_parity + 1):
                if not convertable(k, l, r):
                    continue
                    # print("Error: LRC incovertable")
                    # exit()
                for p in range(1, max_parity + 1):
                    start_time = time.time()
                    print(f"Generating Data for: ({k}, {l}, {r}, {p})\n")
                    run_benchmark(k, l, r, p, mode)
                    throughput = point_throughput(mode)
                    os.remove(throughput_filename)
                    data.append(((k, l, r, p), throughput))
                    print(f"Configuration: ({k}, {l}, {r}, {p})\tThroughput: {throughput}\n")
                    print("--- %s seconds elapsed in calculation ---\n" % (time.time() - start_time))
    os.chdir("..")
    return data

def write_data(data):
    with open(output_filename, "w") as f:
        for datum in data:
            config, throughput = datum
            k, l, r, p = config
            print(f"Configuration: ({k}, {l}, {r}, {p})\tThroughput: {throughput}\n")
            f.write(f"({k}, {l}, {r}, {p})\t{throughput}\n")

def parse_args():
    global chunksize
    global output_file
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="Chunksize in KB", default=chunksize, type=int)
    parser.add_argument("-o", help="Output file name.", default=output_filename, type=str)
    args = parser.parse_args()
    chunksize = args.c
    output_file = "data/" + args.o

def main():
    parse_args()
    data = generate_data("j")
    write_data(data)

if __name__ == "__main__":
    main()