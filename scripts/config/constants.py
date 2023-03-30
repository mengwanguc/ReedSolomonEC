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
# OUTPUT_PATH = "data/isa-l_encode_slec.csv"
# OUTPUT_PATH = "data/isa-l_encode_mlec_serial.csv"
OUTPUT_PATH = "data/isa-l_encode_lrc.csv"

# Input file path for data usage.
# INPUT_PATH = "data/isa-l_encode_slec.csv"
# INPUT_PATH = "data/isa-l_encode_mlec_serial.csv"
INPUT_PATH = "data/isa-l_encode_lrc.csv"

# Output image for heatmap.
# HEATMAP_PATH = "figures/SLEC_encoding.png"
# HEATMAP_PATH = "figures/Num_Cores_SLEC.png"
# HEATMAP_PATH = "figures/Num_Cores_5+1_loc_MLEC.png"
# HEATMAP_PATH = "figures/MLEC_serial_5+1_loc_encoding.png"
HEATMAP_PATH = "figures/Num_Cores_LRC.png"
# HEATMAP_PATH = "figures/Num_Cores_LRC.png"

# Input file path to read durability data from.
DURABILITY_DATA = "data/durability.csv"

# ------------------------------ SLEC Constants ------------------------------ #

# Maximum value for data chunks.
MAX_N = 50

# Maximum value for parity chunks.
MAX_K = 10

# ------------------------------ MLEC Constants ------------------------------ #

# Maximum value for network-level data chunks.
MAX_NET_N = 20

# Maximum value for network-level parity chunks.
MAX_NET_K = 5

# Maximum value for local-level data chunks.
MAX_LOC_N = 20

# Maximum value for local-level parity chunks.
MAX_LOC_K = 5

# ------------------------------- LRC Constants ------------------------------ #

# LRC Option
# 0    LRC
# 1    Optimal LRC
LRC_OPT = 0

# Maximum value for global data chunks.
MAX_LRC_K = 50

# Maximum value for local groups.
MAX_LRC_L = 2

# Maximum value for global parity chunks.
MAX_LRC_R = 10

# Maximum value for local parity chunks.
MAX_LRC_P = 1
