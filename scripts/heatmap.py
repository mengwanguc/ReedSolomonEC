import os
import numpy as np
import seaborn as sns; sns.set_theme()
import matplotlib.pylab as plt
from matplotlib.colors import LinearSegmentedColormap
from config import constants as const
from lib import functions as func

def GenerateData():
    """
    Creates heatmap array with throughput data.
    """

    # Create empty array that can be populated with data.
    array = [[np.nan for n in range(const.MAX_N + 1)] for k in range(const.MAX_K + 1)]

    # Loop through configurations.
    for n in range(const.MAX_N):
        for k in range(const.MAX_K):

            # Generate througput data.
            print(f"Generating Data for: {n+1}+{k+1}\n")
            func.RunBenchmarkSLEC(n+1, k+1)
            throughput = func.ReadData()
            os.remove(const.THROUGHPUT_FILE)

            # Populate array with throughput data.
            array[k+1][n+1] = throughput

def GenerateHeatmap(data):
    """
    Generates a heatmap given an array of data.
    """

    array = np.array(data, dtype=float)

    # Tuning heatmap parameters.
    myColors = ("Black", "Purple", "Blue", "Red", "Pink", "Orange", "Yellow", "Green")
    cmap = LinearSegmentedColormap.from_list("Custom", myColors, len(myColors))
    mask = np.isnan(array)
    ax = sns.heatmap(array, cmap=cmap, mask=mask, linewidths=0.5, cbar_kws={"label": "Throughput (MB/s)"})

    # X-Y axis labels
    ax.set_ylabel("Parity Units K")
    ax.set_xlabel("Data Units N")
    ax.invert_yaxis()

    # Save and show heatmap.
    plt.savefig(const.OUTPUT_PATH)
    plt.show()

def main():
    func.Recalibrate()
    data = GenerateData()
    GenerateHeatmap(data)

if __name__ == "__main__":
    main()