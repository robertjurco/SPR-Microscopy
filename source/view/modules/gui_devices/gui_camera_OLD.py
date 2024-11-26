from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy

from source.view.modules.gui_device import DeviceBox


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