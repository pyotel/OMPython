#!/bin/bash
# Setup script for OMPython workshop

echo "=========================================="
echo "OMPython Workshop Setup"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "../pyproject.toml" ]; then
    echo "Error: Please run this script from the workshop directory"
    exit 1
fi

echo "[1/3] Installing OMPython..."
cd ..
python3 -m pip install -e .
cd workshop

echo ""
echo "[2/3] Installing additional requirements..."
pip install -r requirements.txt

echo ""
echo "[3/3] Verifying installation..."
python3 -c "from OMPython import ModelicaSystem; print('✓ OMPython imported successfully')"
python3 -c "import matplotlib; print('✓ matplotlib imported successfully')"
python3 -c "import numpy; print('✓ numpy imported successfully')"

echo ""
echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""
echo "You can now run the examples:"
echo "  python test_basic.py           # Basic test"
echo "  python simple_example.py       # Simple example with plot"
echo "  python simulate_cooling.py     # Parameter study"
echo "  python interactive_explorer.py # Interactive explorer"
echo ""
