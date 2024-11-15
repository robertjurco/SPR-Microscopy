from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy

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

