from PySide6.QtWidgets import QComboBox, QLabel, QHBoxLayout, QSpinBox
from source.view.widgets.plotting_widgets import PlotWidget  # Assuming this is a custom widget for plotting

import csv
import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6.QtCore import Slot


class ColorMeshWidget(QWidget):
    def __init__(self, parent=None, x_label="X-axis", y_label="Y-axis", log_scale=False):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.ax = self.figure.add_subplot(111)
        self.colorbar = None

        self.x_label = x_label
        self.y_label = y_label
        self.log_scale = log_scale

        self.plot_button = QPushButton("Plot Data")
        self.save_data_button = QPushButton("Save Data")

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.save_data_button)
        self.setLayout(layout)

        self.plot_button.clicked.connect(self._trigger_plot)
        self.save_data_button.clicked.connect(self.save_data)

        self.data = {
            "x_vals": [],  # list of unique x values
            "y_vals": [],  # list of unique y values
            "z_grid": []   # 2D grid as list of lists
        }

    def _trigger_plot(self):
        if self.data["x_vals"] and self.data["y_vals"] and self.data["z_grid"]:
            self._replot()

    def _replot(self):
        self.ax.clear()

        x = self.data["x_vals"]
        y = self.data["y_vals"]
        z = np.array(self.data["z_grid"])

        if self.log_scale:
            self.ax.set_xscale("log")
            self.ax.set_yscale("log")
        else:
            self.ax.set_xscale("linear")
            self.ax.set_yscale("linear")

        mesh = self.ax.pcolormesh(x, y, z, shading='auto', cmap='viridis')

        if self.colorbar:
            self.colorbar.remove()
        self.colorbar = self.figure.colorbar(mesh, ax=self.ax)

        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.figure.tight_layout()
        self.canvas.draw()


    def update_plot(self, x, y, z_value):
        """
        Add a single (x, y, z) value into the grid.
        Dynamically updates meshgrid and Z matrix.
        """
        x_vals = self.data["x_vals"]
        y_vals = self.data["y_vals"]
        z_grid = self.data["z_grid"]

        # Insert x if new
        if x not in x_vals:
            x_vals.append(x)
            x_vals.sort()
            for row in z_grid:
                row.insert(x_vals.index(x), np.nan)

        # Insert y if new
        if y not in y_vals:
            y_vals.append(y)
            y_vals.sort()
            row_len = len(x_vals)
            z_grid.insert(y_vals.index(y), [np.nan] * row_len)

        # Update z value at proper index
        xi = x_vals.index(x)
        yi = y_vals.index(y)
        z_grid[yi][xi] = z_value

        self._replot()

    @Slot()
    def save_data(self):
        if not self.data["z_grid"]:
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Data", "", "CSV Files (*.csv);;All Files (*)", options=options
        )
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([""] + self.data["x_vals"])
                for y, row in zip(self.data["y_vals"], self.data["z_grid"]):
                    writer.writerow([y] + row)

    def set_labels(self, x_label, y_label):
        self.x_label = x_label
        self.y_label = y_label
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.canvas.draw()

    def set_log_scale(self, log_scale):
        self.log_scale = log_scale
        self._replot()

class CameraFPSView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_content()

        self.setWindowTitle("Camera FPS meter")
        #self.showMaximized()  # Show the window in fullscreen

    def setup_content(self):
        # Main horizontal layout (to arrange PlotWidget on left and settings on the right)
        main_layout = QHBoxLayout()

        # Top part - PlotWidget (on the left side)
        self.plot_widget = PlotWidget(x_label="Exposure [ms]", y_label="FPS", log_scale=True, scatter_plot=True)  # Assuming you have a PlotWidget defined elsewhere
        main_layout.addWidget(self.plot_widget)
        self.plot_widget_2 = PlotWidget(x_label="Height [px]", y_label="FPS", scatter_plot=True)  # Assuming you have a PlotWidget defined elsewhere
        main_layout.addWidget(self.plot_widget_2)  # Give it more space with a stretch factor
        self.plot_widget_3 = ColorMeshWidget(x_label="Height [px]", y_label="Exposure [ms]",)  # Assuming you have a PlotWidget defined elsewhere
        main_layout.addWidget(self.plot_widget_3)  # Give it more space with a stretch factor

        # Right part - Settings section
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)

        # Camera selection
        self.camera_select = QComboBox()
        self.camera_select.addItem("Select Camera")  # Default item
        # Populate with cameras from other parts of the code (example method call)
        self.populate_camera_list()  # Add your method to populate cameras
        settings_layout.addWidget(QLabel("Camera Selection"))
        settings_layout.addWidget(self.camera_select)

        # Add action buttons for saving the project and noise analysis
        self.save_project_button = QPushButton("Save Project")
        self.noise_analysis_button = QPushButton("Noise Analysis")
        settings_layout.addWidget(self.save_project_button)
        settings_layout.addWidget(self.noise_analysis_button)

        # Add label to display noise value (will update later based on calculations)
        self.noise_label = QLabel("Noise: Not calculated yet")
        settings_layout.addWidget(self.noise_label)

        # Create label for "Average Noise over"
        self.average_noise_label = QLabel("Noise Averaging Interval (Seconds):")
        settings_layout.addWidget(self.average_noise_label)

        # Create spinbox for positive numbers with a step size of 10
        self.noise_duration_spinbox = QSpinBox()
        self.noise_duration_spinbox.setRange(10, 3600)  # Set range from 10 seconds to 3600 seconds (1 hour)
        self.noise_duration_spinbox.setSingleStep(10)  # Set step size to 10 seconds
        self.noise_duration_spinbox.setPrefix("Seconds: ")
        settings_layout.addWidget(self.noise_duration_spinbox)

        # Add the settings widget layout to the main layout
        main_layout.addWidget(settings_widget)  # Settings take up the remaining space

        # Set the layout for this window
        self.setLayout(main_layout)

    def populate_camera_list(self):
        """Populate the camera selection list."""
        cameras = ["Camera 1", "Camera 2", "Camera 3"]
        self.camera_select.addItems(cameras)
