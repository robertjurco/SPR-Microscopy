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


class CameraList(QScrollArea):
    """
    A QScrollArea widget that displays a list of CameraBox widgets.

    Attributes:
        content_widget (QWidget): The main content widget containing the camera boxes.
        content_layout (QVBoxLayout): The layout for the content widget.
        camera_boxes (list): The list storing CameraBox widgets.
    """

    def __init__(self, num_cameras: int) -> None:
        """
        Initializes the CameraList widget.

        Args:
            num_cameras (int): The initial number of camera_models to be displayed.
        """
        super().__init__()
        self.content_widget = None
        self.content_layout = None
        self.camera_boxes = []
        self.init_ui(num_cameras)

    def init_ui(self, num_cameras: int) -> None:
        """
        Initializes the user interface for the CameraList widget.

        Args:
            num_cameras (int): The initial number of camera_models to be displayed.
        """
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        # Initialize the widget with the initial number of camera_models
        self.reload(0, {"names": {}, "loaded": []})
        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)

    def reload(self, num_cameras: int, info: dict) -> None:
        """
        Reloads the camera list with updated information.

        Args:
            num_cameras (int): The number of camera_models to be displayed.
            info (dict): A dictionary containing camera names and loaded status.
                         Expected keys are:
                         - "names": A dict where keys are camera IDs and values are camera names.
                         - "loaded": A list of camera IDs that are loaded.
        """
        # Clear existing widgets
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Clear the list of camera boxes
        self.camera_boxes = []

        # Add new CameraBox widgets based on the info received
        for camera_id in range(num_cameras):
            name = info["names"].get(camera_id, f"Camera {camera_id + 1}")
            status = "Loaded" if camera_id in info["loaded"] else "Not Loaded"
            camera_box = CameraBox(name, status)
            self.camera_boxes.append(camera_box)
            self.content_layout.addWidget(camera_box)

        # Stretch to keep stuff together
        self.content_layout.addStretch(1)


class GUICamera(QWidget):
    """
    GUICamera is a QWidget that represents a graphical interface for managing camera_models.

    Attributes
    ----------
    search_button_pressed : Signal
        Signal to be emitted when the search button is pressed.

    num_cameras : int
        Number of camera_models detected.

    detected_cams_label : QLabel
        Label to display the number of detected camera_models.

    scroll_area : CameraList
        Widget to display the list of detected camera_models.

    search_button : QPushButton
        Button to initiate camera search.
    """

    # Signals to connect to slots
    search_button_pressed = Signal()

    def __init__(self):
        """
        Initializes the GUICamera widget with default values and sets up the user interface.
        """
        super().__init__()
        # Initial values
        self.num_cameras = 0

        # Camera GUI components
        self.detected_cams_label = QLabel(f'Number of detected camera_models: {self.num_cameras}')
        self.scroll_area = CameraList(self.num_cameras)
        self.search_button = QPushButton('Search camera_models')

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initializes and sets up the user interface components.

        Sets up the layout, adds widgets to it, and connects signals to slots.
        """
        layout = QVBoxLayout()

        # Label
        label = QLabel("--- Connected devices ---")
        layout.addWidget(label)

        # Detected camera_models
        self.detected_cams_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.detected_cams_label)

        # Camera list
        layout.addWidget(self.scroll_area)

        # Search button
        self.search_button.clicked.connect(self.on_search_button_clicked)
        layout.addWidget(self.search_button)

        # Set self layout
        self.setLayout(layout)

    def on_search_button_clicked(self) -> None:
        """
        Slot to handle the event when the search button is clicked.

        Emits the `search_button_pressed` signal.
        """
        self.search_button_pressed.emit()

    def reload(self, num_cameras: int, info: dict):
        """
        Reloads the camera list with new camera data.

        Parameters
        ----------
        num_cameras : int
            The number of detected camera_models.
        info : list
            List containing information about each camera.
        """
        self.num_cameras = num_cameras
        self.detected_cams_label.setText('Number of detected camera_models: ' + str(self.num_cameras))
        self.scroll_area.reload(num_cameras, info)

    def load_camera(self, index: int) -> None:
        """
        Sets the status of a camera to 'Loaded' and updates its GUI components.

        Parameters
        ----------
        index : int
            The index of the camera in the list.
        """
        camera_GUI = self.scroll_area.camera_boxes[index]
        camera_GUI.status = "Loaded"
        camera_GUI.load_button.hide()
        camera_GUI.view_button.show()
        camera_GUI.settings_button.show()
        camera_GUI.reload_button.show()
        camera_GUI.close_button.show()