from matplotlib import pyplot as plt
from matplotlib.ticker import LogLocator
import numpy as np
from model import StorageModel
from utils import CellType, ResultType
import matplotlib.pyplot as plt


def mem_type_comparison(model: StorageModel, result_type: ResultType):
    results = []
    cell_types = []

    # get results from model
    for cell_type in CellType:
        if cell_type == CellType.SRAM and result_type == ResultType.LIFE_EXPECTANCY:
            continue
            print(cell_type)
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
    frequencies = np.arange(10000, 100001, 10000)
    channels = np.arange(4, 100, 4)
    samples = 8192

    total_result_data = np.zeros((len(channels), len(frequencies)))
    colors = np.zeros((len(channels), len(frequencies)), dtype=object)

    for i, freq in enumerate(frequencies):
        for j, channel in enumerate(channels):
            input_writes = channel * samples * 32 / 8
            fft_writes = channel * 5 * 32 / 8
            svm_writes = 3
            thr_writes = 1

            write_size = input_writes + fft_writes + svm_writes + thr_writes
            read_size = input_writes + fft_writes + svm_writes

            model.config["experiment"]["write_size"] = write_size
            model.config["experiment"]["read_size"] = read_size
            model.run()

            total_latency = model.get_result(ResultType.TOTAL_LATENCY)

            result = (model.get_result(ResultType.TOTAL_ENERGY) /
                      (8192 / (freq * channel))) + model.get_result(
                          ResultType.LEAKAGE_POWER)
            total_result_data[j, i] = result

            if total_latency >= (8192 / (freq * channel)) * 1000:
                colors[j, i] = 'red'
            else:
                colors[j, i] = 'green'

            if channel == 16 and freq == 30000:
                print(total_latency)

    F, C = np.meshgrid(frequencies, channels)

    frequencies_flat = F.flatten()
    channels_flat = C.flatten()
    results_flat = total_result_data.flatten()
    colors_flat = colors.flatten()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    scatter1 = ax.scatter(frequencies_flat[colors_flat == 'green'],
                          channels_flat[colors_flat == 'green'],
                          results_flat[colors_flat == 'green'],
                          c='green',
                          label='Satisfy Latency Limit')
    scatter2 = ax.scatter(frequencies_flat[colors_flat == 'red'],
                          channels_flat[colors_flat == 'red'],
                          results_flat[colors_flat == 'red'],
                          c='red',
                          label='Do Not Satisfy Latency Limit')

    ax.set_xlabel('Sampling Rate (Hz)')
    ax.set_ylabel('Channel Count')
    ax.set_zlabel(result_type.value)

    ax.legend(loc='upper left', fontsize='small')

    plt.show()


def plot_power_vs_memory_types(model: StorageModel):
    import numpy as np
    import matplotlib.pyplot as plt

    memory_types = [cell_type for cell_type in CellType]
    results = {
        'Total Power': [],
        'Dynamic Write Power': [],
        'Dynamic Read Power': [],
        'Leakage Power': []
    }

    colors = ['lightcoral', '#2ecc71', '#f1c40f', '#9b59b6']
    hatches = ['///', '', '', '']

    for cell_type in memory_types:
        model.update_config('cell_type', cell_type.value)
        model.run()

        results['Total Power'].append(model.get_result(ResultType.TOTAL_POWER))
        results['Dynamic Write Power'].append(
            model.get_result(ResultType.TOTAL_DYNAMIC_WRITE_POWER))
        results['Dynamic Read Power'].append(
            model.get_result(ResultType.TOTAL_DYNAMIC_READ_POWER))
        results['Leakage Power'].append(
            model.get_result(ResultType.LEAKAGE_POWER))

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(memory_types))
    width = 0.2

    for i, key in enumerate(results):
        ax.bar(x + (i - 1.5) * width,
               results[key],
               width,
               label=key,
               color=colors[i],
               hatch=hatches[i],
               edgecolor='black',
               zorder=3)

    ax.set_xlabel('Cell Type')
    ax.set_ylabel('Power (mW)')

    ax.set_xticks(x)
    ax.set_xticklabels([cell_type.value for cell_type in CellType],
                       rotation=45)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=2)

    ax.set_yscale('log')
    ax.grid(which='both', linestyle='-', linewidth=0.5, alpha=0.7, zorder=0)
    ax.grid(which='major', linestyle='-', linewidth=1.2, alpha=0.9, zorder=0)

    plt.subplots_adjust(left=0.28,
                        bottom=0.146,
                        right=0.788,
                        top=0.874,
                        wspace=0.2,
                        hspace=0.2)

    fig.tight_layout()

    plt.show()


def plot_latency_vs_memory_types(model: StorageModel):
    import numpy as np
    import matplotlib.pyplot as plt

    memory_types = [cell_type for cell_type in CellType]
    print(memory_types)
    results = {'Total Latency': [], 'Read Latency': [], 'Write Latency': []}

    colors = ['#3498db', '#f1c40f', '#9b59b6']
    hatches = ['///', '', '']

    for cell_type in memory_types:
        model.update_config('cell_type', cell_type.value)
        model.run()
        if cell_type == CellType.STT:
            print(model.get_result(ResultType.TOTAL_LATENCY))
            print(model.get_result(ResultType.WORD_WIDTH))

        results['Total Latency'].append(
            model.get_result(ResultType.TOTAL_LATENCY))
        results['Write Latency'].append(
            model.get_result(ResultType.TOTAL_WRITE_LATENCY))
        results['Read Latency'].append(
            model.get_result(ResultType.TOTAL_READ_LATENCY))

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(memory_types))
    width = 0.2

    for i, key in enumerate(results):
        ax.bar(x + (i - 1.5) * width,
               results[key],
               width,
               label=key,
               color=colors[i],
               hatch=hatches[i],
               edgecolor='black',
               zorder=3)

    ax.set_xlabel('Cell Type')
    ax.set_ylabel('Latency (ms)')

    ax.set_xticks(x)
    ax.set_xticklabels([cell_type.value for cell_type in CellType],
                       rotation=45)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=3)

    ax.set_yscale('log')
    ax.grid(which='both', linestyle='-', linewidth=0.5, alpha=0.7, zorder=0)
    ax.grid(which='major', linestyle='-', linewidth=1.2, alpha=0.9, zorder=0)

    plt.subplots_adjust(left=0.28,
                        bottom=0.146,
                        right=0.788,
                        top=0.874,
                        wspace=0.2,
                        hspace=0.2)

    fig.tight_layout()

    plt.show()


def plot_area_vs_memory_types(model: StorageModel):
    memory_types = [cell_type for cell_type in CellType]
    areas = []
    memory_type_labels = []

    for cell_type in memory_types:
        model.update_config('cell_type', cell_type.value)
        model.run()

        area = model.get_result(ResultType.AREA)
        areas.append(area)
        memory_type_labels.append(cell_type.value)

    fig, ax = plt.subplots(figsize=(4, 2.5))
    x = np.arange(len(memory_type_labels))
    width = 0.5

    ax.bar(x, areas, width, color='royalblue', edgecolor='black', zorder=3)

    ax.set_xlabel('Cell Type')
    ax.set_ylabel('Area (mm^2)')
    ax.set_xticks(x)
    ax.set_xticklabels(memory_type_labels, rotation=45)

    ax.set_yscale('linear')
    ax.grid(True,
            which='both',
            linestyle='--',
            linewidth=0.5,
            alpha=0.7,
            zorder=0)

    plt.tight_layout()
    plt.show()


def plot_life_expectancy_vs_memory_types(model: StorageModel):
    categories = [cell_type.name for cell_type in CellType]
    mins = []
    maxes = []

    for cell_type in CellType:
        if cell_type == CellType.SRAM:
            continue
        model.update_config('cell_type', cell_type.value)
        model.run()
        result = model.get_result(ResultType.LIFE_EXPECTANCY)
        mins.append(result[0])
        maxes.append(result[1])

    fig, ax = plt.subplots()

    ax.set_yscale('log')

    min_value_padding = min(mins) * 0.2
    ax.set_ylim(min_value_padding, max(maxes) * 10)

    minor_locator = LogLocator(base=10.0,
                               subs=np.arange(2, 10) * 0.1,
                               numticks=20)
    ax.yaxis.set_minor_locator(minor_locator)
    ax.grid(which='major',
            axis='y',
            linestyle='-',
            color='black',
            linewidth=0.7,
            zorder=0)
    ax.grid(which='minor',
            axis='y',
            linestyle=':',
            color='gray',
            linewidth=0.5,
            zorder=0)

    for i, (min_val, max_val) in enumerate(zip(mins, maxes)):
        ax.bar(categories[i],
               max_val - min_val,
               bottom=min_val,
               color='limegreen',
               width=0.5,
               edgecolor='black',
               alpha=1.0,
               zorder=3)

    ax.set_xlabel('Cell Type')
    ax.set_ylabel('Life Expectancy (s)')

    plt.show()


def channel_freq_plot_vs_word_size(model: StorageModel,
                                   result_type: ResultType):
    frequencies = np.arange(10000, 100001, 10000)
    channels = np.arange(4, 50, 4)
    samples = 8192

    result_data_16 = np.zeros((len(channels), len(frequencies)))
    result_data_32 = np.zeros((len(channels), len(frequencies)))
    result_data_64 = np.zeros((len(channels), len(frequencies)))

    for i, freq in enumerate(frequencies):
        for j, channel in enumerate(channels):
            input_writes = channel * samples * 32
            fft_writes = channel * 5 * 32
            svm_writes = 2.5
            thr_writes = 0.125

            write_size = input_writes + fft_writes + svm_writes + thr_writes
            read_size = input_writes + fft_writes + svm_writes

            model.config["experiment"]["write_size"] = write_size
            model.config["experiment"]["read_size"] = read_size

            model.update_config('word_width', 16)
            model.run()
            result_data_16[j,
                           i] = (model.get_result(ResultType.TOTAL_ENERGY) /
                                 (8192 / (freq * channel))) + model.get_result(
                                     ResultType.LEAKAGE_POWER)

            model.update_config('word_width', 32)
            model.run()
            result_data_32[j,
                           i] = (model.get_result(ResultType.TOTAL_ENERGY) /
                                 (8192 / (freq * channel))) + model.get_result(
                                     ResultType.LEAKAGE_POWER)

            model.update_config('word_width', 64)
            model.run()
            result_data_64[j,
                           i] = (model.get_result(ResultType.TOTAL_ENERGY) /
                                 (8192 / (freq * channel))) + model.get_result(
                                     ResultType.LEAKAGE_POWER)

    F, C = np.meshgrid(frequencies, channels)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = ['#1f77b4', '#2ca02c', '#ff7f0e']

    ax.plot_surface(F,
                    C,
                    result_data_16,
                    color=colors[0],
                    alpha=0.7,
                    label='word_width=16')
    ax.plot_surface(F,
                    C,
                    result_data_32,
                    color=colors[1],
                    alpha=0.7,
                    label='word_width=32')
    ax.plot_surface(F,
                    C,
                    result_data_64,
                    color=colors[2],
                    alpha=0.7,
                    label='word_width=64')

    ax.set_zscale('log')

    ax.set_xlabel('Sampling Rate (Hz)')
    ax.set_ylabel('Channel Count')
    ax.set_zlabel(result_type.value)

    legend_elements = [
        plt.Line2D([0], [0], color=colors[0], lw=4, label='word_width=16'),
        plt.Line2D([0], [0], color=colors[1], lw=4, label='word_width=32'),
        plt.Line2D([0], [0], color=colors[2], lw=4, label='word_width=64')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize='small')

    plt.show()


def plot_pipeline_stages(model: StorageModel, result_type: ResultType):
    write_sizes = [524288, 320, 3, 1]
    read_sizes = [0, 524288, 320, 3]
    stage_names = ["Input PE", "FFT", "SVM", "THR"]
    results = []

    for write_size, read_size in zip(write_sizes, read_sizes):
        model.update_config('write_size', write_size)
        model.update_config('read_size', read_size)
        model.update_config('total_writes', 1)
        model.update_config('total_reads', 1)
        model.run()
        results.append(model.get_result(result_type))

    fig, ax = plt.subplots(figsize=(4, 2.5))
    x = np.arange(len(stage_names))
    width = 0.5

    ax.bar(x, results, width, color='#f1c40f', edgecolor='black', zorder=3)

    ax.set_xlabel('Pipeline Stage')
    ax.set_ylabel(result_type.value)
    ax.set_xticks(x)
    ax.set_xticklabels(stage_names, rotation=45)

    ax.set_yscale('log')

    ax.grid(True,
            which='major',
            linestyle='-',
            linewidth=0.7,
            alpha=0.8,
            zorder=0)
    ax.grid(True,
            which='minor',
            linestyle='--',
            linewidth=0.5,
            alpha=0.5,
            zorder=0)

    ax.minorticks_on()

    plt.tight_layout()
    plt.show()


def main():
    model = StorageModel(cell_type=CellType.STT,
                         total_reads=1,
                         read_size=524611,
                         total_writes=1,
                         write_size=524612,
                         time_constraint=8192 / (30000 * 16))

    channel_freq_plot(model, ResultType.TOTAL_POWER)
    mem_type_comparison(model, ResultType.TOTAL_POWER)
    plot_power_vs_memory_types(model)
    plot_latency_vs_memory_types(model)
    plot_area_vs_memory_types(model)
    plot_life_expectancy_vs_memory_types(model)
    plot_pipeline_stages(model, ResultType.TOTAL_LATENCY)

    #model.cleanup()

    return


if __name__ == "__main__":
    main()
