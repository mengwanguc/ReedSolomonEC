from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pylab as plt
import os
import numpy as np
import seaborn as sns
sns.set_theme()

MAX_N = 50
MAX_K = 15
INPUT_PATH = "slec.dat"

def GetLines():
    """
    Fetches the lines in the output file.
    """
    file_exists = os.path.exists(INPUT_PATH)
    if file_exists:
        with open(INPUT_PATH, "r") as f:
            lines = f.readlines()
            return lines

def ReadData():
    """
    Creates heatmap array with throughput data.
    """

    # Create empty array that can be populated with data.
    array = [[np.nan for n in range(MAX_N + 1)] for k in range(MAX_K + 1)]

    lines = GetLines()
    for line in lines[1:]:
        n, k, throughput = line.split("\t")
        n = int(n)
        k = int(k)
        throughput, _ = throughput.split("\n")
        # Populate array with throughput data.
        array[k][n] = float(throughput) / 1000

    return array


def GenerateHeatmap(data):
    """
    Generates a heatmap given an array of data.
    """

    array = np.array(data, dtype=float)

    # Define custom colormap
    colorlist = ['black', 'maroon', 'red', '#FF4000', '#FF8000', '#FFC000', 'yellow', '#E6FF00', '#B3FF00', 'lime', '#00D100', '#009500', 'darkgreen']
    n_colors = 256  # number of colors in the colormap
    cmap = LinearSegmentedColormap.from_list("Custom", colorlist, N=n_colors)

    # Generate heatmap
    mask = np.isnan(array)
    plt.figure(figsize=(16, 6))
    ticks = [0, 2, 4, 6, 8, 10, 12]
    vmax = 12
    vmin = 0
    cbar_kws = {"label": "Throughput (GB/s)", "drawedges": False, "shrink": 0.5, "spacing": "proportional", "ticks": ticks}
    ax = sns.heatmap(array, cmap=cmap, mask=mask, linewidths=0.5, cbar_kws=cbar_kws, square=True, vmax=vmax, vmin=vmin)

    # X-Y axis labels
    ax.set_ylabel("Parity Units K", fontsize=12)
    ax.set_xlabel("Data Units N", fontsize=12)
    ax.invert_yaxis()

    # Set axis label settings
    x_tick_positions = np.arange(0, len(data[0]), 5)
    x_tick_labels = [str(x) for x in x_tick_positions]
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(x_tick_labels, rotation=0, va='center')

    y_tick_positions = np.arange(0, len(data), 2)
    y_tick_labels = [str(y) for y in y_tick_positions]
    ax.set_yticks(y_tick_positions)
    ax.set_yticklabels(y_tick_labels, rotation=0, va='center')

    # Set title
    ax.set_title("SLEC Encoding Throughput Heatmap", fontdict={'fontsize': 16}, y=1.08)

    # Set boundary around outside of heatmap
    for _, spine in ax.spines.items():
        spine.set_visible(True)
        spine.set_edgecolor('black')
        spine.set_linewidth(0.5)

    # Save and show heatmap.
    plt.savefig("figure.eps",  bbox_inches="tight")
    plt.show()


def main():
    array = ReadData()
    GenerateHeatmap(array)


if __name__ == "__main__":
    main()
