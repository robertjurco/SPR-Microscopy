from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSplitter, QTabWidget
from PySide6.QtCore import Qt

from source.view.modules.gui_camera import GUICamera
from source.view.modules.gui_camera_settings import CameraSettingsGUI


class RightBarGUI(QWidget):
    """
    Class for the right panel of the GUI.

    This class is responsible for creating and managing the right panel of the GUI,
    which includes various settings and connected devices components.
    """
    def __init__(self):
        super().__init__()

        # Load devices panel
        self.settings_bar = CameraSettingsGUI(0)
        self.camera_bar = GUICamera()
        self.slm_bar = GUICamera()
        self.shifts_bar = GUICamera()
        self.piezo_bar = GUICamera()
        self.filter_bar = GUICamera()

        # Init UI
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()

        # Create splitter
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Create and add connected devices bar
        connected_devices_widget = self.create_connected_devices_widget()
        splitter.addWidget(connected_devices_widget)

        # Add settings panel to splitter
        splitter.addWidget(self.settings_bar)

        # Set stretch factors for the splitter
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        # Add splitter to the main layout
        layout.addWidget(splitter)
        self.setLayout(layout)

    def create_connected_devices_widget(self) -> QWidget:
        """Create the connected devices widget with tabs."""
        layout = QVBoxLayout()

        # Connected label
        connected_label = QLabel('--- Connected devices ---')
        connected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        connected_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout.addWidget(connected_label)

        # Tabs for selection of different menus
        tabs = QTabWidget()
        tabs.addTab(self.camera_bar, 'Camera')  # 0
        tabs.addTab(self.slm_bar, 'SLM')  # 1
        tabs.addTab(self.shifts_bar, 'Shifts')  # 2
        tabs.addTab(self.piezo_bar, 'Piezo')  # 3
        tabs.addTab(self.filter_bar, 'filter')  # 4

        layout.addWidget(tabs)

        widget = QWidget()
        widget.setLayout(layout)

        return widget