import pandas

INPUT_PATH = "../data/isa-l_encode_slec.csv"
OUTPUT_PATH = "../paper-figures/test/slec.dat"

df = pandas.read_csv(INPUT_PATH)

df.to_csv(OUTPUT_PATH, sep="\t", index=False)