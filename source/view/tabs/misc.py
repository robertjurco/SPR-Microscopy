import sys
import csv
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PySide6.QtCore import Slot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")

        self.plot_button = QPushButton("Plot Data")
        self.save_data_button = QPushButton("Save Data")

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        #layout.addWidget(self.plot_button)
        #layout.addWidget(self.save_data_button)

        self.setLayout(layout)

        self.plot_button.clicked.connect(self.plot_data)
        self.save_data_button.clicked.connect(self.save_data)

        self.data = None  # To store the plotted data

    @Slot()
    def plot_data(self):
        # Example data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.figure.tight_layout()  # Adjust layout
        self.canvas.draw()

        self.data = {"x": x, "y": y}  # Store the data

    @Slot()
    def save_data(self):
        if self.data is None:
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

