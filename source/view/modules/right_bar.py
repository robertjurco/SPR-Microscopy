from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSplitter, QTabWidget, QPushButton, QScrollArea
from PySide6.QtCore import Qt, Signal

from source.view.modules.gui_device import DeviceBox
from source.view.modules.gui_devices.gui_camera import CameraBox
from source.view.modules.gui_devices.gui_camera_settings import CameraSettingsGUI

class DeviceList(QScrollArea):
    """
    Manages a scrollable list of device boxes.
    """

    def __init__(self, num_devices: int, device_type: str):
        """
        Initializes the DeviceList.

        Parameters:
        num_devices (int): The initial number of devices to be displayed.
        device_type (str): The type of device ("camera", "SLM", etc.).
        """
        super().__init__()
        self.content_widget = None
        self.content_layout = None
        self.device_boxes = []
        self.device_type = device_type
        self.init_ui(num_devices)

    def init_ui(self, num_devices: int) -> None:
        """
        Initializes the user interface for the DeviceList.

        Parameters:
        num_devices (int): The initial number of devices to be displayed.
        """
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.reload_list(0, {"names": {}, "loaded": []})
        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)

    def create_device_box(self, name: str, status: str) -> DeviceBox:
        """
        Creates a specific device box based on the device type.

        Parameters:
        name (str): The name of the device.
        status (str): The status of the device ("Loaded" or "Not Loaded").

        Returns:
        DeviceBox: A concrete implementation of DeviceBox specific to the device type.
        """
        if self.device_type == "camera":
            return CameraBox(name, status)
        return None

    def reload_list(self, num_devices: int, info: dict) -> None:
        """
        Reloads the list of devices with new device data.

        Parameters:
        num_devices (int): The number of devices to be displayed.
        info (dict): Dict containing information about each device.
        """
        # Clear existing widgets
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Clear the list of device boxes
        self.device_boxes = []

        # Add new DeviceBox widgets based on the info received
        for device_id in range(num_devices):
            name = info["names"].get(device_id, f"Device {device_id + 1}")
            status = "Loaded" if device_id in info["loaded"] else "Not Loaded"
            device_box = self.create_device_box(name, status)
            self.device_boxes.append(device_box)
            self.content_layout.addWidget(device_box)

        # Stretch to keep stuff together
        self.content_layout.addStretch(1)

    def load_device(self, index: int) -> None:
        """
        Loads a device and updates its UI.

        Parameters:
        index (int): The index of the device to be loaded.
        """
        device_GUI = self.device_boxes[index]
        device_GUI.status = "Loaded"
        device_GUI.loaded_GUI()


class GUIDevice(QWidget):
    """
    Provides a GUI interface that integrates DeviceList for managing different devices.
    """
    search_button_pressed = Signal()

    def __init__(self, device_type: str):
        """
        Initializes the GUIDevice with default values and sets up the user interface.

        Parameters:
        device_type (str): The type of device ("camera", "SLM", etc.).
        """
        super().__init__()
        self.num_devices = 0
        self.device_type = device_type
        self.device_str = {
            "camera": "Cameras",
            "SLM": "SLMs",
            "motion_control": "Motion controls",
            "piezo": "Piezos",
            "filter": "Filters"
        }

        self.detected_devs_label = QLabel(f'Number of detected {self.device_str[self.device_type]}: {self.num_devices}')
        self.scroll_area = DeviceList(self.num_devices, self.device_type)
        self.search_button = QPushButton(f'Search {self.device_str[self.device_type]}')

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initializes and sets up the user interface components for GUIDevice.

        Sets up the layout, adds widgets to it, and connects signals to slots.
        """
        layout = QVBoxLayout()

        # Label
        label = QLabel("--- Connected devices ---")
        layout.addWidget(label)

        # Detected devices
        self.detected_devs_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.detected_devs_label)

        # Device list
        layout.addWidget(self.scroll_area)

        # Search button
        self.search_button.clicked.connect(self.on_search_button_clicked)
        layout.addWidget(self.search_button)

        # Set self layout
        self.setLayout(layout)

    def on_search_button_clicked(self) -> None:
        """
        Event handler for the search button click. Emits the search_button_pressed signal.
        """
        self.search_button_pressed.emit()

    def reload(self, num_devices: int, info: dict) -> None:
        """
        Reloads the device list with new device data.

        Parameters:
        num_devices (int): The number of detected devices.
        info (dict): Dict containing information about each device.
        """
        self.num_devices = num_devices
        self.detected_devs_label.setText(
            f'Number of detected {self.device_str[self.device_type]}: ' + str(self.num_devices))
        self.scroll_area.reload_list(num_devices, info)

    def load_device(self, index: int) -> None:
        """
        Loads a specific device and updates the GUI.

        Parameters:
        index (int): The index of the device to be loaded.
        """
        self.scroll_area.load_device(index)

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
        self.camera_bar = GUIDevice("camera")
        self.slm_bar = GUIDevice("SLM")
        self.shifts_bar = GUIDevice("motion_control")
        self.piezo_bar = GUIDevice("piezo")
        self.filter_bar = GUIDevice("filter")

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
        tabs.addTab(self.shifts_bar, 'Motion control')  # 2
        tabs.addTab(self.piezo_bar, 'Piezo')  # 3
        tabs.addTab(self.filter_bar, 'Filter')  # 4

        layout.addWidget(tabs)

        widget = QWidget()
        widget.setLayout(layout)

        return widget