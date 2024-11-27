from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QComboBox, QPushButton, QLabel)
from source.view.modules.gui_tab import TabGUI
from source.view.modules.tabs.misc import PlotWidget
from PySide6.QtCore import Qt

class ImaginingGUI(TabGUI):
    def __init__(self, index):
        super().__init__(index)
        self.setup_content()

    def setup_content(self):
        # Main vertical layout
        main_layout = QVBoxLayout()

        # Top Widget (PlotWidget)
        plot_widget = PlotWidget()

        # Bottom part (split horizontally into two)
        bottom_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left half (CameraWidget)
        camera_widget = PlotWidget()
        bottom_splitter.addWidget(camera_widget)

        # Right half (Settings)
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)

        # Camera selection
        self.camera_select = QComboBox()
        self.camera_select.addItem("Select Camera")
        # Populate with cameras from other parts of the code (example method call)
        self.populate_camera_list()
        settings_layout.addWidget(QLabel("Camera Selection"))
        settings_layout.addWidget(self.camera_select)

        # Buttons for actions
        acquire_button = QPushButton("Acquire References")
        start_button = QPushButton("Start Measurement")
        settings_layout.addWidget(acquire_button)
        settings_layout.addWidget(start_button)

        bottom_splitter.addWidget(settings_widget)

        # Create splitter to divide the whole layout vertically
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.addWidget(plot_widget)
        main_splitter.addWidget(bottom_splitter)

        # Add the main splitter to the main layout
        main_layout.addWidget(main_splitter)

        # Add the main layout to the content layout of the superclass
        self.content_layout.addLayout(main_layout)

    def populate_camera_list(self):
        # This is just an example. Populate the camera_select with actual cameras.
        cameras = ["Camera 1", "Camera 2", "Camera 3"]
        self.camera_select.addItems(cameras)