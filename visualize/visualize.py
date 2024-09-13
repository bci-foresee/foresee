import pydoc
import matplotlib.pyplot as plt
import pandas as pd
import sys

#TODO(Bernardo): The functions below can be simplified further. 
#TODO(Bernardo): Finish the num_runs functionality.
def plot_visualizations(filename, accuracy=False, time=False, power=False, num_runs=1, compare_to_filename=None):
  """Plots the data for the given pipeline or PE file.

  Args:
    filename: The name of the CSV file containing data on the pipeline or PE.
    accuracy: Optional flag to create a plot based on accuracy.
    time: Optional flag to create a plot based on time.
    power: Optional flag to create a plot based on power.
    num_runs: Optional flag to specify the number of runs to plot.
    compare_to_filename=Optional flag to specify the PE or pipeline we are comparing against.
  """

  # Read the CSV file(s) into a pandas DataFrame
  df = pd.read_csv(filename)
  df_comp = None
  if (compare_to_filename):
    df_comp = pd.read_csv(compare_to_filename)

  # TODO(Bernardo): Separate the functions below into their own files.
  if accuracy:
    plot_accuracy_visualization(df, df_comp, num_runs)
  elif time:
    plot_time_visualization(df, df_comp, num_runs)
  elif power:
    plot_power_visualization(df, df_comp, num_runs)

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

  # Create the plot
  plt.plot(x, y)
  if (df_comp):
    x_comp = df_comp.iloc[:, 0]
    y_comp = df_comp.iloc[:, 1]
    plt.plot(x_comp, y_comp, label='Comparison')
  plt.xlabel('Run')
  plt.ylabel('Accuracy')
  plt.title('Accuracy Plot')
  plt.show()

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

  # Create the plot
  plt.plot(x, y)
  if (df_comp):
    x_comp = df_comp.iloc[:, 0]
    y_comp = df_comp.iloc[:, 2]
    plt.plot(x_comp, y_comp, label='Comparison')
  plt.xlabel('Run')
  plt.ylabel('Time')
  plt.title('Time Plot')
  plt.show()

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

  # Create the plot
  plt.plot(x, y)
  if (df_comp):
    x_comp = df_comp.iloc[:, 0]
    y_comp = df_comp.iloc[:, 3]
    plt.plot(x_comp, y_comp, label='Comparison')
  plt.xlabel('Run')
  plt.ylabel('Power')
  plt.title('Power Plot')
  plt.show()

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: python visualize.py <filename.csv> [--accuracy] [--time] [--power] [--num_runs=n] [--compare_to=filename]")
    sys.exit(1)

  filename = sys.argv[1]
  accuracy = None
  time = None
  power = None
  num_runs = None
  compare_to_filename = None

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
      compare_to_filename = int(arg.split('=')[1])

  plot_visualizations(filename, accuracy=accuracy, time=time, power=power, num_runs=num_runs, compare_to_filename=compare_to_filename)

  pydoc.writedoc('visualize')