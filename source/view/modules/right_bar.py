from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QSplitter, QTabWidget, QHBoxLayout

from source.view.modules.gui_camera import GUICamera
from source.view.modules.gui_camera_settings import CameraSettingsGUI


class RightBarGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Load devices panel
        self.camera_bar = GUICamera()
        self.slm_bar = GUICamera()
        self.shifts_bar = GUICamera()
        self.piezo_bar = GUICamera()
        self.filter_bar = GUICamera()

        # Init UI
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Splitter
        splitter = QSplitter(Qt.Orientation.Vertical)


        # Connected bar
        H_layout = QVBoxLayout()

        # Connected label
        connected_label = QLabel('--- Connected devices ---')
        connected_label.setAlignment(Qt.AlignCenter)
        connected_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        H_layout.addWidget(connected_label)

        # Connected devices panel
        # tabs for selection of different menus
        tabs = QTabWidget()
        tabs.addTab(self.camera_bar, 'Camera')  # 0
        tabs.addTab(self.slm_bar, 'SLM')     # 1
        tabs.addTab(self.shifts_bar, 'Shifts')  # 2
        tabs.addTab(self.piezo_bar, 'Piezo')   # 3
        tabs.addTab(self.filter_bar, 'Filter')  # 4
        H_layout.addWidget(tabs)

        H_widget = QWidget()
        H_widget.setLayout(H_layout)

        splitter.addWidget(H_widget)


        # Settings panel
        settings_bar = CameraSettingsGUI("...", 100, 200, 300)
        splitter.addWidget(settings_bar)

        # Splitter
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        layout.addWidget(splitter)


        #self.setMinimumWidth(400)
        self.setLayout(layout)