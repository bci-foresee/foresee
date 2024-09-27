import os
import matplotlib.pyplot as plt
import pandas as pd
import sys


#TODO(Bernardo): The functions below can be simplified further.
#TODO(Bernardo): Finish the num_runs functionality.
def plot_visualizations(filename,
                        accuracy=False,
                        time=False,
                        power=False,
                        num_runs=1,
                        compare_to_filename=None,
                        custom=None):
    """Plots the data for the given pipeline or PE file.

  Args:
    filename: The name of the CSV file containing data on the pipeline or PE.
    accuracy: Optional flag to create a plot based on accuracy.
    time: Optional flag to create a plot based on time.
    power: Optional flag to create a plot based on power.
    num_runs: Optional flag to specify the number of runs to plot.
    compare_to_filename: Optional flag to specify the PE or pipeline we are comparing against.
    custom: Optional flag to specify a custom function to plot the data.
  """

    # Read the CSV file(s) into a pandas DataFrame
    df = pd.read_csv(filename)
    df_comp = None
    if (compare_to_filename):
        df_comp = pd.read_csv(compare_to_filename)

    # TODO(Bernardo): Separate the functions below into their own files.
    if accuracy:
        plot_accuracy_visualization(df, df_comp, num_runs)
    if time:
        plot_time_visualization(df, df_comp, num_runs)
    if power:
        plot_power_visualization(df, df_comp, num_runs)
    if custom:
        plot_custom_visualization(df, df_comp, custom)


def plot_accuracy_visualization(df, df_comp, num_runs):
    """Plots accuracy.

  Args:
    df: pandas DataFrame containing the data.
    df_comp: pandas DataFrame containing the data we are comparing against.
    num_runs: the number of runs to plot.
  """
    # TODO(Bernardo): Fix once we have CSV.
    # Assuming the first column is n_run and the second column is the accuracy value
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]

    plt.clf()

    # Create the plot
    plt.plot(x, y)
    if (df_comp != None and not df_comp.empty):
        x_comp = df_comp.iloc[:, 0]
        y_comp = df_comp.iloc[:, 1]
        plt.plot(x_comp, y_comp, label='Comparison')
    plt.xlabel('Run')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Plot')

    output_dir = 'visualize/output_plots'
    filename = 'accuracy_plot.png'

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the plot to the specified location
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)


def plot_time_visualization(df, df_comp, num_runs):
    """Plots time.

  Args:
    df: pandas DataFrame containing the data.
    df_comp: pandas DataFrame containing the data we are comparing against.
    num_runs: the number of runs to plot.
  """
    # TODO(Bernardo): Fix once we have CSV.
    # Assuming the first column is n_run and the third column is the time value
    x = df.iloc[:, 0]
    y = df.iloc[:, 2]

    plt.clf()

    # Create the plot
    plt.plot(x, y)
    if (df_comp != None and not df_comp.empty):
        x_comp = df_comp.iloc[:, 0]
        y_comp = df_comp.iloc[:, 2]
        plt.plot(x_comp, y_comp, label='Comparison')
    plt.xlabel('Run')
    plt.ylabel('Time')
    plt.title('Time Plot')

    output_dir = 'visualize/output_plots'
    filename = 'time_plot.png'

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the plot to the specified location
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)


def plot_power_visualization(df, df_comp, num_runs):
    """Plots power.

  Args:
    df: pandas DataFrame containing the data.
    df_comp: pandas DataFrame containing the data we are comparing against.
    num_runs: the number of runs to plot.
  """
    # TODO(Bernardo): Fix once we have CSV.
    # Assuming the first column is n_run and the fourth column is the power value
    x = df.iloc[:, 0]
    y = df.iloc[:, 3]

    plt.clf()

    # Create the plot
    plt.plot(x, y)
    if (df_comp != None and not df_comp.empty):
        x_comp = df_comp.iloc[:, 0]
        y_comp = df_comp.iloc[:, 3]
        plt.plot(x_comp, y_comp, label='Comparison')
    plt.xlabel('Run')
    plt.ylabel('Power')
    plt.title('Power Plot')
    output_dir = 'visualize/output_plots'
    filename = 'power_plot.png'

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the plot to the specified location
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)


def plot_custom_visualization(df, df_comp, custom):
    """Plots a custom visualization.

  Args:
    df: pandas DataFrame containing the data.
    df_comp: pandas DataFrame containing the data we are comparing against.
    custom: custom function to plot the data.
  """

    # Import the user-defined function dynamically
    try:
        module = __import__(custom)
        plot_function = getattr(module, custom)
    except ImportError:
        print(f"Error: Could not import function '{custom}'.")
        return

    plt.clf()

    # Use the imported function to plot the data
    plot_function(df, df_comp)

    output_dir = 'visualize/output_plots'
    filename = 'custom_plot.png'

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the plot to the specified location
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(
            "Usage: python visualize.py <filename.csv> [--accuracy] [--time] [--power] [--num_runs=n] [--compare_to=filename] [--custom=function_name]"
        )
        sys.exit(1)

    filename = sys.argv[1]
    accuracy = None
    time = None
    power = None
    num_runs = None
    compare_to_filename = None
    custom = None

    # Parse command-line arguments
    for arg in sys.argv[2:]:
        if arg.startswith('--accuracy'):
            accuracy = True
        elif arg.startswith('--time'):
            time = True
        elif arg.startswith('--power'):
            power = True
        elif arg.startswith('--num_runs='):
            num_runs = int(arg.split('=')[1])
        elif arg.startswith('--compare_to='):
            compare_to_filename = str(arg.split('=')[1])
        elif arg.startswith('--custom='):
            custom = str(arg.split('=')[1])

    plot_visualizations(filename,
                        accuracy=accuracy,
                        time=time,
                        power=power,
                        num_runs=num_runs,
                        compare_to_filename=compare_to_filename,
                        custom=custom)
