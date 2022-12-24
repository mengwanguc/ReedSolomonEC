
## Setting up Submodules

- To properly clone the repository with its submodules, run the following command:
    - `git clone --recurse-submodules -j8 https://github.com/rajrana22/ReedSolomonEC.git`
    -  -j8 is an optional performance optimization
- The `isa-l` submodule needs to be on the `ReedSolomon` branch.
- The `JavaReedSolomon` submodule is based on the [Backblaze Java Reed-Solomon repository](https://github.com/Backblaze/JavaReedSolomon).
- The `isa-l` submodule is forked from the [Intel ISA-L repository](https://github.com/intel/isa-l).

---

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

- SLEC throughput can be measured using the following command:
    - `python3 gen_slec.py`

---

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

- MLEC throughput can be measured using the following command:
    -  `python3 gen_mlec.py`

---

## Heatmap Generation Steps:

- Command to run the heatmap generation script:
    - `python3 heatmap.py [-n -k -m -o]`
- Parameters:
  - `n` = Number of data shards (default = `17`).
  - `k` = Number of parity shards (defualt = `3`).
  - `c` = Chunksize in KB (default = `128`).
  - `m` = Mode (default = `i`):
    - `i` to use the ISA-L tool.
    - `j` to use the JavaReedSolomon tool.
  - `o` = Heatmap filename with appropriate image extension (default = `heatmap.png`).

---

## Back-End Files

- `run_benchmark.sh`:

---