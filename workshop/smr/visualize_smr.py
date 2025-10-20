#!/usr/bin/env python3
"""
Comprehensive visualization module for SMR Power Plant simulation.
Creates multiple plots showing different aspects of reactor operation.
"""

import sys
import pathlib
import matplotlib.pyplot as plt
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from OMPython import ModelicaSystem


def simulate_smr(model_file, model_name, sim_time=1000, params=None):
    """Run SMR simulation with optional parameter overrides."""
    mod = ModelicaSystem(
        fileName=str(model_file),
        modelName=model_name,
        build=True
    )

    mod.setSimulationOptions({
        'stopTime': str(sim_time),
        'stepSize': '1.0',
        'tolerance': '1e-6'
    })

    if params:
        mod.setParameters(params)

    mod.simulate()

    # Extract results
    results = {
        'time': mod.getSolutions("time")[0],
        'T_core': mod.getSolutions("T_core")[0],
        'Q_transfer': mod.getSolutions("Q_transfer")[0],
        'P_electric': mod.getSolutions("P_electric")[0],
    }

    # Get parameters
    all_params = mod.getParameters()

    return results, all_params


def create_comprehensive_plot(results, params, output_file):
    """Create a comprehensive 4-panel plot of SMR operation."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('SMR Power Plant - Comprehensive Analysis',
                 fontsize=16, fontweight='bold', y=0.995)

    time = results['time']
    T_core = results['T_core']
    Q_transfer = results['Q_transfer']
    P_electric = results['P_electric']

    # Panel 1: Core Temperature
    ax1 = axes[0, 0]
    ax1.plot(time, T_core - 273.15, 'r-', linewidth=2, label='Core Temperature')
    ax1.axhline(y=float(params['T_steam'])-273.15, color='b',
                linestyle='--', label=f'Steam Temp ({float(params["T_steam"])-273.15:.0f}°C)')
    ax1.set_xlabel('Time (s)', fontsize=11)
    ax1.set_ylabel('Temperature (°C)', fontsize=11)
    ax1.set_title('Core Coolant Temperature', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Panel 2: Heat Transfer
    ax2 = axes[0, 1]
    ax2.plot(time, Q_transfer / 1e6, 'g-', linewidth=2)
    ax2.axhline(y=float(params['Q_fission'])/1e6, color='orange',
                linestyle='--', label=f'Fission Power ({float(params["Q_fission"])/1e6:.0f} MW)')
    ax2.set_xlabel('Time (s)', fontsize=11)
    ax2.set_ylabel('Heat Transfer (MW)', fontsize=11)
    ax2.set_title('Heat Transfer Rate', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Panel 3: Electric Power Output
    ax3 = axes[1, 0]
    ax3.plot(time, P_electric / 1e6, 'b-', linewidth=2)
    avg_power = P_electric.mean() / 1e6
    ax3.axhline(y=avg_power, color='r', linestyle='--',
                label=f'Average ({avg_power:.1f} MW)')
    ax3.set_xlabel('Time (s)', fontsize=11)
    ax3.set_ylabel('Electric Power (MW)', fontsize=11)
    ax3.set_title('Electric Power Output', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Panel 4: Efficiency over time
    ax4 = axes[1, 1]
    Q_fission = float(params['Q_fission'])
    efficiency = (P_electric / Q_fission) * 100
    ax4.plot(time, efficiency, 'purple', linewidth=2)
    nominal_eff = float(params['eff_thermal']) * 100
    ax4.axhline(y=nominal_eff, color='orange', linestyle='--',
                label=f'Nominal ({nominal_eff:.1f}%)')
    ax4.set_xlabel('Time (s)', fontsize=11)
    ax4.set_ylabel('Efficiency (%)', fontsize=11)
    ax4.set_title('Thermal-to-Electric Efficiency', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()

    output_file.parent.mkdir(exist_ok=True)
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")
    plt.close()


def create_energy_flow_diagram(results, params, output_file):
    """Create Sankey-style energy flow diagram."""

    fig, ax = plt.subplots(figsize=(12, 8))

    # Get final steady-state values
    Q_fission = float(params['Q_fission']) / 1e6  # MW
    Q_transfer_final = results['Q_transfer'][-1] / 1e6  # MW
    P_electric_final = results['P_electric'][-1] / 1e6  # MW
    Q_loss = Q_fission - Q_transfer_final  # Heat loss in core
    Q_steam_loss = Q_transfer_final - P_electric_final  # Steam cycle losses

    # Create bar chart showing energy flow
    stages = ['Fission\nPower', 'Heat\nTransfer', 'Electric\nPower']
    values = [Q_fission, Q_transfer_final, P_electric_final]
    colors = ['red', 'orange', 'green']

    bars = ax.bar(stages, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f} MW',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Add loss annotations
    ax.annotate(f'Core Loss\n{Q_loss:.1f} MW',
                xy=(0.5, Q_fission*0.7), fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

    ax.annotate(f'Cycle Loss\n{Q_steam_loss:.1f} MW',
                xy=(1.5, Q_transfer_final*0.6), fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

    ax.set_ylabel('Power (MW)', fontsize=13, fontweight='bold')
    ax.set_title('SMR Energy Flow Diagram (Steady State)',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    # Add efficiency text
    eff_text = f"Overall Efficiency: {(P_electric_final/Q_fission)*100:.1f}%"
    ax.text(0.5, 0.95, eff_text, transform=ax.transAxes,
            fontsize=12, ha='center', va='top',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    plt.tight_layout()
    output_file.parent.mkdir(exist_ok=True)
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")
    plt.close()


def create_transient_analysis(results, params, output_file):
    """Create detailed transient analysis plot."""

    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle('SMR Transient Response Analysis',
                 fontsize=16, fontweight='bold')

    time = results['time']
    T_core = results['T_core']
    Q_transfer = results['Q_transfer']
    P_electric = results['P_electric']

    # Calculate derivatives (rate of change)
    dt = np.diff(time)
    dT_dt = np.diff(T_core) / dt
    dQ_dt = np.diff(Q_transfer) / dt
    dP_dt = np.diff(P_electric) / dt
    time_diff = time[:-1]

    # Panel 1: Temperature and its rate of change
    ax1 = axes[0]
    ax1_twin = ax1.twinx()

    l1 = ax1.plot(time, T_core - 273.15, 'r-', linewidth=2, label='Core Temp')
    l2 = ax1_twin.plot(time_diff, dT_dt, 'b--', linewidth=1.5,
                       alpha=0.7, label='Rate of Change')

    ax1.set_xlabel('Time (s)', fontsize=11)
    ax1.set_ylabel('Temperature (°C)', fontsize=11, color='r')
    ax1_twin.set_ylabel('dT/dt (K/s)', fontsize=11, color='b')
    ax1.set_title('Core Temperature Transient', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='r')
    ax1_twin.tick_params(axis='y', labelcolor='b')
    ax1.grid(True, alpha=0.3)

    # Combine legends
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')

    # Panel 2: Heat transfer dynamics
    ax2 = axes[1]
    ax2.plot(time, Q_transfer / 1e6, 'g-', linewidth=2, label='Heat Transfer')
    Q_fission = float(params['Q_fission'])
    ax2.axhline(y=Q_fission/1e6, color='orange', linestyle='--',
                label='Fission Power')

    ax2.set_xlabel('Time (s)', fontsize=11)
    ax2.set_ylabel('Power (MW)', fontsize=11)
    ax2.set_title('Heat Transfer Dynamics', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Panel 3: Power output settling
    ax3 = axes[2]
    ax3.plot(time, P_electric / 1e6, 'b-', linewidth=2, label='Electric Power')

    # Calculate settling time (when within 2% of final value)
    final_power = P_electric[-1]
    tolerance = 0.02 * final_power
    settled_mask = np.abs(P_electric - final_power) < tolerance
    if np.any(settled_mask):
        settling_time = time[np.argmax(settled_mask)]
        ax3.axvline(x=settling_time, color='r', linestyle='--',
                   label=f'Settling Time: {settling_time:.1f}s')
        ax3.axhline(y=final_power/1e6, color='orange', linestyle=':',
                   alpha=0.5, label=f'Steady State: {final_power/1e6:.1f} MW')

    ax3.set_xlabel('Time (s)', fontsize=11)
    ax3.set_ylabel('Electric Power (MW)', fontsize=11)
    ax3.set_title('Power Output Settling', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    output_file.parent.mkdir(exist_ok=True)
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")
    plt.close()


def main():
    """Main execution function."""

    print("=" * 70)
    print("SMR Power Plant - Comprehensive Visualization")
    print("=" * 70)

    # Define paths
    project_dir = pathlib.Path(__file__).parent.parent.parent
    model_file = project_dir / "mo_example" / "srm.mo"
    model_name = "SMR_PowerPlant"
    output_dir = pathlib.Path(__file__).parent / "results"

    print(f"\nModel file: {model_file}")
    print(f"Model name: {model_name}")

    try:
        print("\n[1/4] Running SMR simulation...")
        results, params = simulate_smr(model_file, model_name, sim_time=1000)
        print("  ✓ Simulation complete")

        print("\n[2/4] Creating comprehensive plot...")
        create_comprehensive_plot(
            results, params,
            output_dir / "smr_comprehensive.png"
        )

        print("\n[3/4] Creating energy flow diagram...")
        create_energy_flow_diagram(
            results, params,
            output_dir / "smr_energy_flow.png"
        )

        print("\n[4/4] Creating transient analysis...")
        create_transient_analysis(
            results, params,
            output_dir / "smr_transient.png"
        )

        print("\n" + "=" * 70)
        print("✓ All visualizations completed successfully!")
        print("=" * 70)
        print(f"\nResults saved in: {output_dir}")
        print("  - smr_comprehensive.png")
        print("  - smr_energy_flow.png")
        print("  - smr_transient.png")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
