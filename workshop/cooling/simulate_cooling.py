#!/usr/bin/env python3
"""
Newton Cooling Dynamic Model Simulation
Loads the NewtonCoolingDynamic model, varies parameters, and plots results.
"""

import sys
import pathlib
import matplotlib.pyplot as plt
import numpy as np

# Add parent directory to path to import OMPython
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from OMPython import ModelicaSystem


def simulate_with_parameters(model_file, model_name, param_variations, sim_time=1.0):
    """
    Simulate the model with different parameter values.

    Args:
        model_file: Path to the .mo file
        model_name: Name of the model class
        param_variations: Dict of parameter variations {param_name: [values]}
        sim_time: Simulation stop time

    Returns:
        Dict with simulation results for each variation
    """
    results = {}

    for param_name, param_values in param_variations.items():
        print(f"\n=== Varying parameter: {param_name} ===")
        results[param_name] = []

        for value in param_values:
            print(f"  Simulating with {param_name}={value}...")

            # Create ModelicaSystem instance
            mod = ModelicaSystem(
                fileName=model_file,
                modelName=model_name,
                build=True
            )

            # Set simulation options
            mod.setSimulationOptions({
                'stopTime': str(sim_time),
                'stepSize': '0.002',
                'tolerance': '1e-6'
            })

            # Set parameter value
            mod.setParameters({param_name: str(value)})

            # Run simulation
            mod.simulate()

            # Get results
            time = mod.getSolutions("time")[0]
            temperature = mod.getSolutions("T")[0]
            ambient_temp = mod.getSolutions("T_inf")[0]

            results[param_name].append({
                'value': value,
                'time': time,
                'T': temperature,
                'T_inf': ambient_temp
            })

            print(f"    ✓ Simulation complete. Final temp: {temperature[-1]:.2f} K")

    return results


def plot_results(results, output_dir):
    """
    Create plots for all parameter variations.

    Args:
        results: Results from simulate_with_parameters()
        output_dir: Directory to save plots
    """
    output_dir = pathlib.Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    for param_name, param_results in results.items():
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        fig.suptitle(f'Newton Cooling - Varying {param_name}', fontsize=14, fontweight='bold')

        # Plot temperature over time
        for result in param_results:
            label = f"{param_name}={result['value']}"
            ax1.plot(result['time'], result['T'], label=label, linewidth=2)

        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Temperature (K)')
        ax1.set_title('Object Temperature vs Time')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Plot temperature difference over time
        for result in param_results:
            temp_diff = result['T'] - result['T_inf']
            label = f"{param_name}={result['value']}"
            ax2.plot(result['time'], temp_diff, label=label, linewidth=2)

        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Temperature Difference (K)')
        ax2.set_title('Temperature Difference (T - T_inf) vs Time')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        plt.tight_layout()

        # Save plot
        output_file = output_dir / f"cooling_{param_name}.png"
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ Plot saved: {output_file}")

        # Also show the plot
        plt.show()
        plt.close()


def plot_comparison(results, output_dir):
    """
    Create a comparison plot showing final temperatures for different parameters.

    Args:
        results: Results from simulate_with_parameters()
        output_dir: Directory to save plots
    """
    output_dir = pathlib.Path(output_dir)

    fig, ax = plt.subplots(figsize=(12, 6))

    x_offset = 0
    colors = plt.cm.Set3(np.linspace(0, 1, len(results)))

    for (param_name, param_results), color in zip(results.items(), colors):
        param_values = [r['value'] for r in param_results]
        final_temps = [r['T'][-1] for r in param_results]

        positions = np.arange(len(param_values)) + x_offset
        ax.bar(positions, final_temps, width=0.8, label=param_name,
               color=color, alpha=0.7, edgecolor='black')

        # Add value labels on bars
        for pos, temp, val in zip(positions, final_temps, param_values):
            ax.text(pos, temp + 1, f'{temp:.1f}K\n({param_name}={val})',
                   ha='center', va='bottom', fontsize=8)

        x_offset += len(param_values) + 1

    ax.set_ylabel('Final Temperature (K)')
    ax.set_title('Final Temperature Comparison for Different Parameters')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_xticks([])

    plt.tight_layout()

    output_file = output_dir / "cooling_comparison.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Comparison plot saved: {output_file}")
    plt.show()
    plt.close()


def main():
    """Main execution function."""

    # Define paths
    script_dir = pathlib.Path(__file__).parent
    project_dir = script_dir.parent.parent
    model_file = project_dir / "mo_example" / "cooling.mo"
    model_name = "NewtonCoolingDynamic"

    print("=" * 70)
    print("Newton Cooling Dynamic Model - Parameter Study")
    print("=" * 70)
    print(f"Model file: {model_file}")
    print(f"Model name: {model_name}")

    # Define parameter variations to study
    param_variations = {
        'h': [0.5, 0.7, 1.0, 1.5],  # Convective cooling coefficient
        'm': [0.05, 0.1, 0.2, 0.3],  # Mass
        'A': [0.5, 1.0, 1.5, 2.0],   # Surface area
    }

    print("\nParameter variations:")
    for param, values in param_variations.items():
        print(f"  {param}: {values}")

    # Run simulations
    print("\n" + "=" * 70)
    print("Starting simulations...")
    print("=" * 70)

    try:
        results = simulate_with_parameters(
            model_file=str(model_file),
            model_name=model_name,
            param_variations=param_variations,
            sim_time=1.5
        )

        print("\n" + "=" * 70)
        print("Generating plots...")
        print("=" * 70)

        # Create plots
        plot_results(results, script_dir / "results")
        plot_comparison(results, script_dir / "results")

        print("\n" + "=" * 70)
        print("✓ All simulations and plots completed successfully!")
        print("=" * 70)

    except Exception as e:
        print(f"\n✗ Error during simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
