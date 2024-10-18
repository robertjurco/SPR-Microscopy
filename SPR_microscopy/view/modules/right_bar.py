from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QSplitter, QTabWidget

from view.modules.gui_camera import GUICamera


class SettingsGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label
        label = QLabel('--- Settings ---')
        layout.addWidget(label)

        # Scroll area
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        for i in range(1):
            scroll_layout.addWidget(QLabel(f"Device {i + 1}"))
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        self.setLayout(layout)

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

        # Connected devices panel
        # tabs for selection of different menus
        tabs = QTabWidget()
        tabs.addTab(self.camera_bar, 'Camera')  # 0
        tabs.addTab(self.slm_bar, 'SLM')     # 1
        tabs.addTab(self.shifts_bar, 'Shifts')  # 2
        tabs.addTab(self.piezo_bar, 'Piezo')   # 3
        tabs.addTab(self.filter_bar, 'Filter')  # 4

        splitter.addWidget(tabs)


        # Settings panel
        settings_bar = SettingsGUI()
        splitter.addWidget(settings_bar)

        # Splitter
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        layout.addWidget(splitter)


        #self.setMinimumWidth(400)
        self.setLayout(layout)