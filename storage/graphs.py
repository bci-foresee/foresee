from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from model import StorageModel
from utils import CellType, OpTarget, ResultType
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def mem_type_comparison(model: StorageModel, result_type: ResultType):
    results = []
    cell_types = []

    # get results from model
    for cell_type in CellType:
        if cell_type == CellType.SRAM and result_type == ResultType.LIFE_EXPECTANCY:
            continue
        model.update_config('cell_type', cell_type.value)
        model.run()
        result = model.get_result(result_type)

        results.append(result)
        cell_types.append(cell_type.value)

    X_axis = np.arange(len(cell_types))
    bar_width = 0.6

    plt.figure(figsize=(12, 8))

    if result_type == ResultType.LIFE_EXPECTANCY:
        min_vals = [x for x, y in results]
        max_vals = [y for x, y in results]

        bars = plt.bar(X_axis,
                       np.array(max_vals) - np.array(min_vals),
                       bar_width,
                       color='skyblue',
                       edgecolor='black',
                       bottom=np.array(min_vals))

        plt.yscale('log')
        plt.ylim([min(min_vals) * 0.1, max(max_vals) * 10])
    else:
        bars = plt.bar(X_axis,
                       results,
                       bar_width,
                       color='skyblue',
                       edgecolor='black')

    # se ticks and labels
    plt.xticks(X_axis, cell_types, rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel("Cell Types", fontsize=14, fontweight='bold', labelpad=15)
    plt.ylabel(result_type.value, fontsize=14, fontweight='bold', labelpad=15)

    plt.title(f"{result_type.value} Across NVM Types",
              fontsize=16,
              fontweight='bold')

    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


def channel_freq_plot(model: StorageModel, result_type: ResultType):
    frequencies = np.arange(10000, 50000, 10000)
    channels = np.arange(40, 200, 40)

    total_result_data = np.zeros((len(channels), len(frequencies)))

    for i, freq in enumerate(frequencies):
        for j, channel in enumerate(channels):
            model.config["experiment"]["write_frequency"] = int(channel * freq)
            model.run()

            total_result_data[j, i] = model.get_result(result_type)

    F, C = np.meshgrid(frequencies, channels)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(F, C, total_result_data, cmap='viridis')

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Channels')
    ax.set_zlabel(result_type.value)

    plt.show()


# runs example graphs
def main():
    model = StorageModel(
        read_frequency=0,
        write_frequency=30000 * 150,
        read_size=0,
        write_size=2,
        cell_type=CellType.RRAM,
        process_node=22,
        opt_target=OpTarget.ReadDynamicEnergy,
        word_width=16,
        capacity=1,
        bits_per_cell=1,
    )
    model.run()
    channel_freq_plot(model, ResultType.TOTAL_POWER)
    mem_type_comparison(model, ResultType.TOTAL_POWER)
    mem_type_comparison(model, ResultType.TOTAL_WRITE_LATENCY)
    mem_type_comparison(model, ResultType.LIFE_EXPECTANCY)
    mem_type_comparison(model, ResultType.AREA)

    #model.cleanup()

    return


if __name__ == "__main__":
    main()
