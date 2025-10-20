#!/usr/bin/env python3
"""
Interactive parameter explorer for Newton Cooling model.
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


class CoolingModelExplorer:
    """Interactive explorer for Newton Cooling model parameters."""

    def __init__(self, model_file, model_name):
        self.model_file = model_file
        self.model_name = model_name

        # Parameter ranges
        self.param_ranges = {
            'h': (0.1, 2.0, 0.7),    # (min, max, default)
            'm': (0.01, 0.5, 0.1),
            'A': (0.1, 3.0, 1.0),
            'T0': (300, 400, 363.15),
            'c_p': (0.5, 2.0, 1.2)
        }

        # Initial simulation
        self.current_params = {k: v[2] for k, v in self.param_ranges.items()}
        self.simulate()

        # Create interactive plot
        self.setup_interactive_plot()

    def simulate(self):
        """Run simulation with current parameters."""
        mod = ModelicaSystem(
            fileName=self.model_file,
            modelName=self.model_name,
            build=True
        )

        mod.setSimulationOptions({
            'stopTime': '2.0',
            'stepSize': '0.01'
        })

        mod.setParameters({k: str(v) for k, v in self.current_params.items()})
        mod.simulate()

        self.time = mod.getSolutions("time")[0]
        self.temperature = mod.getSolutions("T")[0]
        self.ambient_temp = mod.getSolutions("T_inf")[0]

    def setup_interactive_plot(self):
        """Create the interactive matplotlib figure with sliders."""
        # Create figure with subplots
        self.fig = plt.figure(figsize=(12, 10))
        gs = self.fig.add_gridspec(3, 2, height_ratios=[3, 1, 1],
                                    hspace=0.3, wspace=0.3)

        # Main plot
        self.ax_main = self.fig.add_subplot(gs[0, :])
        self.line_T, = self.ax_main.plot(self.time, self.temperature,
                                          'b-', linewidth=2, label='Object Temperature')
        self.line_Tinf, = self.ax_main.plot(self.time, self.ambient_temp,
                                             'r--', linewidth=2, label='Ambient Temperature')

        self.ax_main.set_xlabel('Time (s)', fontsize=12)
        self.ax_main.set_ylabel('Temperature (K)', fontsize=12)
        self.ax_main.set_title('Newton Cooling Model - Interactive Explorer',
                               fontsize=14, fontweight='bold')
        self.ax_main.legend(fontsize=11)
        self.ax_main.grid(True, alpha=0.3)

        # Create sliders
        self.sliders = {}
        slider_positions = [
            (gs[1, 0], 'h', 'Convection Coef. h'),
            (gs[1, 1], 'm', 'Mass m'),
            (gs[2, 0], 'A', 'Surface Area A'),
            (gs[2, 1], 'T0', 'Initial Temp T0'),
        ]

        for position, param, label in slider_positions:
            ax_slider = self.fig.add_subplot(position)
            min_val, max_val, init_val = self.param_ranges[param]

            slider = Slider(
                ax=ax_slider,
                label=label,
                valmin=min_val,
                valmax=max_val,
                valinit=init_val,
                orientation='horizontal'
            )
            slider.on_changed(lambda val, p=param: self.update_parameter(p, val))
            self.sliders[param] = slider

        # Add text box for parameter info
        self.info_text = self.fig.text(
            0.5, 0.02,
            self.get_info_string(),
            ha='center',
            fontsize=10,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )

        plt.suptitle('Adjust parameters using sliders below',
                    y=0.98, fontsize=12, style='italic')

    def update_parameter(self, param_name, value):
        """Update a parameter and re-simulate."""
        print(f"Updating {param_name} = {value:.3f}")
        self.current_params[param_name] = value

        # Re-simulate
        try:
            self.simulate()

            # Update plot
            self.line_T.set_ydata(self.temperature)
            self.line_Tinf.set_ydata(self.ambient_temp)

            # Update y-axis limits
            all_temps = np.concatenate([self.temperature, self.ambient_temp])
            margin = 5
            self.ax_main.set_ylim(all_temps.min() - margin, all_temps.max() + margin)

            # Update info text
            self.info_text.set_text(self.get_info_string())

            self.fig.canvas.draw_idle()

        except Exception as e:
            print(f"Error during simulation: {e}")

    def get_info_string(self):
        """Generate info string with current parameters and results."""
        final_temp = self.temperature[-1]
        initial_temp = self.temperature[0]
        temp_drop = initial_temp - final_temp

        info = (
            f"Parameters: h={self.current_params['h']:.3f}, "
            f"m={self.current_params['m']:.3f}, "
            f"A={self.current_params['A']:.3f}, "
            f"T0={self.current_params['T0']:.2f}K | "
            f"Final T={final_temp:.2f}K (drop: {temp_drop:.2f}K)"
        )
        return info

    def show(self):
        """Display the interactive plot."""
        plt.show()


def main():
    """Main execution function."""
    project_dir = pathlib.Path(__file__).parent.parent.parent
    model_file = str(project_dir / "mo_example" / "bouncingball.mo")
    model_name = "NewtonCoolingDynamic"

    print("=" * 70)
    print("Newton Cooling Model - Interactive Explorer")
    print("=" * 70)
    print("\nStarting interactive explorer...")
    print("Adjust the sliders to see how parameters affect the cooling process.")
    print("\nNote: Each slider adjustment will trigger a new simulation.")
    print("=" * 70)

    try:
        explorer = CoolingModelExplorer(model_file, model_name)
        explorer.show()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
