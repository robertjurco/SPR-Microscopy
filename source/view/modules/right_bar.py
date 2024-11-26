from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSplitter, QTabWidget, QPushButton, QScrollArea, QHBoxLayout
from PySide6.QtCore import Qt, Signal, Slot

from source.view.modules.gui_device import DeviceBox
from source.view.modules.gui_devices.gui_camera import CameraBox
from source.view.modules.gui_devices.gui_camera_settings import CameraSettingsGUI
from source.view.modules.gui_devices.gui_motion_control import MotionControlBox
from source.view.modules.gui_devices.gui_slm import SLMBox


def create_device_box(serial: int, device: dict) -> DeviceBox:
    """
    Creates a specific device box based on the device type.

    Parameters:
    serial (str): The serial number of the device.
    device (dict): The dictionary containing the device details, including the name, type, and status.

    Returns:
    DeviceBox: A concrete implementation of DeviceBox specific to the device type.
    """
    device_type = device['type']
    status = device['status']
    name = device['name']

    if device_type == "camera":
        return CameraBox(serial, name, device_type, status)
    if device_type == "motion_control":
        return MotionControlBox(serial, name, device_type, status)
    if device_type == "slm":
        return SLMBox(serial, name, device_type, status)


class RightBarGUI(QWidget):
    """
    Class for the right panel of the GUI.

    This class is responsible for creating and managing the right panel of the GUI,
    which includes various settings and connected devices components.
    """

    button_signal = Signal(str, str, str)  # Serial, Device Type, Button Name

    search_button_clicked = Signal()
    load_all_button_clicked = Signal()

    def __init__(self):
        super().__init__()

        # Load devices panel
        self.content_layout = None
        self.settings_bar = CameraSettingsGUI(0)

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
        layout = QVBoxLayout()

        connected_label = QLabel('--- Connected devices ---')
        connected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        connected_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(connected_label)

        # Scroll area setup
        scroll_area = QScrollArea()
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.addStretch(1)  # Stretch at the end
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        unified_search_button = QPushButton('Search')
        load_all_button = QPushButton('Load All')
        button_layout.addWidget(unified_search_button)
        button_layout.addWidget(load_all_button)
        layout.addLayout(button_layout)

        unified_search_button.clicked.connect(self.on_search_button_clicked)
        load_all_button.clicked.connect(self.on_load_all_button_clicked)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def test_reload(self, connected_devices):
        # Clear existing widgets
        for i in reversed(range(self.content_layout.count() - 1)):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)  # Or use widget.deleteLater() if you need to free resources

        # Add new device boxes
        for serial, device in connected_devices.items():
            box = create_device_box(serial, device)
            if box:
                self.content_layout.insertWidget(self.content_layout.count() - 1, box)  # Insert before the stretch
                box.button_pressed.connect(self.handle_button_pressed)

    def on_search_button_clicked(self) -> None:
        """
        Slot to handle the unified search button click.
        This will trigger the search button click for all device types.
        """
        self.search_button_clicked.emit()

    def on_load_all_button_clicked(self) -> None:
        """
        Slot to handle the Load All button click.
        This will trigger loading for all device types.
        """
        self.load_all_button_clicked.emit()

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
            device_box = create_device_box(name, status)
            self.device_boxes.append(device_box)
            self.content_layout.addWidget(device_box)

        # Stretch to keep stuff together
        self.content_layout.addStretch(1)

    @Slot(str, str, str)
    def handle_button_pressed(self, button_name, serial, device_type):
        self.button_signal.emit(button_name, serial, device_type)

    def send_massage_to_box(self, serial, massage):

        return False
