#!/usr/bin/env python3
"""
Interactive dashboard for SMR Power Plant model.
Allows real-time parameter adjustment and visualization.
"""

import sys
import pathlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from OMPython import ModelicaSystem


class SMRDashboard:
    """Interactive dashboard for SMR Power Plant parameters."""

    def __init__(self, model_file, model_name):
        self.model_file = model_file
        self.model_name = model_name

        # Parameter ranges (min, max, default)
        self.param_ranges = {
            'Q_fission': (5e7, 2e8, 1e8),        # Fission power (W)
            'eff_thermal': (0.20, 0.45, 0.35),   # Efficiency
            'UA': (2e4, 1e5, 5e4),               # Heat exchanger UA (W/K)
            'm_coolant': (200, 1000, 500),       # Coolant mass (kg)
        }

        # Initial simulation
        self.current_params = {k: v[2] for k, v in self.param_ranges.items()}
        self.simulate()

        # Create interactive plot
        self.setup_interactive_plot()

    def simulate(self):
        """Run simulation with current parameters."""
        print(f"Simulating with: {self.current_params}")

        mod = ModelicaSystem(
            fileName=self.model_file,
            modelName=self.model_name,
            build=True
        )

        mod.setSimulationOptions({
            'stopTime': '1000',
            'stepSize': '2.0'
        })

        mod.setParameters({k: str(v) for k, v in self.current_params.items()})
        mod.simulate()

        self.time = mod.getSolutions("time")[0]
        self.T_core = mod.getSolutions("T_core")[0]
        self.Q_transfer = mod.getSolutions("Q_transfer")[0]
        self.P_electric = mod.getSolutions("P_electric")[0]

    def setup_interactive_plot(self):
        """Create the interactive matplotlib figure with sliders."""
        # Create figure with subplots
        self.fig = plt.figure(figsize=(15, 11))
        gs = self.fig.add_gridspec(4, 2, height_ratios=[3, 1, 1, 1],
                                    hspace=0.35, wspace=0.3)

        # Main plots (3 panels in top row)
        self.ax_temp = self.fig.add_subplot(gs[0, 0])
        self.ax_power = self.fig.add_subplot(gs[0, 1])

        # Initialize plots
        self.line_temp, = self.ax_temp.plot(
            self.time, self.T_core - 273.15,
            'r-', linewidth=2, label='Core Temperature'
        )
        self.ax_temp.set_xlabel('Time (s)', fontsize=11)
        self.ax_temp.set_ylabel('Temperature (°C)', fontsize=11)
        self.ax_temp.set_title('Core Coolant Temperature',
                               fontsize=12, fontweight='bold')
        self.ax_temp.legend()
        self.ax_temp.grid(True, alpha=0.3)

        self.line_power_e, = self.ax_power.plot(
            self.time, self.P_electric / 1e6,
            'b-', linewidth=2, label='Electric Power'
        )
        self.line_power_t, = self.ax_power.plot(
            self.time, self.Q_transfer / 1e6,
            'g--', linewidth=2, label='Heat Transfer'
        )
        self.ax_power.set_xlabel('Time (s)', fontsize=11)
        self.ax_power.set_ylabel('Power (MW)', fontsize=11)
        self.ax_power.set_title('Power Output',
                                fontsize=12, fontweight='bold')
        self.ax_power.legend()
        self.ax_power.grid(True, alpha=0.3)

        # Create sliders
        self.sliders = {}
        slider_configs = [
            (gs[1, 0], 'Q_fission', 'Fission Power (MW)', 1e6),
            (gs[1, 1], 'eff_thermal', 'Efficiency', 1),
            (gs[2, 0], 'UA', 'Heat Exchanger UA (kW/K)', 1e3),
            (gs[2, 1], 'm_coolant', 'Coolant Mass (kg)', 1),
        ]

        for position, param, label, scale in slider_configs:
            ax_slider = self.fig.add_subplot(position)
            min_val, max_val, init_val = self.param_ranges[param]

            slider = Slider(
                ax=ax_slider,
                label=label,
                valmin=min_val / scale,
                valmax=max_val / scale,
                valinit=init_val / scale,
                orientation='horizontal'
            )
            slider.on_changed(
                lambda val, p=param, s=scale: self.update_parameter(p, val * s)
            )
            self.sliders[param] = slider

        # Add info text box
        self.info_text = self.fig.add_subplot(gs[3, :])
        self.info_text.axis('off')
        self.info_box = self.info_text.text(
            0.5, 0.5, self.get_info_string(),
            ha='center', va='center',
            fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
            transform=self.info_text.transAxes
        )

        plt.suptitle('SMR Power Plant - Interactive Dashboard\n' +
                    'Adjust parameters using sliders below',
                    y=0.98, fontsize=14, fontweight='bold')

    def update_parameter(self, param_name, value):
        """Update a parameter and re-simulate."""
        print(f"\nUpdating {param_name} = {value:.2e}")
        self.current_params[param_name] = value

        # Re-simulate
        try:
            self.simulate()

            # Update plots
            self.line_temp.set_ydata(self.T_core - 273.15)
            self.line_power_e.set_ydata(self.P_electric / 1e6)
            self.line_power_t.set_ydata(self.Q_transfer / 1e6)

            # Update y-axis limits
            temp_margin = 5
            self.ax_temp.set_ylim(
                (self.T_core - 273.15).min() - temp_margin,
                (self.T_core - 273.15).max() + temp_margin
            )

            power_data = np.concatenate([self.P_electric, self.Q_transfer]) / 1e6
            power_margin = power_data.max() * 0.1
            self.ax_power.set_ylim(
                0, power_data.max() + power_margin
            )

            # Update info text
            self.info_box.set_text(self.get_info_string())

            self.fig.canvas.draw_idle()

        except Exception as e:
            print(f"Error during simulation: {e}")
            import traceback
            traceback.print_exc()

    def get_info_string(self):
        """Generate info string with current parameters and results."""
        final_temp = self.T_core[-1] - 273.15
        final_power = self.P_electric[-1] / 1e6
        final_heat = self.Q_transfer[-1] / 1e6
        actual_eff = (self.P_electric[-1] / self.current_params['Q_fission']) * 100

        info = (
            f"Parameters: Q_fission={self.current_params['Q_fission']/1e6:.1f} MW, "
            f"η={self.current_params['eff_thermal']:.2f}, "
            f"UA={self.current_params['UA']/1e3:.1f} kW/K, "
            f"m={self.current_params['m_coolant']:.0f} kg\n"
            f"Steady State: T_core={final_temp:.1f}°C, "
            f"P_electric={final_power:.1f} MW, "
            f"Q_transfer={final_heat:.1f} MW, "
            f"Efficiency={actual_eff:.1f}%"
        )
        return info

    def show(self):
        """Display the interactive plot."""
        plt.show()


def main():
    """Main execution function."""
    project_dir = pathlib.Path(__file__).parent.parent.parent
    model_file = str(project_dir / "mo_example" / "srm.mo")
    model_name = "SMR_PowerPlant"

    print("=" * 70)
    print("SMR Power Plant - Interactive Dashboard")
    print("=" * 70)
    print("\nStarting interactive dashboard...")
    print("Adjust the sliders to see how parameters affect the SMR operation.")
    print("\nNote: Each slider adjustment will trigger a new simulation.")
    print("=" * 70)

    try:
        dashboard = SMRDashboard(model_file, model_name)
        dashboard.show()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
