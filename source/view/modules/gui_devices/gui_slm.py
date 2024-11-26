import os

from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy

from source.view.modules.gui_device import DeviceBox


class SLMBox(DeviceBox):

    def __init__(self, serial: int, name: str, type: str, status: str):
        super().__init__(serial, name, type, status)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface for the device box. Must be implemented by subclasses.
        """
        # Create and set the layout for the device widget
        main_layout = QVBoxLayout()

        # Create a layout for the icon and buttons
        icon_button_layout = QHBoxLayout()

        # Add the device image
        image_label = QLabel(self)
        pixmap = QPixmap('view/icons/devices/SLM_780by780.jpg')
        pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)  # Adjust the size as needed
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        icon_button_layout.addWidget(image_label)

        # Create a vertical layout for the button rows
        button_layout = QVBoxLayout()

        # Add button rows
        icon_path = 'view/icons/arrows-counter-clockwise-duotone.svg'
        for _ in range(2):  # Two lines of buttons
            button_row_layout = QHBoxLayout()
            for _ in range(6):  # Number of buttons you want in each row
                button = QPushButton(self)
                button.setIcon(QIcon(icon_path))
                button.setIconSize(QSize(40, 40))  # Adjust the size as needed
                button.setToolTip("text")
                button.setFixedSize(40, 40)  # Ensuring the buttons are square
                button_row_layout.addWidget(button)

            button_layout.addLayout(button_row_layout)

        icon_button_layout.addLayout(button_layout)

        main_layout.addLayout(icon_button_layout)

        # Add the device name label
        name_label = QLabel(f"<b>SLM:</b> {self.name}", self)
        name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(name_label)

        # Add the serial number label, right-aligned
        serial_number_label = QLabel(f"<b>Serial:</b> {str(self.serial)}", self)
        serial_number_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(serial_number_label)

        self.setLayout(main_layout)
        # Set size policies (optional: ensure it expands well)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

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

