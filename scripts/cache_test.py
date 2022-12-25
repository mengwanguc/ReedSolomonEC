import os
import re
from lib import functions as func
from config import constants as const

net_n = 16
net_k = 2
loc_n = 8
loc_k = 2


def CacheTest():
    """
    Measures cache stats.
    """
    print("\nMeasuring Cache Statistics\n")

    os.system(f"perf stat -o {const.THROUGHPUT_FILE} -B -e cpu-cycles,instructions,cache-references,cache-misses ./erasure_code/erasure_code_perf_mlec 16 2 8 2 128 > /dev/null")

    with open(const.THROUGHPUT_FILE, "r") as f:
        lines = f.readlines()
        parameters = ["cpu-cycles", "instructions", "cache-references", "cache-misses"]
        stats = []
        for key, line in enumerate(lines):
            for parameter in parameters:
                if (parameter in line):
                    stat = lines[key].split(parameter)[0].strip()
                    stat = float(re.sub("[^0-9.]", "", stat))
                    stats.append(stat)
    os.system(f"rm -rf {const.THROUGHPUT_FILE}")
    return stats


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

    throughput_difference, throughput_change = func.FindDelta(old_throughput, new_throughput)

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
    cache_miss_ratio_diff, cache_miss_ratio_change = func.FindDelta(old_cache_miss_ratio, new_cache_miss_ratio)

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
    miss_ratio_diff, miss_ratio_change = func.FindDelta(old_miss_to_inst_ratio, new_miss_to_inst_ratio)

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
    old_throughput = func.RunBenchmarkMLEC(net_n, net_k, loc_n, loc_k)
    old_cache_stats = CacheTest()
    Compile()
    new_throughput = func.RunBenchmarkMLEC(net_n, net_k, loc_n, loc_k)
    new_cache_stats = CacheTest()
    Summary(old_throughput, new_throughput, old_cache_stats, new_cache_stats)


if __name__ == "__main__":
    main()
