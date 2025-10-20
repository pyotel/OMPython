# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OMPython is a Python interface to OpenModelica, providing a Python API for interacting with the OpenModelica Compiler (OMC) via ZeroMQ. The library enables loading, building, simulating, and analyzing Modelica models from Python.

## Core Architecture

### Main Components

**OMCSession (OMPython/OMCSession.py):**
- `OMCSessionZMQ`: Primary class for ZeroMQ-based communication with OMC
- `OMCSessionCmd`: Higher-level command interface wrapping OMCSessionZMQ
- Process management classes for running OMC in different environments:
  - `OMCProcessLocal`: Local OMC process (Linux/Windows)
  - `OMCProcessPort`: Connect to existing OMC server via port
  - `OMCProcessDocker`: OMC running in Docker container
  - `OMCProcessDockerContainer`: OMC in existing Docker container
  - `OMCProcessWSL`: OMC via Windows Subsystem for Linux

**ModelicaSystem (OMPython/ModelicaSystem.py):**
- `ModelicaSystem`: Main user-facing class for working with Modelica models
  - Loads model files or packages
  - Builds models and parses XML metadata
  - Manages parameters, inputs, outputs, continuous variables
  - Handles simulation, optimization, and linearization
- `ModelicaSystemCmd`: Wrapper for compiled model executables
  - Manages command-line arguments for simulation binaries
  - Handles override files and CSV input data
- `LinearizationResult`: Dataclass containing linearization results (A, B, C, D matrices)

**Parsers:**
- `OMParser.py`: Basic parser for OMC responses
- `OMTypedParser.py`: Typed parser using pyparsing for structured OMC output

### Communication Flow

1. User creates `ModelicaSystem` or `OMCSessionZMQ` instance
2. OMC process starts (local, Docker, WSL, or connects to existing)
3. ZeroMQ socket established on dynamically allocated port
4. Commands sent via `sendExpression()` method
5. Results parsed and returned to user

### Key Design Patterns

- Session classes follow factory pattern (different OMCProcess implementations)
- ModelicaSystem uses builder pattern for configuration (setParameters, setSimulationOptions, etc.)
- Error handling via custom exceptions: `OMCSessionException`, `ModelicaSystemError`

## Development Commands

### Installation
```bash
# Install in development mode
python -m pip install -U .

# Install with dev dependencies
pip install . pytest pytest-md pytest-emoji pre-commit
```

### Linting
```bash
# Setup pre-commit hooks (recommended)
pre-commit install

# Run all linters manually
pre-commit run --all-files

# Individual linters
flake8
mypy --exclude tests/
codespell
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_ModelicaSystem.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_ModelicaSystem.py::test_function_name
```

### Requirements

- Python 3.10+
- OpenModelica Compiler (omc) must be installed or accessible
- Dependencies: numpy, psutil, pyparsing, pyzmq
- For testing: pytest, docker (for docker tests)

## Key Implementation Details

### Session Initialization

When creating an OMCSessionZMQ:
1. OMC process spawned with `--interactive=zmq` flag
2. Random string generated for session identification
3. Port file created in temp directory: `openmodelica.{random_string}.objid`
4. Log file: `openmodelica.{random_string}.log`
5. Connection established via ZeroMQ REQ socket

### ModelicaSystem Workflow

Typical usage pattern:
1. Initialize: `ModelicaSystem(fileName, modelName, lmodel, build=True)`
2. Configure: `setParameters()`, `setSimulationOptions()`, `setInputs()`
3. Execute: `simulate()`, `linearize()`, or `optimize()`
4. Extract results: `getSolutions()`, `getContinuous()`, `getOutputs()`

### XML Parsing

After `buildModel()`:
- OMC generates `{modelName}_init.xml` containing model metadata
- Parsed in `_xmlparse()` to extract:
  - Default simulation options (startTime, stopTime, stepSize, tolerance, solver)
  - Variable metadata (parameters, continuous, inputs, outputs)
  - Variable attributes (min, max, unit, changeable, variability, causality)

### Simulation Execution

The compiled model executable accepts runtime flags:
- `-r={resultFile}` - result file path
- `-override={var1=val1,var2=val2}` - override parameters
- `-csvInput={file}` - CSV input data for input signals
- `-l={time}` - linearization time point

### Command Line Options

Set via `setCommandLineOptions()` passed to OMC:
- `--linearizationDumpLanguage=python` - generates Python file with matrices
- `--generateSymbolicLinearization` - enables symbolic linearization

## Testing Notes

- Docker tests require `openmodelica/openmodelica:v1.25.0-minimal` image
- Tests use Modelica Standard Library 4.0.0
- CI runs on Ubuntu and Windows with Python 3.10 and 3.12
- Timezone set to Europe/Berlin for consistent test behavior

## Important Patterns for Modifications

### Adding New OMC API Methods to OMCSessionCmd

Follow pattern in OMCSession.py:273-272:
```python
def apiMethodName(self, className):
    return self._ask(question='apiMethodName', opt=[className])
```

### Adding ModelicaSystem Configuration Methods

Follow pattern for get/set methods:
1. Add internal dict storage (e.g., `self._new_options`)
2. Implement getter returning dict/list based on input type
3. Implement setter using `_prepare_input_data()` and `_set_method_helper()`

### Error Handling

- Raise `ModelicaSystemError` for model-related issues
- Raise `OMCSessionException` for OMC communication issues
- Use logger (logging module) for debug/info/warning messages
- Check OMC error messages via `getMessagesStringInternal()`

## Workshop Examples

The `workshop/` directory contains tutorial examples demonstrating OMPython usage with different Modelica models. Each workshop includes test scripts, visualization tools, parameter studies, and interactive dashboards.

### Directory Structure

```
workshop/
├── cooling/          # Newton Cooling Law example
│   ├── test_basic.py
│   ├── simple_example.py
│   ├── simulate_cooling.py
│   ├── interactive_explorer.py
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── INDEX.md
│   ├── requirements.txt
│   └── .gitignore
│
└── smr/              # Small Modular Reactor example
    ├── test_basic.py
    ├── visualize_smr.py
    ├── parameter_study.py
    ├── interactive_dashboard.py
    ├── README.md
    ├── requirements.txt
    └── .gitignore

mo_example/
├── cooling.mo        # NewtonCoolingDynamic model
└── srm.mo           # SMR_PowerPlant model
```

### Workshop: Cooling (workshop/cooling/)

**Model:** `mo_example/cooling.mo` - NewtonCoolingDynamic

Newton's Law of Cooling simulation demonstrating heat transfer from a hot body to ambient environment.

**Key Parameters:**
- `T0` (K): Initial temperature
- `h` (W/m²·K): Heat transfer coefficient
- `A` (m²): Surface area
- `m` (kg): Mass
- `c_p` (J/kg·K): Specific heat capacity

**Scripts:**
1. `test_basic.py` - Basic test without GUI, verifies model loading and simulation
2. `simple_example.py` - Simple visualization with 2 plots (temperature, cooling rate)
3. `simulate_cooling.py` - Parameter study comparing different heat transfer coefficients
4. `interactive_explorer.py` - Interactive dashboard with real-time parameter adjustment

**Typical Usage:**
```bash
cd workshop/cooling
python3 test_basic.py                # Basic test
python3 simple_example.py            # Simple visualization
python3 simulate_cooling.py          # Parameter study
python3 interactive_explorer.py      # Interactive dashboard
```

### Workshop: SMR (workshop/smr/)

**Model:** `mo_example/srm.mo` - SMR_PowerPlant

Small Modular Reactor power plant simulation with thermal-to-electric conversion.

**Key Parameters:**
- `Q_fission` (W): Nuclear fission heat output (default: 100 MW)
- `eff_thermal`: Thermal-to-electric efficiency (default: 0.35)
- `UA` (W/K): Heat exchanger thermal conductance (default: 50 kW/K)
- `m_coolant` (kg): Coolant mass (default: 500 kg)

**Key Variables:**
- `T_core` (K): Core coolant temperature
- `Q_transfer` (W): Heat transfer rate
- `P_electric` (W): Electric power output

**Model Equations:**
```
dT_core/dt = (Q_fission - Q_transfer) / (m_coolant * Cp)
Q_transfer = UA * (T_core - T_steam)
P_electric = Q_transfer * eff_thermal
```

**Scripts:**
1. `test_basic.py` - Basic SMR simulation test with result verification
2. `visualize_smr.py` - Comprehensive visualizations:
   - 4-panel analysis (temperature, heat transfer, power, efficiency)
   - Energy flow diagram (Sankey-style bar chart)
   - Transient response analysis (derivatives, settling time)
3. `parameter_study.py` - Systematic parameter sweeps:
   - UA: [30, 50, 70, 90 kW/K]
   - eff_thermal: [0.25, 0.30, 0.35, 0.40]
   - m_coolant: [300, 500, 700, 900 kg]
   - Sensitivity analysis comparing all parameters
4. `interactive_dashboard.py` - Real-time interactive control:
   - Adjustable sliders for 4 parameters
   - Live plot updates (temperature, power output)
   - Operating status display

**Typical Usage:**
```bash
cd workshop/smr
python3 test_basic.py                # Basic test (~5s)
python3 visualize_smr.py             # Generate 3 visualizations (~15-20s)
python3 parameter_study.py           # Parameter sweep study (~2-3 min)
python3 interactive_dashboard.py     # Interactive dashboard
```

### Workshop Development Pattern

When creating new workshop examples, follow this pattern:

**1. Python Script Path Setup:**
```python
import sys
import pathlib

# Add OMPython to path (scripts are 3 levels deep: workshop/{name}/*.py)
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from OMPython import ModelicaSystem
```

**2. Model Path Reference:**
```python
project_dir = pathlib.Path(__file__).parent.parent.parent
model_file = project_dir / "mo_example" / "model_name.mo"
```

**3. Basic Simulation Pattern:**
```python
mod = ModelicaSystem(
    fileName=str(model_file),
    modelName="ModelName",
    build=True
)

mod.setSimulationOptions({
    'stopTime': '1000',
    'stepSize': '1.0',
    'tolerance': '1e-6'
})

mod.setParameters({'param1': 'value1', 'param2': 'value2'})
mod.simulate()

# Extract results
time = mod.getSolutions("time")[0]
var1 = mod.getSolutions("var1")[0]
```

**4. Required Files:**
- `test_basic.py` - Basic test without visualization
- Visualization scripts - At least one plot generation script
- `README.md` - Documentation with model description and usage
- `requirements.txt` - Python dependencies (matplotlib, numpy, etc.)
- `.gitignore` - Exclude results/, simulation artifacts, Python cache

**5. .gitignore Pattern:**
```gitignore
# Python cache
__pycache__/
*.pyc

# Simulation results
results/
*.png
*.pdf

# OpenModelica artifacts
*.exe
*.mat
*.log
*.xml
*.c
*.o
```

### Workshop Dependencies

Install workshop dependencies:
```bash
cd workshop/{name}
pip install -r requirements.txt
```

Common requirements:
- `matplotlib>=3.5.0` - Plotting
- `numpy>=1.21.0` - Numerical operations
- `pyzmq>=22.0.0` - OMC communication
- `pyparsing>=3.0.0` - Parsing
- `psutil>=5.8.0` - Process management
