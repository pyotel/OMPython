#!/usr/bin/env python3
"""
Basic test to verify the simulation works without GUI.
"""

import sys
import pathlib

# Add parent directory to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from OMPython import ModelicaSystem


def main():
    print("=" * 70)
    print("Testing Newton Cooling Model Simulation")
    print("=" * 70)

    # Define paths
    project_dir = pathlib.Path(__file__).parent.parent.parent
    model_file = project_dir / "mo_example" / "bouncingball.mo"
    model_name = "NewtonCoolingDynamic"

    print(f"\nModel file: {model_file}")
    print(f"Model exists: {model_file.exists()}")
    print(f"Model name: {model_name}")

    try:
        print("\n[1/5] Loading model...")
        mod = ModelicaSystem(
            fileName=str(model_file),
            modelName=model_name,
            build=True
        )
        print("  ✓ Model loaded successfully")

        print("\n[2/5] Checking parameters...")
        params = mod.getParameters()
        print(f"  Found {len(params)} parameters:")
        for name, value in params.items():
            print(f"    {name}: {value}")

        print("\n[3/5] Setting simulation options...")
        mod.setSimulationOptions({
            'stopTime': '1.0',
            'stepSize': '0.01',
            'tolerance': '1e-6'
        })
        print("  ✓ Simulation options set")

        print("\n[4/5] Modifying parameters...")
        mod.setParameters({'h': '1.0', 'm': '0.15'})
        print("  ✓ Parameters modified (h=1.0, m=0.15)")

        print("\n[5/5] Running simulation...")
        mod.simulate()
        print("  ✓ Simulation completed")

        print("\n" + "=" * 70)
        print("Extracting and analyzing results...")
        print("=" * 70)

        # Get results
        time = mod.getSolutions("time")[0]
        temperature = mod.getSolutions("T")[0]
        ambient_temp = mod.getSolutions("T_inf")[0]

        print(f"\nSimulation statistics:")
        print(f"  Time points: {len(time)}")
        print(f"  Simulation duration: {time[0]:.2f}s to {time[-1]:.2f}s")
        print(f"\nTemperature analysis:")
        print(f"  Initial temperature: {temperature[0]:.2f} K ({temperature[0]-273.15:.2f} °C)")
        print(f"  Final temperature: {temperature[-1]:.2f} K ({temperature[-1]-273.15:.2f} °C)")
        print(f"  Temperature drop: {temperature[0] - temperature[-1]:.2f} K")
        print(f"\nAmbient temperature:")
        print(f"  Initial: {ambient_temp[0]:.2f} K ({ambient_temp[0]-273.15:.2f} °C)")
        print(f"  Final: {ambient_temp[-1]:.2f} K ({ambient_temp[-1]-273.15:.2f} °C)")

        # Calculate cooling rate
        cooling_rate = (temperature[0] - temperature[-1]) / (time[-1] - time[0])
        print(f"\nAverage cooling rate: {cooling_rate:.2f} K/s")

        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED!")
        print("=" * 70)

        return 0

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
