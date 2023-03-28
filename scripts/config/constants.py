"""
Declaration of constants used by Python scripts.
"""

# ------------------------------ Data File Paths ----------------------------- #

# Total SLEC data.
ISA_L_SLEC = "data/isa-l_encode_slec.csv"
JAVA_RS_SLEC = "data/javars_encode_slec.csv"

# Total MLEC data.
ISA_L_MLEC = "data/isa-l_encode_mlec.csv"
JAVA_RS_MLEC = "data/javars_encode_mlec.csv"

# Total LRC data.
ISA_L_LRC = "data/isa-l_encode_lrc.csv"
JAVA_RS_LRC = "data/javars_encode_lrc.csv"

# Durability data.
SLEC_DURABILITY = "data/slec_durability.csv"
MLEC_DURABILITY = "data/mlec_durability.csv"

# --------------------------- Ubiquitous Constants --------------------------- #

# Erasure coding type enumerations
SLEC = 0
MLEC = 1
LRC = 2
DEC_SLEC = 3

# Erasure coding tool enumerations
ISA_L = 0
JAVA_RS = 1

# Chunk size in KB.
CHUNKSIZE = 128

# Erasure coding "mode" to be used:
MODE = ISA_L

# File name for the temporary throughput file.
# (Useful for debugging)
THROUGHPUT_FILE = "throughput.log"

# Output file path for data generation.
# MAKE SURE TO CHANGE THIS WHEN NEEDED.
OUTPUT_PATH = "data/isa-l_encode_slec.csv"
# OUTPUT_PATH = "data/isa-l_encode_mlec_serial.csv"

# Output image for heatmap.
HEATMAP_PATH = "figures/SLEC_encoding_heatmap.png"
# HEATMAP_PATH = "figures/MLEC_serial_10+2_encoding_heatmap.png"

# Input file path to read data from.
DURABILITY_DATA = "data/durability.csv"

# ------------------------------ SLEC Constants ------------------------------ #

# Maximum value for data chunks.
MAX_N = 50

# Maximum value for parity chunks.
MAX_K = 10

# ------------------------------ MLEC Constants ------------------------------ #

# Maximum value for network-level data chunks.
MAX_NET_N = 50

# Maximum value for network-level parity chunks.
MAX_NET_K = 10

# Maximum value for local-level data chunks.
MAX_LOC_N = 50

# Maximum value for local-level parity chunks.
MAX_LOC_K = 10

# ------------------------------- LRC Constants ------------------------------ #

# LRC Option
# 0    LRC
# 1    Optimal LRC
LRC_OPT = 0

# Maximum value for global data chunks.
MAX_LRC_K = 7

# Maximum value for local groups.
MAX_LRC_L = 3

# Maximum value for global parity chunks.
MAX_LRC_R = 4

# Maximum value for local parity chunks.
MAX_LRC_P = 2
