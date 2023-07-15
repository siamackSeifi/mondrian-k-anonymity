import matplotlib.pyplot as plt
import pandas as pd

import config


def plot(durations, avg, mode):
    x_axis = list(durations.keys())  # Extract keys from durations

    # Create separate bar chart for durations
    fig1, ax1 = plt.subplots()
    ax1.bar(x_axis, list(durations.values()), color='blue', label='durations')
    ax1.set_ylabel('durations (seconds)')
    ax1.set_xlabel('k')
    ax1.set_ylim([0, max(durations.values()) + 5])  # Adjust the y-axis limits
    ax1.legend(loc='upper left')
    plt.title(f'Execution time against K - \'{mode}\' mode')
    plt.savefig(f'{config.outputBaseUrl}{config.inputFile}_durations - {mode}.png')

    # Create separate line chart for avg
    fig2, ax2 = plt.subplots()
    ax2.plot(x_axis, list(avg.values()), color='red', marker='o', label='C-avg')
    ax2.set_ylabel('C-avg')
    ax2.set_xlabel('k')
    ax2.set_ylim([0, max(avg.values()) + 1])  # Adjust the y-axis limits
    # Show AVG values as text on the line chart
    for key, value in avg.items():
        ax2.text(key, value, str(value), ha='center', va='bottom')
    ax2.legend(loc='upper right')
    plt.title(f'C-avg metric against K - \'{mode}\' mode')
    plt.savefig(f'{config.outputBaseUrl}{config.inputFile}_C-avg - {mode}.png')

    # Create a combined plot
    fig3, ax3 = plt.subplots()
    ax3.bar(x_axis, list(durations.values()), color='blue', label='durations')
    ax3.set_ylabel('durations (seconds)')
    ax3.set_xlabel('k')
    ax3.set_ylim([0, max(durations.values()) + 5])  # Adjust the y-axis limits
    ax3.legend(loc='upper left')

    ax4 = ax3.twinx()
    ax4.plot(x_axis, list(avg.values()), color='red', marker='o', label='C-avg')
    ax4.set_ylabel('C-avg')
    ax4.set_ylim([0, max(avg.values()) + 1])  # Adjust the y-axis limits
    # Show AVG values as text on the line chart
    for key, value in avg.items():
        ax4.text(key, value, str(value), ha='center', va='bottom')
    ax4.legend(loc='upper right')
    plt.title(f'Execution time and C-avg metric against K - \'{mode}\' mode')
    plt.savefig(f'{config.outputBaseUrl}{config.inputFile}_combined_plot - {mode}.png')

    # Display the separate plots
    plt.show()


def quantize_categorical_columns(data):
    for column in config.qi:
        # check for each column whether its data is numerical
        # ignore numerical values
        if pd.to_numeric(data[column], errors='coerce').isna().any():
            unique_strings = data[column].unique()
            if config.userDefinedCatAvailable:
                # quantizes data based on user-defined generalization hierarchies for categorical attributes
                mapping = {}
                for idx, value in enumerate(unique_strings):
                    if column in config.userDefinedCat and value in config.userDefinedCat[column].values():
                        reverse_mapping = {value: idx for idx, value in config.userDefinedCat[column].items()}
                        mapping[value] = reverse_mapping[value]
                    else:
                        raise Exception(f"You did not provide quantized values for '{column}' completely!"
                                        f"\n***missing value: '{value}'***"
                                        f"\nin config.userDefinedCat")
            else:  # just quantiles the non-numeric values, so it would tarnish data semantics.
                mapping = {value: idx for idx, value in enumerate(unique_strings)}

            if config.debug:
                # Print the mapping
                print(f"Mapping for column '{column}':")
                for string, number in mapping.items():
                    print(f"'{string}' -> {number}")

            data[column] = data[column].map(mapping).astype(int)

    return data


def calc_C_AVG(data, k_factor):
    grouped = data.groupby(config.qi)

    if config.debug:
        for _, group in grouped:
            if group.size < k_factor:
                print('The following equivalent class is smaller than K')
                print(group)
                print()

    return round((len(data)/grouped.ngroups)/k_factor, 3)
