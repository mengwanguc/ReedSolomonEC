import os
import argparse
import re
import time
from os.path import exists
import functions as func

chunksize = 128
throughput_filename = "throughput.log"
    
def CalculateThroughput(net_n=16, net_k=2, loc_n=8, loc_k=2):
    """
    Measures throughput performance.
    """
    print("\nCalculating Throughput...\n")
    os.system(f"../run_benchmark.sh -a {net_n} -b {net_k} -n {loc_n} -k {loc_k} -c {chunksize} -m i -f {throughput_filename} -e m")
    throughput = func.GenerateSinglePoint(net_n, net_k, loc_n, loc_k)
    os.system(f"rm -rf {throughput_filename}")
    return throughput

def CacheTest():
    """
    Measures cache stats.
    """
    print("\nMeasuring Cache Statistics\n")
    os.system(f"perf stat -o {throughput_filename} -B -e cpu-cycles,instructions,cache-references,cache-misses ./erasure_code/erasure_code_perf_mlec 16 2 8 2 128 > /dev/null")
    with open(throughput_filename, "r") as f:
        lines = f.readlines()
    for key, line in enumerate(lines):
        if ("cpu-cycles" in line):
            cycles = lines[key].split("cpu-cycles")[0].strip()
        if ("instructions" in line):
            instructions = lines[key].split("instructions")[0].strip()
        if ("cache-references" in line):
            cache_refs = lines[key].split("cache-references")[0].strip()
        if ("cache-misses" in line):
            cache_misses = lines[key].split("cache-misses")[0].strip()
    cycles = float(re.sub("[^0-9.]", "", cycles))
    instructions = float(re.sub("[^0-9.]", "", instructions))
    cache_refs = float(re.sub("[^0-9.]", "", cache_refs))
    cache_misses = float(re.sub("[^0-9.]", "", cache_misses))
    stats = (cycles, instructions, cache_refs, cache_misses)
    os.system(f"rm -rf {throughput_filename}")
    return stats

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

def CacheRatio(value1, value2):
    """
    Measures a cache ratio.
    """
    return (value1 / value2)

def Summary(old_throughput, new_throughput, old_cache_stats, new_cache_stats):
    """
    Calculates and reports differences in throughput and cache statistics.
    """
    print("Old Throughput: " + str(old_throughput) + " MB/s\n")
    print("New Throughput: " + str(new_throughput) + " MB/s\n")

    throughput_difference, throughput_change = FindDelta(old_throughput, new_throughput)

    if (throughput_difference >= 0):
        print("Difference in Throughput: +" + "{:.2f}".format(throughput_difference) + " MB/s\n")
        print("Percent Increase in Throughput: +" + "{:.4f}".format(throughput_change) + "%\n")
    else:
        print("Difference in Throughput: " + "{:.2f}".format(throughput_difference) + " MB/s\n")
        print("Percent Increase in Throughput: " + "{:.4f}".format(throughput_change) + "%\n")
    
    old_cycles, old_instructions, old_cache_refs, old_cache_misses = old_cache_stats
    new_cycles, new_instructions, new_cache_refs, new_cache_misses = new_cache_stats

    old_cache_miss_ratio = CacheRatio(old_cache_misses, old_cache_refs)
    new_cache_miss_ratio = CacheRatio(new_cache_misses, new_cache_refs)
    cache_miss_ratio_diff, cache_miss_ratio_change = FindDelta(old_cache_miss_ratio, new_cache_miss_ratio)

    print("\nOld Cache Miss Ratio: " + str(old_cache_miss_ratio) + "\n")
    print("New Cache Miss Ratio: " + str(new_cache_miss_ratio) + "\n")

    if (cache_miss_ratio_diff >= 0):
        print("Difference in Cache Miss Ratio: +" + "{:.4f}".format(cache_miss_ratio_diff) + "\n")
        print("Percent Increase in Cache Miss Ratio: +" + "{:.4f}".format(cache_miss_ratio_change) + "%\n")
    else:
        print("Difference in Cache Miss Ratio: " + "{:.4f}".format(cache_miss_ratio_diff) + "\n")
        print("Percent Increase in Cache Miss Ratio: " + "{:.4f}".format(cache_miss_ratio_change) + "%\n")

    old_miss_to_inst_ratio = CacheRatio(old_cache_misses, old_instructions)
    new_miss_to_inst_ratio = CacheRatio(new_cache_misses, new_instructions)
    miss_ratio_diff, miss_ratio_change = FindDelta(old_miss_to_inst_ratio, new_miss_to_inst_ratio)

    print("\nOld Cache Miss to Instructions Ratio: " + str(old_miss_to_inst_ratio) + "\n")
    print("New Cache Miss to Instructions Ratio: " + str(new_miss_to_inst_ratio) + "\n")

    if (miss_ratio_diff >= 0):
        print("Difference in Cache Miss to Instructions Ratio: +" + "{:.4f}".format(miss_ratio_diff) + "\n")
        print("Percent Increase in Cache Miss to Instructions Ratio: +" + "{:.4f}".format(miss_ratio_change) + "%\n")
    else:
        print("Difference in Cache Miss to Instructions Ratio: " + "{:.4f}".format(miss_ratio_diff) + "\n")
        print("Percent Increase in Cache Miss to Instructions Ratio: " + "{:.4f}".format(miss_ratio_change) + "%\n")


def Compile():
    print("Compiling...\n")
    os.system("make perfs")

def main():
    os.chdir("isa-l")
    old_throughput = CalculateThroughput()
    old_cache_stats = CacheTest()
    Compile()
    new_throughput = CalculateThroughput()
    new_cache_stats = CacheTest()
    Summary(old_throughput, new_throughput, old_cache_stats, new_cache_stats)

if __name__ == "__main__":
    main()