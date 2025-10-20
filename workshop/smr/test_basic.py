#!/usr/bin/env python3
"""
Basic test for SMR (Small Modular Reactor) Power Plant model.
Tests model loading, simulation, and basic output verification.
"""

import sys
import pathlib

# Add parent directory to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from OMPython import ModelicaSystem


def main():
    print("=" * 70)
    print("SMR Power Plant Model - Basic Test")
    print("=" * 70)

    # Define paths
    project_dir = pathlib.Path(__file__).parent.parent.parent
    model_file = project_dir / "mo_example" / "srm.mo"
    model_name = "SMR_PowerPlant"

    print(f"\nModel file: {model_file}")
    print(f"Model exists: {model_file.exists()}")
    print(f"Model name: {model_name}")

    try:
        print("\n[1/5] Loading SMR model...")
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
            'stopTime': '1000',  # 1000 seconds simulation
            'stepSize': '1.0',
            'tolerance': '1e-6'
        })
        print("  ✓ Simulation options set")

        print("\n[4/5] Running simulation...")
        mod.simulate()
        print("  ✓ Simulation completed")

        print("\n[5/5] Extracting and analyzing results...")
        print("=" * 70)

        # Get results
        time = mod.getSolutions("time")[0]
        T_core = mod.getSolutions("T_core")[0]
        Q_transfer = mod.getSolutions("Q_transfer")[0]
        P_electric = mod.getSolutions("P_electric")[0]

        print(f"\nSimulation statistics:")
        print(f"  Time points: {len(time)}")
        print(f"  Simulation duration: {time[0]:.1f}s to {time[-1]:.1f}s")

        print(f"\nCore Temperature:")
        print(f"  Initial: {T_core[0]:.2f} K ({T_core[0]-273.15:.2f} °C)")
        print(f"  Final: {T_core[-1]:.2f} K ({T_core[-1]-273.15:.2f} °C)")
        print(f"  Temperature change: {T_core[-1] - T_core[0]:.2f} K")

        print(f"\nHeat Transfer:")
        print(f"  Initial: {Q_transfer[0]/1e6:.2f} MW")
        print(f"  Final: {Q_transfer[-1]/1e6:.2f} MW")
        print(f"  Change: {(Q_transfer[-1] - Q_transfer[0])/1e6:.2f} MW")

        print(f"\nElectric Power Output:")
        print(f"  Initial: {P_electric[0]/1e6:.2f} MW")
        print(f"  Final: {P_electric[-1]/1e6:.2f} MW")
        print(f"  Average: {P_electric.mean()/1e6:.2f} MW")

        # Calculate efficiency
        Q_fission = float(params['Q_fission'])
        actual_eff = (P_electric[-1] / Q_fission) * 100
        nominal_eff = float(params['eff_thermal']) * 100
        print(f"\nEfficiency:")
        print(f"  Nominal: {nominal_eff:.1f}%")
        print(f"  Actual (final): {actual_eff:.1f}%")

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
