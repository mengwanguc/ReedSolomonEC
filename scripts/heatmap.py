import os
import numpy as np
import seaborn as sns; sns.set_theme()
import matplotlib.pylab as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
from config import constants as const
from lib import functions as func

def ReadData():
    """
    Creates heatmap array with throughput data.
    """

    # Create empty array that can be populated with data.
    array = [[np.nan for n in range(const.MAX_N + 1)] for k in range(const.MAX_K + 1)]

    lines = func.GetLines()
    for line in lines[1:]:
        n, k, throughput = line.split(",")
        n = int(n)
        k = int(k)
        throughput, _ = throughput.split("\n")
        # Populate array with throughput data.
        array[k][n] = float(throughput)
        # net_n, net_k, loc_n, loc_k, throughput = line.split(",")
        # net_n = int(net_n)
        # net_k = int(net_k)
        # loc_n = int(loc_n)
        # loc_k = int(loc_k)
        # if (net_n == 5) and (net_k == 1):
        #     throughput, _ = throughput.split("\n")
        #     # Populate array with throughput data.
        #     array[loc_k][loc_n] = float(throughput)

    return array

def GenerateHeatmap(data):
    """
    Generates a heatmap given an array of data.
    """

    array = np.array(data, dtype=float)

    # Tuning heatmap parameters.
    # cmap = LinearSegmentedColormap.from_list("", ["red", "purple", "orange", "yellow", "lightgreen"], N=100)
    colorlist = ['black', 'maroon', 'red', '#ff7200', '#FFAF00', 'yellow', 'lime', '#00AF00', 'darkgreen', 'pink']
    # myColors = ("Red", "Purple", "Orange", "Yellow", "Green")
    cmap = LinearSegmentedColormap.from_list("Custom", colorlist, len(colorlist))
    bounds = [0, 1000, 2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000]
    norm = BoundaryNorm(bounds, len(colorlist) - 1)
    mask = np.isnan(array)

    plt.figure(figsize=(16, 6))
    ticks = np.arange(0, 12001, 2000)
    cbar_kws = {"label": "Throughput (MB/s)", "drawedges": False, "shrink": 0.5, "spacing": "proportional", "ticks": ticks}
    ax = sns.heatmap(array, cmap=cmap, norm=norm, mask=mask, linewidths=0.5, cbar_kws=cbar_kws, square=True)

    # cbar = plt.colorbar(ax.collections[0], ticks=ticker.MultipleLocator(2000), **cbar_kws)
    # cbar.ax.yaxis.set_tick_params(width=0)

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



    # Set boundary around outside of heatmap
    for _, spine in ax.spines.items():
        spine.set_visible(True)
        spine.set_edgecolor('black')
        spine.set_linewidth(0.5)

    # Save and show heatmap.
    plt.savefig(const.HEATMAP_PATH)
    plt.show()

def main():
    func.Recalibrate()
    array = ReadData()
    GenerateHeatmap(array)

if __name__ == "__main__":
    main()