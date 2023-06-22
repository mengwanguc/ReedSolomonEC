# Reed Solomon Erasure Coding

The purpose of this repository is to provide a code base with a wide repertoire of erasure coding functionality.

Much of the underlying erasure coding is performed by the ISA-L and Java Reed Solomon libraries, which are kept as submodules in this repository.

However, these submodules have been modified to allow increased erasure coding capabilities, such as multi-level erasure coding (MLEC) and locally-reparable codes (LRC).

The `JavaReedSolomon` submodule is based on the [Backblaze Java Reed-Solomon repository](https://github.com/Backblaze/JavaReedSolomon) and the `isa-l` submodule is based on the [Intel ISA-L repository](https://github.com/intel/isa-l).

This repository also contains a series of Python scripts that give useful erasure coding data collection (mostly throughput) and analysis.

### MLEC Paper Artifact:

- The specific script used to generate figure 11 in the "Design Considerations and Analysis of Multi-Level Erasure Coding in Large-Scale Data Centers" paper is the `heatmap.py` script, with details included [here](#available-scripts).

## Erasure Coding Methodology

### Single-Level Erasure Coding

- The method for single-level erasure coding (or SLEC) is to use standard Reed-Solomon erasure coding techniques.
- The algorithm description is available in [this blog post](https://www.backblaze.com/blog/reed-solomon/) by Backblaze.


### Multi-Level Erasure Coding

- The method for multi-level erasure coding (or MLEC) is to combine network-level and local-level erasure coding techniques.
- There are two methods for doing MLEC in the ISA-L library:
1. Stripe-By-Stripe (serially):
    - Take a single stripe and perform network-level erasure coding.
    - With that same stripe still loaded in memory, perform local-level erasure coding.
    - Fetch the next stripe.
2. Split (in parallel):
    - First perform erasure coding on all stripes at the network level.
    - Then perform erasure coding on all stripes at the local level.
    - NOTE: To generate MLEC throughput data in split mode, follow [these instructions](#extraneous-settings-for-certain-erasure-coding-methods) first.


## Setting up Submodules

- To properly clone the repository with its submodules, run the following command:
    ```
    $  git clone --recurse-submodules -j8 https://github.com/rajrana22/ReedSolomonEC.git
    ```
    -  -j8 is an optional performance optimization
- After this is complete, open the ISA-L submodule with the following terminal command:
    ```
    $  cd ReedSolomonEC/isa-l/
    ```
- From there, follow the instructions in the README on how to install the appropriate tools and build the ISA-L library.
- For most users (specifically on a Linux-based OS), this should be as simple as the following terminal commands:

    ```
    $  sudo apt update
    $  sudo apt install gcc g++ make nasm autoconf libtool
    $  ./autogen.sh
    $  ./configure
    $  make
    $  sudo make install
    ```
- After that has been done, run the following command:
    ```
    $  make perfs
    ```

## Configuration

- Inside the `scripts/config/` directory within the main repository there is a configuration file called `constants.py`.
- This file contains all of the configurable variables required for the Python scripts.
- These variables must be configured correctly according to the requirements of the specific Python script before running the script.

### Common Configurations to Change

- `MODE` (ISA-L or JavaRS)
- `OUTPUT_PATH` (output file path)
- `INPUT_PATH` (input file path)
- `MAX_VALUES` (different for each erasure coding type)
- `CHUNKSIZE` (chunk size in MB)

## Datasets

- Dataset files are in the `data/` directory.
- For example:
    - The file `isa-l_decode_slec.csv` is a list of decoding throughput measurements of many different SLEC configurations using the ISA-L library.
    - The file `javars_encode_lrc.csv` is a list of encoding throughput measurements of many different LRC configurations using the JavaRS library.
- These files are usually generated via [multiple value data generation](#end-to-end-multiple-value-data-generation).
- These files can be used in scripts for data processing and graph generation.

## Data Generation

### Single Value Data Generation

- Consider the SLEC throughput for a specific configuration of `n` data chunks and `k` parity chunks with a chunk size of `chunksize` MB.
- The following command will measure the encoding throughput for such a configuration using a modified version of the ISA-L library:
    ```
    $  ./isa-l/erasure_code/erasure_code_perf_from_file n k chunksize
    ```
- Similarly, the following command will measure the encoding throughput for such a configuration using a modified version of the JavaRS library:
    ```
    $  ./gradlew -PmainClass=com.backblaze.erasure.ReedSolomonBenchmarkSLEC run n k chunksize
    ```
- Now consider the MLEC throughput for a specific configuration of `net_n` network-level data chunks, `net_k` network-level parity chunks, `loc_n` local-level data chunks, and `loc_k` local-level parity chunks, with a chunk size of `chunksize` MB.
- The following command will measure the encoding throughput for such a configuration in parallel on a modified version of the ISA-L library:
    ```
    $  ./isa-l/erasure_code/erasure_code_perf_mlec net_n net_k loc_n loc_k chunksize
    ```
- The following command will measure the encoding throughput for such a configuration serially on a modified version of the ISA-L library:
    ```
    $  ./isa-l/erasure_code/erasure_code_perf_mlec_split net_n net_k loc_n loc_k chunksize
    ```

### Multiple Value Data Generation

- This section outlines in detail how to generate multiple data values for throughput measurements using the ISA-L library.
- The following is an example of the end-to-end steps for generating SLEC encoding throughput data:
1. Open `scripts/config/constants.py` and set the following variable values:
    - `MODE = ISA_L`
    - `OUTPUT_PATH = "data/<desired_filename>.csv"`
    - `MAX_N = 50` (for configurations with number of data chunks from 1 to 50)
    - `MAX_K = 10` (for configurations with number of parity chunks from 1 to 10)
2. In the terminal, change the current working directory to the `scripts/` directory using the following command:
    ```
    $  cd scripts/
    ```
3. In the terminal, run the following command:
    ```
    $  python3 gen_slec.py
    ```
4. The terminal output will display information regarding the data collection process.
5. Upon completion of the script's execution, the file `<desired_filename>.csv` within the `data/` directory will have the records of each collected measurement.
- If generating throughput data of other erasure coding types, simply run the corresponding script with the appropriate configuration settings.
    - For instance, if MLEC or LRC encoding throughput data is required, some configuration settings that must be set are:
        - `MAX_NET_N`, `MAX_NET_K`, `MAX_LOC_N`, and `MAX_LOC_K` for MLEC
        - `LRC_OPT`, `MAX_LRC_K`, `MAX_LRC_L`, `MAX_LRC_R`, and `MAX_LRC_P` for LRC
    - NOTE: To generate SLEC decoding throughput data or MLEC throughput data in split mode, follow [these instructions](#extraneous-settings-for-certain-erasure-coding-methods) first.

## Available Scripts

- All available Python scripts are contained within the `scripts/` directory
- `gen_slec.py`:
  - Generates SLEC throughput according to the `MAX_VALUE` constants specified in the configuration file.
- `gen_lrc.py`:
  - Generates LRC throughput according to the `MAX_VALUE` constants specified in the configuration file.
- `heatmap.py`:
  - Generates a heatmap of throughput performance for SLEC, MLEC, and .
  - This script uses experiment results in file ???.log to reproduce Figure 11 "Encoding throughput for various (k+p)" in the MLEC paper.
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

- Inside the `scripts/lib/` directory there is a file called `functions.py` that contains shared functions that are used by multiple Python scripts.
- Can be helpful when writing a new script.
- Modify where necessary according to needs.

## Other Notes

### Extraneous Settings for Certain Erasure Coding Methods

- Before running any script, the following must be done:
    - Open `scripts/lib/functions.py`.
    - If running MLEC in parallel (split mode):
        - Go to line 38 in the `RunBenchmarkMLEC` function definition.
        - Change the `os.system` method option from `-e {MLEC}` to `-e {MLEC_SPLIT}`.
    - If running SLEC for decoding measurements:
        - Go to line 26 in the `RunBenchmarkSLEC` function definition.
        - Change the `os.system` method option from `-e {SLEC}` to `-e {DEC_SLEC}`.
- Note that this inconvenience is due to a lack of functionality with the decision to include the in-parallel MLEC throughput data collection method.
