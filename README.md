# OMPython - Pyotel

OMPython is a Python interface that uses ZeroMQ to
communicate with OpenModelica.

[![FMITest](https://github.com/OpenModelica/OMPython/actions/workflows/FMITest.yml/badge.svg)](https://github.com/OpenModelica/OMPython/actions/workflows/FMITest.yml)
[![Test](https://github.com/OpenModelica/OMPython/actions/workflows/Test.yml/badge.svg)](https://github.com/OpenModelica/OMPython/actions/workflows/Test.yml)

## Moelica 예제
http://modelica.co.kr/board/describing-behavior/basic-equations/basic-equations_examples/an-electrical-example/


## Dependencies

-   Python 3.x supported
-   PyZMQ is required

## Installation

Installation using `pip` is recommended.

### Via pip

```bash
pip install OMPython
```

### Via source

Clone the repository and run:

```
cd <OMPythonPath>
python -m pip install -U .
```

## Usage

Running the following commands should get you started

```python
import OMPython
help(OMPython)
```

```python
from OMPython import OMCSessionZMQ
omc = OMCSessionZMQ()
omc.sendExpression("getVersion()")
```

or read the [OMPython documentation](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/ompython.html)
online.

## Workshop Examples

The `workshop/` directory contains comprehensive tutorial examples demonstrating OMPython usage:

### Newton Cooling Law (workshop/cooling/)

Demonstrates heat transfer simulation using Newton's Law of Cooling.

**Scripts:**
- `test_basic.py` - Basic test and verification
- `simple_example.py` - Simple visualization
- `simulate_cooling.py` - Parameter study
- `interactive_explorer.py` - Interactive dashboard

**Quick Start:**
```bash
cd workshop/cooling
pip install -r requirements.txt
python3 test_basic.py
```

See [workshop/cooling/README.md](workshop/cooling/README.md) for details.

### Small Modular Reactor (workshop/smr/)

SMR (Small Modular Reactor) power plant simulation with thermal-to-electric conversion.

**Scripts:**
- `test_basic.py` - Basic SMR simulation test
- `visualize_smr.py` - Comprehensive visualizations (4-panel analysis, energy flow, transient response)
- `parameter_study.py` - Parameter sweeps and sensitivity analysis
- `interactive_dashboard.py` - Real-time interactive control

**Quick Start:**
```bash
cd workshop/smr
pip install -r requirements.txt
python3 test_basic.py
python3 visualize_smr.py  # Generates 3 visualization plots
```

See [workshop/smr/README.md](workshop/smr/README.md) for details.

**Model Equations:**
```
dT_core/dt = (Q_fission - Q_transfer) / (m_coolant * Cp)
Q_transfer = UA * (T_core - T_steam)
P_electric = Q_transfer * eff_thermal
```

## Bug Reports

  - Submit bugs through the [OpenModelica GitHub issues](https://github.com/OpenModelica/OMPython/issues/new).
  - [Pull requests](https://github.com/OpenModelica/OMPython/pulls) are welcome.


## Development
It is recommended to set up [`pre-commit`](https://pre-commit.com/) to
automatically run linters:
```sh
# cd to the root of the repository
pre-commit install
```

## Contact

  - Adeel Asghar, <adeel.asghar@liu.se>
  - Arunkumar Palanisamy, <arunkumar.palanisamy@liu.se>
