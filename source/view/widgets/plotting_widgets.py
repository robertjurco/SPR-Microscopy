import sys
import csv
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, \
    QSpinBox, QHBoxLayout
from PySide6.QtCore import Slot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure



class PlotWidget(QWidget):
    def __init__(self, parent=None, x_label="X-axis", y_label="Y-axis", log_scale=False, scatter_plot=False):
        super().__init__(parent)

        self.setFixedSize(600, 600)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Create subplot and set labels
        self.ax = self.figure.add_subplot(111)

        self.x_label = x_label
        self.y_label = y_label
        self.log_scale = log_scale
        self.scatter_plot = scatter_plot

        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)

        self.save_data_button = QPushButton("Save Data")

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.save_data_button)

        self.setLayout(layout)

        self.save_data_button.clicked.connect(self.save_data)

        self.data = {"x": None, "y": None}  # To store the plotted data

    @Slot()
    def plot_data(self, x=None, y=None, scatter_plot=False, color='blue', clear=False):
        """
        Plot data as a scatter plot or line plot.
        If data is passed, plot it.
        """
        if x is None or y is None:
            return  # Don't plot if data is not provided

        if clear:
            self.ax.clear()  # Clear previous plots

        if self.log_scale:
            self.ax.set_xscale("log")
            self.ax.set_yscale("log")

        if scatter_plot:
            self.ax.scatter(x, y, color=color, s=2)
        else:
            self.ax.plot(x, y, color=color)

        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.figure.tight_layout()  # Adjust layout to avoid overlap
        self.canvas.draw()

        self.data = {"x": x, "y": y}  # Store the data for potential saving

    @Slot()
    def update_plot(self, x, y):
        """
        Update the plot by adding a new point (or data series).
        This allows for dynamic updates to the plot (i.e., adding new points).
        """
        if self.data["x"] is not None and self.data["y"] is not None:
            self.data["x"].append(x)
            self.data["y"].append(y)
        else:
            self.data["x"] = [x]
            self.data["y"] = [y]

        self.plot_data(self.data["x"], self.data["y"])

    @Slot()
    def save_data(self):
        """
        Save the plotted data to a CSV file.
        """
        if self.data["x"] is None or self.data["y"] is None:
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Data", "", "CSV Files (*.csv);;All Files (*)", options=options
        )
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["x", "y"])
                for xi, yi in zip(self.data["x"], self.data["y"]):
                    writer.writerow([xi, yi])

    def set_labels(self, x_label, y_label):
        """Allow dynamic updating of axis labels."""
        self.x_label = x_label
        self.y_label = y_label
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.canvas.draw()

    def set_log_scale(self, log_scale):
        """Enable or disable logarithmic scale for both axes."""
        self.log_scale = log_scale
        if self.log_scale:
            self.ax.set_xscale("log")
            self.ax.set_yscale("log")
        else:
            self.ax.set_xscale("linear")
            self.ax.set_yscale("linear")
        self.canvas.draw()

    def set_scatter_plot(self, scatter_plot):
        """Switch between scatter plot and line plot."""
        self.scatter_plot = scatter_plot
        self.plot_data(self.data["x"], self.data["y"])

class HistogramPlotWidget(QWidget):
    def __init__(self, parent=None, x_label="Value", y_label="Frequency", bins=50):
        super().__init__(parent)

        self.setFixedSize(600, 600)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)

        self.bins = bins
        self.last_data = None
        self.hist_data = None

        # UI elements
        self.save_data_button = QPushButton("Save Histogram Data")

        self.bin_label = QLabel("Number of bins:")
        self.bin_spinbox = QSpinBox()
        self.bin_spinbox.setRange(1, 1000)
        self.bin_spinbox.setValue(self.bins)
        self.bin_spinbox.valueChanged.connect(self.update_bins)

        bin_layout = QHBoxLayout()
        bin_layout.addWidget(self.bin_label)
        bin_layout.addWidget(self.bin_spinbox)
        bin_layout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(bin_layout)
        layout.addWidget(self.save_data_button)

        self.setLayout(layout)
        self.save_data_button.clicked.connect(self.save_data)

    @Slot()
    def plot_histogram(self, data, color='blue', clear=True):
        if data is None or len(data) == 0:
            return

        self.last_data = data

        if clear:
            self.ax.clear()

        counts, bin_edges, _ = self.ax.hist(data, bins=self.bins, color=color, alpha=0.7, edgecolor='black')

        self.ax.set_xlabel(self.ax.get_xlabel())
        self.ax.set_ylabel(self.ax.get_ylabel())
        self.figure.tight_layout()
        self.canvas.draw()

        self.hist_data = {
            "bin_edges": bin_edges,
            "counts": counts
        }

    def update_bins(self, value):
        self.bins = value
        if self.last_data is not None:
            self.plot_histogram(self.last_data)

    @Slot()
    def save_data(self):
        if self.hist_data is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Histogram Data", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Bin Start", "Bin End", "Count"])
                bin_edges = self.hist_data["bin_edges"]
                counts = self.hist_data["counts"]

                for i in range(len(counts)):
                    writer.writerow([bin_edges[i], bin_edges[i + 1], counts[i]])

