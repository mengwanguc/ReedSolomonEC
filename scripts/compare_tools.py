import os
import matplotlib.pyplot as plt
from lib import constants as const
from lib import functions as func

def ReadDurability():
    """
    Reads durability data.
    """
    ...

def ReadThroughput():
    """
    Reads throughput data.
    """
    ...

def GenerateScatterplot():
    if (const.MODE = "i"):
        ...
    else if (const.MODE = "j"):
        ...
    else:
        print("ERROR: Incorrect Mode\n")
        exit(1)

    isa_s_dur, isa_s_through = isa_s
    isa_m_dur, isa_m_through = isa_m
    java_s_dur, java_s_through = java_s
    java_m_dur, java_m_through = java_m
    plt.plot(isa_s_dur, isa_s_through, c ="red", label="ISA-L single-level")
    plt.plot(isa_m_dur, isa_m_through, c ="blue", label="ISA-L multi-level")
    plt.plot(java_s_dur, java_s_through, c ="orange", label="JavaRS single-level")
    plt.plot(java_m_dur, java_m_through, c ="green", label="JavaRS multi-level")

    # Graph labels.
    plt.xlabel("Durability (nines)")
    plt.ylabel("Throughput (MB/s)")
    plt.legend(loc='upper right')

    # Save and show graph.
    plt.savefig(f"{const.OUTPUT_PATH}")
    plt.show()

def main():
    funconst.Recalibrate()
    GenerateScatterplot()

if __name__ == "__main__":
    main()