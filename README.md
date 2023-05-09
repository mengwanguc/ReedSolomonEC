# Reed Solomon Erasure Coding

The purpose of this repository is to provide a code base with a wide repertoire of erasure coding functionality.

Much of the underlying erasure coding is performed by the ISA-L and Java Reed Solomon libraries, which are kept as submodules in this repository.

However, these submodules have been modified to allow increased erasure coding capabilities, such as multi-level erasure coding (MLEC) and locally-reparable codes (LRC).

The `JavaReedSolomon` submodule is based on the [Backblaze Java Reed-Solomon repository](https://github.com/Backblaze/JavaReedSolomon) and the `isa-l` submodule is based on the [Intel ISA-L repository](https://github.com/intel/isa-l).

This repository also contains a series of Python scripts that give useful erasure coding data collection (mostly throughput) and analysis.


## Setting up Submodules

- To properly clone the repository with its submodules, run the following command:
    - `git clone --recurse-submodules -j8 https://github.com/rajrana22/ReedSolomonEC.git`
    -  -j8 is an optional performance optimization
- The `isa-l` submodule needs to be on the `ReedSolomon` branch.


## Configuration

- Inside `scripts/config` directory there is a configuration file called `constants.py`.
- This file contains all of the constants required for the Python scripts.
- These constants must be configured correctly according to the requirements of the specific Python script.

### Common Configurations to Change

- `MODE`
- `OUTPUT_PATH`
- `MAX_VALUES` (different for each erasure coding type)
- `CHUNKSIZE`


## Single-Level Erasure Coding

- The method for single-level erasure coding (or SLEC) is to use standard Reed-Solomon erasure coding techniques.

### Datasets

- Files are in the `data` folder.
- The file `total_isa-l_slec.csv` is a dataset of throughput measurements of many different SLEC configurations using the ISA-L library.
- The file `total_javars_slec.csv` is a dataset of throughput measurements of many different SLEC configurations using the JavaRS library.

### Data Generation

- Consider the SLEC throughput for a specific configuration of `n` data chunks, `k` parity chunks, and a chunk size of `chunksize` MB.
- The throughput for such a configuration can be measured using the following commands for ISA-L and JavaRS, respectively:
```
./isa-l/erasure_code/erasure_code_perf_from_file n k chunksize
```
```
./gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmarkSLEC run n k chunksize
```


## Multi-Level Erasure Coding

- The method for multi-level erasure coding (or MLEC) is to combine network-level and local-level erasure coding techniques.
- There are two methods for doing MLEC in the ISA-L library:
1. Split:
    - First perform erasure coding on all stripes at the network level.
    - Then perform erasure coding on all stripes at the local level.
2. Stripe-By-Stripe:
    - Take a single stripe and perform network-level erasure coding.
    - With that same stripe still loaded in memory, perform local-level erasure coding.
    - Fetch the next stripe.


### Datasets

- Files are in the `data` folder.
- The file `total_isa-l_mlec.csv` is a dataset of throughput measurements of many different MLEC configurations using the ISA-L library.
- The file `total_javars_mlec.csv` is a dataset of throughput measurements of many different MLEC configurations using the JavaRS library.

### Data Generation

- Consider the MLEC throughput for a specific configuration of `net_n` network-level data chunks, `net_k` network-level parity chunks, `loc_n` local-level data chunks, `loc_k` local-level parity chunks, and a chunk size of `chunksize` MB.
- The throughput for such a configuration can be measured using the following commands for ISA-L using the split method, ISA-L using the stripe-by-stripe method, and JavaRS, respectively:
```
./isa-l/erasure_code/erasure_code_perf_mlec net_n net_k loc_n loc_k chunksize
```
```
./gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmarkMLEC run net_n net_k loc_n loc_k chunksize
```


## Available Scripts

- `gen_slec.py`:
  - Generates SLEC throughput according to the `MAX_VALUE` constants specified in the configuration file.
- `gen_lrc.py`:
  - Generates LRC throughput according to the `MAX_VALUE` constants specified in the configuration file.
- `heatmap.py`:
  - Generates a heatmap of throughput performance for MLEC.
- `compare_tools.py`:
  - Compares the throughput performance of the ISA-L erasure coding tool to that of the Java Reed-Solomon erasure coding tool.
  - Works with different erasure coding types.
- `cache_test.py`:
  - Test script for measuring and summarizing cache and throughput performance.
- `reconstruct_figure.py`:
  - Reconstructs figure 1 from the ECWide paper.
  - Requires the correct throughput input.


## Back-End Files

- `run_benchmark.sh`:
  - Shell script that runs the proper throughput benchmarking commands according to specified flags.
  - Look into file to see all of the possible flags.

### Shared Functions

- Inside the `scripts/lib` directory there is a file called `functions.py` that contains shared functions that are used by multiple Python scripts.
- Can be helpful when writing a new script.
- Modify where necessary according to needs.
