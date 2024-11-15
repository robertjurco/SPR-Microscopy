from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy


# Assuming camera module is imported correctly
# from source.view.modules.gui_devices.gui_camera import CameraBox


def create_button(text: str, slot) -> QPushButton:
    """
    Creates a QPushButton with the specified text and connects it to the provided slot.

    Parameters:
    text (str): The text to display on the button.
    slot (callable): The event handler to connect to the button's clicked signal.

    Returns:
    QPushButton: The created button with the connected slot.
    """
    button = QPushButton(text)
    button.clicked.connect(slot)
    return button


class DeviceBox(QWidget):
    """
    Abstract base class for creating device boxes. Provides a blueprint for device-specific box implementations.
    """
    load_button_pressed = Signal()
    view_button_pressed = Signal()
    settings_button_pressed = Signal()
    reload_button_pressed = Signal()
    close_button_pressed = Signal()

    def __init__(self, name: str, status: str):
        """
        Initializes the DeviceBox.

        Parameters:
        name (str): The name of the device.
        status (str): The status of the device ("Loaded" or "Not Loaded").
        """
        super().__init__()
        self.name = name
        self.status = status
        self.init_ui(name)


    def init_ui(self, name: str):
        """
        Initializes the user interface for the device box. Must be implemented by subclasses.

        Parameters:
        name (str): The name of the device.
        """
        raise NotImplementedError()


    def loaded_GUI(self):
        """
        Updates the GUI interface when the device is loaded. Must be implemented by subclasses.
        """
        raise NotImplementedError()


    def on_load_button_pressed(self) -> None:
        """
        Event handler for the load button press. Must be implemented by subclasses.
        """
        raise NotImplementedError()


    def on_view_button_pressed(self) -> None:
        """
        Event handler for the view button press. Must be implemented by subclasses.
        """
        raise NotImplementedError()


    def on_settings_button_pressed(self) -> None:
        """
        Event handler for the settings button press. Must be implemented by subclasses.
        """
        raise NotImplementedError()


    def on_reload_button_pressed(self) -> None:
        """
        Event handler for the reload button press. Must be implemented by subclasses.
        """
        raise NotImplementedError()


    def on_close_button_pressed(self) -> None:
        """
        Event handler for the close button press. Must be implemented by subclasses.
        """
        raise NotImplementedError()


class CameraBox(DeviceBox):
    """
    Concrete implementation of DeviceBox for camera devices.
    """

    def init_ui(self, name: str):
        """
        Initializes the user interface for the CameraBox.

        Parameters:
        name (str): The name of the camera.
        """
        layout = QVBoxLayout()
        label = QLabel(name)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        self.load_button = create_button('Load', self.on_load_button_pressed)
        self.view_button = create_button('View', self.on_view_button_pressed)
        self.settings_button = create_button('Settings', self.on_settings_button_pressed)
        self.reload_button = create_button('Reload', self.on_reload_button_pressed)
        self.close_button = create_button('Close', self.on_close_button_pressed)

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.view_button)
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.reload_button)
        button_layout.addWidget(self.close_button)

        if self.status == "Loaded":
            self.load_button.hide()
        else:
            self.view_button.hide()
            self.settings_button.hide()
            self.reload_button.hide()
            self.close_button.hide()

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def loaded_GUI(self):
        """
        Updates the CameraBox GUI when the camera is loaded.
        """
        self.load_button.hide()
        self.view_button.show()
        self.settings_button.show()
        self.reload_button.show()
        self.close_button.show()

    def on_load_button_pressed(self):
        """
        Event handler for the load button press. Emits the load_button_pressed signal.
        """
        self.load_button_pressed.emit()

    def on_view_button_pressed(self):
        """
        Event handler for the view button press. Emits the view_button_pressed signal.
        """
        self.view_button_pressed.emit()

    def on_settings_button_pressed(self):
        """
        Event handler for the settings button press. Emits the settings_button_pressed signal.
        """
        self.settings_button_pressed.emit()

    def on_reload_button_pressed(self):
        """
        Event handler for the reload button press. Emits the reload_button_pressed signal.
        """
        self.reload_button_pressed.emit()

    def on_close_button_pressed(self):
        """
        Event handler for the close button press. Emits the close_button_pressed signal.
        """
        self.close_button_pressed.emit()


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