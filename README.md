# Foresee: BCI Pipeline Design & Analysis Tool

### Tool Status

![PE Python Tests](https://github.com/ysarch-lab/aloha-verilog/actions/workflows/PE-python-suite.yml/badge.svg)

![PE Verilog Tests](https://github.com/ysarch-lab/aloha-verilog/actions/workflows/PE-verilog-suite.yml/badge.svg)

<!-- ![PE RTL Power Tests](https://github.com/ysarch-lab/aloha-verilog/actions/workflows/PE-rtl-power-suite.yml/badge.svg) -->

![Pipeline Tests](https://github.com/ysarch-lab/aloha-verilog/actions/workflows/pipeline-suite.yml/badge.svg)

Readme last updated: 24 April 2025 

## Overview

Foresee is a comprehensive Brain-Computer Interface (BCI) pipelFORESEE: BCI Pipeline Design & Analysis Toooine design and analysis tool. It enables researchers and engineers to design, test, and implement BCI pipelines through an intuitive graphical interface. The tool is built on a growing library of modules that can be easily integrated into a pipeline for rapid prototyping and testing.

Key features include:
- Graphical pipeline editor
- Performance analysis and visualization
- Hardware simulation capabilities
- Integration of RTL with high-level simulation


## Installation

Go to the releases tab and download the executable for your platform. If you are on macOS, make sure you download the x86 or ARM variation, depending on what CPU your computer has

## Project Structure

The project is organized into two main components:
- `app/` - Contains the Electron frontend
- `backend/` - Contains the Python backend including modules, pipeline execution, and analysis tools

## Developer Installation

### Linux

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-organization/foresee.git
   cd foresee
   ```

2. **Set up the conda environment**
   
   First, make sure you have conda installed. If not, you can install either Anaconda (full distribution with many packages) or Miniconda (minimal distribution) from https://www.anaconda.com/download/.
   
   ```bash
   # Create and activate the conda environment
   conda env create -f environment.yaml
   conda activate foresee
   ```

3. **Install Node.js and npm**
   
   ```bash
   sudo apt update
   sudo apt install nodejs npm
   ```

4. **Install Electron app dependencies**
   
   ```bash
   cd app
   npm install
   ```

5. **Install backend dependencies**
   
   ```bash
   cd ../backend
   pip install flask flask-cors
   ```

### Apple Silicon macOS

*Detailed installation instructions for Apple Silicon macOS will be added soon. The basic approach will be similar to Linux but with macOS-specific package management.*

## Running FORESEE

FORESEE requires both the Python backend and Electron frontend to be running simultaneously.

### 1. Start the Python Backend

```bash
# Navigate to the backend directory
cd backend

# Start the Flask server
python app.py
```

The backend will start and listen on http://127.0.0.1:5000.

### 2. Start the Electron Frontend

Open a new terminal window:

```bash
# Navigate to the app directory
cd app

# Run the development server
npm run dev
```

This will start both the Next.js server and the Electron application.

For production use:

```bash
# Build and start the application
npm run start
```

Note: The `npm run dev` and `npm run start` commands only launch the frontend components - they do not automatically start the Python backend.

## Using FORESEE

Once both the backend and frontend are running, you can access the FORESEE application through the Electron window that opens automatically.

The main interface allows you to:
1. Create new pipelines
2. Import existing pipeline configurations
3. Add modules to your pipeline
4. Connect modules to form a complete pipeline
5. Configure modules parameters
6. Run simulations
7. Analyze performance metrics

## Backend Architecture

The backend is divided into multiple components, each with a specific purpose:

**backend/asa/**: This is the accelerator set architecture (ASA) directory. This directory contains all of the modules that are used in pipelines.

**backend/pipelines/**: This directory contains all of the pipelines that are used in the simulator. These pipelines are built using the modules in the ASA directory.

**backend/signals/**: This directory contains the management of input signals for the simulator. This includes generating test signals and importing iEEG signals measured in real life.

### ASA (Accelerator Set Architecture)

ASA stands for accelerator set architecture. This directory contains all of the modules that are used in pipelines created by the simulator. For example, let's say you wanted to create a pipeline for detecting seizures from iEEG data. One method (inspired by [Shiao et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5359075/)) is to use the pipeline depicted in the logo image above.

To create such a pipeline, we would first implement all of the individual modules such as the FFT, SVM, etc. In `backend/asa/processing_element.py` you can find the parent class which every module inherits from. This class defines all the necessary methods and attributes a module must contain.

Within the directory, there are subdirectories for each module (e.g., `backend/asa/fft/`). Each directory contains the necessary files to implement the module, including the Python implementation, the RTL implementation (when available), and tests.

### Module Structure

When creating a new module, you need to:

1. **Create a Class**: Define a class that inherits from ProcessingElement, with appropriate typed parameters:

```python
class FFT(ProcessingElement):
    """
    Performs the Discrete Fourier Transform (DFT) using the Fast Fourier 
    Transform (FFT) algorithm.
    """
    name = "FFT"
    
    def __init__(self, berger_bands, n_samples, fs, clk=0, save_visualization=False):
        super().__init__(name=self.name, clk=clk, save_visualization=save_visualization)
        
        self.points = n_samples
        self.sample_freq = fs
        self.berger_bands = berger_bands
```

2. **Implement Required Methods**:
   - `run()`: Main orchestration method
   - `load_inputs()`: Loads input data from connected modules
   - `dimension_validate()`: Validates input dimensions
   - `compute()`: Performs the actual computation
   - `visualize()`: Generates visualizations (if needed)

### Testing Modules

After creating a module, you should test it:

```bash
cd backend/asa/your_pe
pytest -v -rP # The `-v` flag is for verbose output and the `-rP` flag is for showing debug statements.
```

Tests can be simple:

```python
from asa import FFT
from asa.utils import generate_signal
    
def test_fft() -> None:
    # Generate an input signal
    input_signal = generate_signal(frequencies=[10, 20, 40],
                                 amplitudes=[20, 15, 10],
                                 fs=400,
                                 n_channels=2,
                                 n_samples=8000)
    
    # Create the PE you want to test
    fft_pe = FFT(n_samples=8000,
               fs=400,
               berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)],
               clk=1,
               save_visualization=True)
    
    # Run the pipeline
    output = fft_pe.compute(input=input_signal)
    
    # Add assertions to validate the output
    assert output.shape == (2, 6)  # Example assertion
```

The backend includes utility functions to help with testing, such as `create_testing_pipeline()` in `backend/asa/utils.py`.

## Development

For developers looking to extend FORESEE, please refer to the following resources:

- `app/README.md` - Information about the Electron frontend
- `backend/README.md` - Information about the Python backend
- `setup.md` - Additional setup instructions

## Troubleshooting

**The application doesn't start:**
- Make sure both the backend and frontend are running
- Check if port 5000 is available for the backend server
- Verify that all dependencies are installed correctly

**Processing elements fail to run:**
- Ensure the conda environment is activated (`conda activate foresee`)
- Check that the processing element has valid connections and parameters

## Contributing

We welcome contributions to FORESEE! There are several ways you can contribute:

### Contributing Modules

Modules are the building blocks of BCI pipelines. To contribute a new PE:

1. Follow the structure outlined in the Processing Element Structure section
2. Implement all required methods (`run()`, `load_inputs()`, `dimension_validate()`, etc.)
3. Include comprehensive tests for your PE
4. Document your PE with clear descriptions of its parameters and functionality
5. Submit a pull request with your implementation

### Contributing Pipelines

Pipelines that replicate existing research papers are particularly valuable. To contribute a pipeline:

1. Create a new directory in the `backend/pipelines/` folder named after the paper or technique
2. Implement the pipeline using existing processing elements (or contribute new ones as needed)
3. Include a README.md within your pipeline directory that:
   - Cites the original paper
   - Explains the pipeline architecture
   - Describes any modifications from the original paper
   - Provides example usage
4. Add tests that verify the pipeline functions correctly
5. Submit a pull request with your implementation

## License

?