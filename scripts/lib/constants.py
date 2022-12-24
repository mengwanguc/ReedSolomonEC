"""
Declaration of constants used by Python scripts.
"""

# ------------------------------ Data File Paths ----------------------------- #

# Total SLEC data.
isa_l_slec = "data/total_isa-l_slec.csv"
javars_slec = "data/total_javars_slec.csv"

# Total MLEC data.
isa_l_mlec = "data/total_isa-l_mlec.csv"
javars_mlec = "data/total_javars_mlec.csv"

# Total LRC data.
isa_l_lrc = "data/total_isa-l_lrc.csv"
javars_lrc = "data/total_javars_lrc.csv"

# --------------------------- Ubiquitous Constants --------------------------- #

# Chunk size in MB.
CHUNKSIZE = 128

# Erasure coding "mode" to be used:
#   "i" = ISA-L tool
#   "j" = JavaRS tool
MODE = "i"

# File name for the temporary throughput file.
# (Useful for debugging)
THROUGHPUT_FILE = "throughput.log"

# Output file path for data generation.
OUTPUT_PATH = isa_l_slec

# Input file path to read data from.
DURABILITY_DATA = "data/durability.csv"

# ------------------------------ SLEC Constants ------------------------------ #

# Maximum value for data chunks.
MAX_N = 17

# Maximum value for parity chunks.
MAX_K = 3

# ------------------------------ MLEC Constants ------------------------------ #

# Maximum value for network-level data chunks.
MAX_NET_N = 16

# Maximum value for network-level parity chunks.
MAX_NET_K = 2

# Maximum value for local-level data chunks.
MAX_LOC_N = 8

# Maximum value for local-level parity chunks.
MAX_LOC_K = 2
