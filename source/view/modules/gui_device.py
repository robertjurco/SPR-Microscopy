import os

from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy

from source.tools import QIcon_modify_color


class DeviceBox(QWidget):
    """
    Abstract base class for creating device boxes. Provides a blueprint for device-specific box implementations.
    """
    button_pressed = Signal(str, str, str)  # Button name, Serial, Device type

    def __init__(self, serial: int, name: str, type: str, status: str):
        """
        Initializes the DeviceBox.

        Parameters:
        name (str): The name of the device.
        status (str): The status of the device ("Loaded" or "Not Loaded").
        """
        super().__init__()
        self.serial = serial
        self.name = name
        self.type = type
        self.status = status

    def create_button(self, icon_path: str, tooltip: str, shown_state: str = 'loaded') -> QPushButton:
        button = QPushButton(self)
        icon = QIcon_modify_color('view/icons/controls/' + icon_path, 'black')
        button.setIcon(icon)
        button.setIconSize(QSize(40, 40))  # Adjust the size as needed
        button.setToolTip(tooltip)
        button.setFixedSize(40, 40)  # Ensuring the buttons are square

        return button

    def disconnected(self):
        print(f"Device {self.serial} is disconnected")

    def init_ui(self):
        """
        Initializes the user interface for the device box. Must be implemented by subclasses.
        """
        raise NotImplementedError()

    def update_status(self, new_status: str) -> None:
        """
        Updates the GUI interface when the device is loaded. Must be implemented by subclasses.
        """
        raise NotImplementedError()

    @Slot()
    def on_load_button_pressed(self) -> None:
        """
        Event handler for the load button press. Must be implemented by subclasses.
        """
        raise NotImplementedError()

    @Slot()
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

