#!/usr/bin/env python3
"""
Parameter study for SMR Power Plant model.
Analyzes the effect of different parameters on reactor performance.
"""

import sys
import pathlib
import matplotlib.pyplot as plt
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from OMPython import ModelicaSystem


def run_parameter_sweep(model_file, model_name, param_name, param_values, sim_time=1000):
    """
    Run simulations with different parameter values.

    Returns:
        List of results dictionaries
    """
    results_list = []

    for value in param_values:
        print(f"  Simulating with {param_name}={value}...")

        mod = ModelicaSystem(
            fileName=str(model_file),
            modelName=model_name,
            build=True
        )

        mod.setSimulationOptions({
            'stopTime': str(sim_time),
            'stepSize': '1.0'
        })

        mod.setParameters({param_name: str(value)})
        mod.simulate()

        results = {
            'param_value': value,
            'time': mod.getSolutions("time")[0],
            'T_core': mod.getSolutions("T_core")[0],
            'Q_transfer': mod.getSolutions("Q_transfer")[0],
            'P_electric': mod.getSolutions("P_electric")[0],
        }

        results_list.append(results)
        print(f"    Final power: {results['P_electric'][-1]/1e6:.2f} MW")

    return results_list


def plot_parameter_study(param_name, param_label, results_list, output_file):
    """Create visualization for parameter study results."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'SMR Parameter Study: {param_label}',
                 fontsize=16, fontweight='bold')

    # Color map for different parameter values
    colors = plt.cm.viridis(np.linspace(0, 1, len(results_list)))

    # Panel 1: Core Temperature
    ax1 = axes[0, 0]
    for result, color in zip(results_list, colors):
        label = f'{param_name}={result["param_value"]}'
        ax1.plot(result['time'], result['T_core'] - 273.15,
                color=color, linewidth=2, label=label)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Core Temperature (°C)')
    ax1.set_title('Core Temperature Evolution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Panel 2: Heat Transfer
    ax2 = axes[0, 1]
    for result, color in zip(results_list, colors):
        label = f'{param_name}={result["param_value"]}'
        ax2.plot(result['time'], result['Q_transfer'] / 1e6,
                color=color, linewidth=2, label=label)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Heat Transfer (MW)')
    ax2.set_title('Heat Transfer Rate')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Panel 3: Electric Power
    ax3 = axes[1, 0]
    for result, color in zip(results_list, colors):
        label = f'{param_name}={result["param_value"]}'
        ax3.plot(result['time'], result['P_electric'] / 1e6,
                color=color, linewidth=2, label=label)
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Electric Power (MW)')
    ax3.set_title('Electric Power Output')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Panel 4: Summary comparison (steady-state values)
    ax4 = axes[1, 1]
    param_vals = [r['param_value'] for r in results_list]
    final_temps = [r['T_core'][-1] - 273.15 for r in results_list]
    final_powers = [r['P_electric'][-1] / 1e6 for r in results_list]

    ax4_twin = ax4.twinx()

    l1 = ax4.plot(param_vals, final_temps, 'ro-', linewidth=2,
                  markersize=8, label='Core Temp')
    l2 = ax4_twin.plot(param_vals, final_powers, 'bs-', linewidth=2,
                       markersize=8, label='Power Output')

    ax4.set_xlabel(param_label)
    ax4.set_ylabel('Final Core Temp (°C)', color='r')
    ax4_twin.set_ylabel('Final Power (MW)', color='b')
    ax4.set_title('Steady-State Comparison')
    ax4.tick_params(axis='y', labelcolor='r')
    ax4_twin.tick_params(axis='y', labelcolor='b')
    ax4.grid(True, alpha=0.3)

    # Combine legends
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax4.legend(lines, labels, loc='upper left')

    plt.tight_layout()

    output_file.parent.mkdir(exist_ok=True)
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")
    plt.close()


def create_sensitivity_analysis(all_studies, output_file):
    """Create sensitivity analysis comparing all parameter studies."""

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('SMR Parameter Sensitivity Analysis',
                 fontsize=16, fontweight='bold')

    # Prepare data for sensitivity plot
    param_names = []
    power_variations = []
    temp_variations = []

    for param_name, results_list in all_studies.items():
        param_names.append(param_name)

        # Calculate variation (max - min) / mean
        powers = [r['P_electric'][-1] for r in results_list]
        temps = [r['T_core'][-1] for r in results_list]

        power_var = (max(powers) - min(powers)) / np.mean(powers) * 100
        temp_var = (max(temps) - min(temps)) / np.mean(temps) * 100

        power_variations.append(power_var)
        temp_variations.append(temp_var)

    # Panel 1: Power output sensitivity
    ax1 = axes[0]
    bars1 = ax1.bar(param_names, power_variations, color='skyblue',
                    edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Power Variation (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Sensitivity of Power Output to Parameters', fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar, val in zip(bars1, power_variations):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')

    # Panel 2: Core temperature sensitivity
    ax2 = axes[1]
    bars2 = ax2.bar(param_names, temp_variations, color='salmon',
                    edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Temperature Variation (%)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Parameter', fontsize=12, fontweight='bold')
    ax2.set_title('Sensitivity of Core Temperature to Parameters', fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar, val in zip(bars2, temp_variations):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    output_file.parent.mkdir(exist_ok=True)
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")
    plt.close()


def main():
    """Main execution function."""

    print("=" * 70)
    print("SMR Power Plant - Parameter Study")
    print("=" * 70)

    # Define paths
    project_dir = pathlib.Path(__file__).parent.parent.parent
    model_file = project_dir / "mo_example" / "srm.mo"
    model_name = "SMR_PowerPlant"
    output_dir = pathlib.Path(__file__).parent / "results"

    # Define parameter studies
    studies = {
        'UA': {
            'label': 'Heat Exchanger UA (W/K)',
            'values': [3e4, 5e4, 7e4, 9e4]
        },
        'eff_thermal': {
            'label': 'Thermal Efficiency',
            'values': [0.25, 0.30, 0.35, 0.40]
        },
        'm_coolant': {
            'label': 'Coolant Mass (kg)',
            'values': [300, 500, 700, 900]
        }
    }

    try:
        all_results = {}

        for i, (param_name, study_config) in enumerate(studies.items(), 1):
            print(f"\n[{i}/{len(studies)}] Parameter study: {param_name}")
            print("=" * 70)

            results_list = run_parameter_sweep(
                model_file, model_name,
                param_name, study_config['values'],
                sim_time=1000
            )

            all_results[param_name] = results_list

            print(f"\n  Creating plots for {param_name}...")
            plot_parameter_study(
                param_name, study_config['label'],
                results_list,
                output_dir / f"param_study_{param_name}.png"
            )

        print(f"\n[{len(studies)+1}/{len(studies)+1}] Creating sensitivity analysis...")
        create_sensitivity_analysis(
            all_results,
            output_dir / "sensitivity_analysis.png"
        )

        print("\n" + "=" * 70)
        print("✓ All parameter studies completed successfully!")
        print("=" * 70)
        print(f"\nResults saved in: {output_dir}")
        for param_name in studies.keys():
            print(f"  - param_study_{param_name}.png")
        print("  - sensitivity_analysis.png")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
