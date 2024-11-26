import os

from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy, \
    QSpacerItem

from source.view.modules.gui_device import DeviceBox


class MotionControlBox(DeviceBox):

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
        pixmap = QPixmap('view/icons/devices/KCube_780by780.jpg')
        pixmap = pixmap.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio)  # Adjust the size as needed
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        icon_button_layout.addWidget(image_label)

        # Create a vertical layout for the button rows
        button_layout = QVBoxLayout()

        # Using `add_buttons` to add buttons dynamically
        self.add_buttons(button_layout)

        icon_button_layout.addLayout(button_layout)
        main_layout.addLayout(icon_button_layout)

        # Create a horizontal layout for name and serial number labels
        name_serial_layout = QHBoxLayout()

        # Add the device name label
        name_label = QLabel(f"<b>Motion control:</b> {self.name}", self)
        name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        name_serial_layout.addWidget(name_label)

        # Add the serial number label, right-aligned
        serial_number_label = QLabel(f"<b>Serial:</b> {str(self.serial)}", self)
        serial_number_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        name_serial_layout.addWidget(serial_number_label)

        # Add the combined horizontal layout to the main layout
        main_layout.addLayout(name_serial_layout)

        self.setLayout(main_layout)
        # Set size policies (optional: ensure it expands well)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

    def add_buttons(self, layout: QVBoxLayout):
        button_row_layout_1 = QHBoxLayout()

        button_1 = self.create_button(icon_path='play-circle-light.svg', tooltip='Play', shown_state='loaded')
        button_2 = self.create_button(icon_path='pause-circle-light.svg', tooltip='Pause', shown_state='connected')
        button_3 = self.create_button(icon_path='arrow-circle-up-light.svg', tooltip='Load', shown_state='connected')
        button_4 = self.create_button(icon_path='arrow-counter-clockwise-light.svg', tooltip='Reload', shown_state='loaded')
        button_5 = self.create_button(icon_path='x-circle-light.svg', tooltip='Close', shown_state='loaded')

        # Connect buttons to their corresponding slots
        button_1.clicked.connect(self.on_button_play_clicked)
        button_2.clicked.connect(self.on_button_pause_clicked)
        button_3.clicked.connect(self.on_button_load_clicked)
        button_4.clicked.connect(self.on_button_reload_clicked)
        button_5.clicked.connect(self.on_button_close_clicked)

        # Adding spacers for alignment
        left_spacer = QSpacerItem(40, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        right_spacer = QSpacerItem(40, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Add left spacer for left-aligned buttons
        button_row_layout_1.addWidget(button_1)
        button_row_layout_1.addWidget(button_2)
        button_row_layout_1.addSpacerItem(left_spacer)

        # Add right spacer for right-aligned buttons
        button_row_layout_1.addSpacerItem(right_spacer)
        button_row_layout_1.addWidget(button_3)
        button_row_layout_1.addWidget(button_4)
        button_row_layout_1.addWidget(button_5)

        layout.addLayout(button_row_layout_1)

        # Second row of buttons
        button_row_layout_2 = QHBoxLayout()
        button_view = self.create_button(icon_path='eye-light.svg', tooltip='View', shown_state='default')
        button_settings = self.create_button(icon_path='gear-light.svg', tooltip='Settings', shown_state='default')

        # Connect buttons to their corresponding slots
        button_view.clicked.connect(self.on_button_view_clicked)
        button_settings.clicked.connect(self.on_button_settings_clicked)

        # Add buttons to the second row layout
        button_row_layout_2.addWidget(button_view)
        button_row_layout_2.addSpacerItem(left_spacer)
        button_row_layout_2.addSpacerItem(right_spacer)
        button_row_layout_2.addWidget(button_settings)

        layout.addLayout(button_row_layout_2)

    def update_status(self, new_status: str) -> None:
        """
        Updates the GUI interface when the device is loaded. Must be implemented by subclasses.
        """
        raise NotImplementedError()

    # Slots for button signals
    @Slot()
    def on_button_play_clicked(self):
        self.button_pressed.emit('Play', self.serial, self.type)

    @Slot()
    def on_button_pause_clicked(self):
        self.button_pressed.emit('Pause', self.serial, self.type)

    @Slot()
    def on_button_load_clicked(self):
        self.button_pressed.emit('Load', self.serial, self.type)

    @Slot()
    def on_button_reload_clicked(self):
        self.button_pressed.emit('Reload', self.serial, self.type)

    @Slot()
    def on_button_close_clicked(self):
        self.button_pressed.emit('Close', self.serial, self.type)

    @Slot()
    def on_button_view_clicked(self):
        self.button_pressed.emit('View', self.serial, self.type)

    @Slot()
    def on_button_settings_clicked(self):
        self.button_pressed.emit('Settings', self.serial, self.type)
