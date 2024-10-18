from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy


class CameraBox(QWidget):

    # Signals to connect to slots
    load_button_pressed = Signal()
    view_button_pressed = Signal()
    settings_button_pressed = Signal()
    reload_button_pressed = Signal()
    close_button_pressed = Signal()

    def __init__(self, name, status):
        super().__init__()

        # Buttons
        self.reload_button = None
        self.settings_button = None
        self.view_button = None
        self.close_button = None
        self.load_button = None

        # Class properties
        self.setObjectName("CameraBox")
        self.name = name
        self.status = status

        # Init UI
        self.initUI(name)

    def initUI(self, name):

        layout = QVBoxLayout()

        # Camera name, Id, ...
        label = QLabel(name)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        # Add camera buttons
        button_layout = QHBoxLayout()

        self.load_button = QPushButton('Load')
        self.load_button.clicked.connect(self.on_load_button_pressed)
        button_layout.addWidget(self.load_button)

        self.view_button = QPushButton('View')
        self.view_button.clicked.connect(self.on_view_button_pressed)
        button_layout.addWidget(self.view_button)

        self.settings_button = QPushButton('Settings')
        self.settings_button.clicked.connect(self.on_settings_button_pressed)
        button_layout.addWidget(self.settings_button)

        self.reload_button = QPushButton('Reload')
        self.reload_button.clicked.connect(self.on_reload_button_pressed)
        button_layout.addWidget(self.reload_button)

        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.on_close_button_pressed)
        button_layout.addWidget(self.close_button)

        # Set button status
        if self.status == "Loaded":
            self.load_button.hide()
        else:
            self.view_button.hide()
            self.settings_button.hide()
            self.reload_button.hide()
            self.close_button.hide()

        # Set layout
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def on_load_button_pressed(self):
        self.load_button_pressed.emit()

    def on_view_button_pressed(self):
        self.view_button_pressed.emit()

    def on_settings_button_pressed(self):
        self.settings_button_pressed.emit()

    def on_reload_button_pressed(self):
        self.reload_button_pressed.emit()

    def on_close_button_pressed(self):
        self.close_button_pressed.emit()

class CameraList(QScrollArea):
    def __init__(self, num_cameras):
        super().__init__()

        # Prepare QWidget and it's layout
        self.content_widget = None
        self.content_layout = None
        self.camera_boxes = []

        # Init UI
        self.initUI(num_cameras)

    def reload(self, num_cameras, info):
        # Clear existing widgets
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # clear camera boxes
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

    def initUI(self, num_cameras):
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)


        # Add multiple CameraBox widgets
        self.reload(0, "")

        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)

class GUICamera(QWidget):
    # Signals to connect to slots
    search_button_pressed = Signal()

    def __init__(self):
        super().__init__()
        # Initial values
        self.num_cameras = 0

        # Camera GUI components
        self.detected_cams_label = QLabel('Number of detected cameras: ' + str(self.num_cameras))
        self.scroll_area = CameraList(self.num_cameras)
        self.search_button = QPushButton('Search cameras')

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label
        label = QLabel("--- Connected devices ---")
        layout.addWidget(label)

        # Detected cameras
        self.detected_cams_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.detected_cams_label)

        # Camera list
        layout.addWidget(self.scroll_area)

        # Search search_button
        self.search_button.clicked.connect(self.on_search_button_clicked)
        layout.addWidget(self.search_button)

        # Set self layout
        self.setLayout(layout)

    def on_search_button_clicked(self):
        self.search_button_pressed.emit()

    def reload(self, num_cameras, info):
        self.num_cameras = num_cameras
        self.detected_cams_label.setText('Number of detected cameras: ' + str(self.num_cameras))
        self.scroll_area.reload(num_cameras, info)

    def load_camera(self, index):
        camera_GUI = self.scroll_area.camera_boxes[index]

        camera_GUI.status = "Loaded"

        camera_GUI.load_button.hide()
        camera_GUI.view_button.show()
        camera_GUI.settings_button.show()
        camera_GUI.reload_button.show()
        camera_GUI.close_button.show()