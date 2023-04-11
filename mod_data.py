import pandas

data = "data/isa-l_encode_slec.csv"
output = "F/tp_SLEC/slec.dat"

df = pandas.read_csv(data)

# df = df.replace('nan','')

df.to_csv(output, sep="\t", index=False)