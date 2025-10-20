#!/usr/bin/env python3
"""
Simple example of loading and simulating a Modelica model with OMPython.
"""

import sys
import pathlib
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from OMPython import ModelicaSystem


def main():
    # Define paths
    project_dir = pathlib.Path(__file__).parent.parent.parent
    model_file = project_dir / "mo_example" / "bouncingball.mo"
    model_name = "NewtonCoolingDynamic"

    print("Loading Modelica model...")
    print(f"  File: {model_file}")
    print(f"  Model: {model_name}")

    # Create and build the model
    mod = ModelicaSystem(
        fileName=str(model_file),
        modelName=model_name,
        build=True
    )

    print("\nModel loaded successfully!")

    # Check available parameters
    print("\n=== Available Parameters ===")
    params = mod.getParameters()
    for name, value in params.items():
        print(f"  {name}: {value}")

    # Set simulation options
    print("\n=== Setting Simulation Options ===")
    mod.setSimulationOptions({
        'stopTime': '2.0',
        'stepSize': '0.01',
        'tolerance': '1e-6'
    })

    # Modify a parameter
    print("\n=== Modifying Parameters ===")
    print("  Setting h (cooling coefficient) = 1.0")
    mod.setParameters({'h': '1.0'})

    # Run simulation
    print("\n=== Running Simulation ===")
    mod.simulate()
    print("  ✓ Simulation complete!")

    # Get results
    print("\n=== Extracting Results ===")
    time = mod.getSolutions("time")[0]
    temperature = mod.getSolutions("T")[0]
    ambient_temp = mod.getSolutions("T_inf")[0]

    print(f"  Time points: {len(time)}")
    print(f"  Initial temperature: {temperature[0]:.2f} K")
    print(f"  Final temperature: {temperature[-1]:.2f} K")

    # Plot results
    print("\n=== Creating Plot ===")
    plt.figure(figsize=(10, 6))

    plt.plot(time, temperature, 'b-', linewidth=2, label='Object Temperature (T)')
    plt.plot(time, ambient_temp, 'r--', linewidth=2, label='Ambient Temperature (T_inf)')

    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Temperature (K)', fontsize=12)
    plt.title('Newton Cooling Model - Temperature vs Time', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)

    # Save plot
    output_file = pathlib.Path(__file__).parent / "results" / "simple_example.png"
    output_file.parent.mkdir(exist_ok=True)
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Plot saved: {output_file}")

    plt.show()

    print("\n=== Done! ===")


if __name__ == "__main__":
    main()
