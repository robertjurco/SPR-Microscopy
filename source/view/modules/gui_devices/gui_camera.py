from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy


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

class CameraBox(QWidget):
    """
    Class representing a camera box in a QWidget-based UI.

    The CameraBox contains buttons for various actions related to a camera, such as loading, viewing, settings, reloading, and closing.

    Signals:
        load_button_pressed: Emitted when the "Load" button is pressed.
        view_button_pressed: Emitted when the "View" button is pressed.
        settings_button_pressed: Emitted when the "Settings" button is pressed.
        reload_button_pressed: Emitted when the "Reload" button is pressed.
        close_button_pressed: Emitted when the "Close" button is pressed.
    """

    # Define signals to connect to slots
    load_button_pressed = Signal()
    view_button_pressed = Signal()
    settings_button_pressed = Signal()
    reload_button_pressed = Signal()
    close_button_pressed = Signal()

    def __init__(self, name: str, status: str):
        """
        Initialize the CameraBox instance.

        Parameters:
            name (str): The name of the camera.
            status (str): The status of the camera (e.g., "Loaded").
        """
        super().__init__()

        # Initialize UI components
        self.reload_button = None
        self.settings_button = None
        self.view_button = None
        self.close_button = None
        self.load_button = None

        # Set object properties
        self.setObjectName("CameraBox")
        self.name = name
        self.status = status

        # Initialize the user interface
        self.init_ui(name)

    def init_ui(self, name: str):
        """
        Initialize the user interface for the CameraBox.

        Parameters:
            name (str): The name of the camera.
        """
        layout = QVBoxLayout()

        # Create and add label for the camera name
        label = QLabel(name)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Create and add buttons
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

        # Set button visibility based on the status
        if self.status == "Loaded":
            self.load_button.hide()
        else:
            self.view_button.hide()
            self.settings_button.hide()
            self.reload_button.hide()
            self.close_button.hide()

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        # Set the layout for the CameraBox
        self.setLayout(layout)

    def on_load_button_pressed(self) -> None:
        """Slot for handling the "Load" button press event."""
        self.load_button_pressed.emit()

    def on_view_button_pressed(self) -> None:
        """Slot for handling the "View" button press event."""
        self.view_button_pressed.emit()

    def on_settings_button_pressed(self) -> None:
        """Slot for handling the "Settings" button press event."""
        self.settings_button_pressed.emit()

    def on_reload_button_pressed(self) -> None:
        """Slot for handling the "Reload" button press event."""
        self.reload_button_pressed.emit()

    def on_close_button_pressed(self) -> None:
        """Slot for handling the "Close" button press event."""
        self.close_button_pressed.emit()
