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
