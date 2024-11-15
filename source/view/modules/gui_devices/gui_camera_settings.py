from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QFormLayout


class CameraSettingsGUI(QWidget):
    """
    GUI for displaying and modifying camera settings.
    """
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 100
    DEFAULT_BITDEPTH = 100
    DEFAULT_EXPOSURE = 100
    DEFAULT_GAIN = 10
    DEFAULT_FRAME_RATE = 30

    settings_applied = Signal(dict)  # Signal for settings applied

    def __init__(self, Camera_Id: int):
        """
        Constructs the CameraSettingsGUI with the specified Camera ID.

        :param Camera_Id: The ID of the camera.
        """
        super().__init__()
        self.device_name = None
        self.camera_id = Camera_Id

        # Initialize camera settings
        self.camera_settings = {
            'width': None,
            'width_min': None,
            'width_max': None,
            'height': None,
            'height_min': None,
            'height_max': None,
            'bitdepth': None,
            'exposure': None,
            'exposure_min': None,
            'exposure_max': None,
            'gain': None,
            'gain_min': None,
            'gain_max': None,
            'frame_rate': None,
            'frame_rate_min': None,
            'frame_rate_max': None,
        }

        # Initialize GUI components
        self.init_ui()

        # Hide all widgets initially
        self.hide_all()

    def init_ui(self) -> None:
        """
        Initialize the user interface components.
        """
        layout = QVBoxLayout()

        settings_label = QLabel('--- Settings ---')
        settings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(settings_label)

        self.device_name_label = QLabel('Device:')
        layout.addWidget(self.device_name_label)

        form_layout = QFormLayout()

        self.width_label, self.width_spinbox = self.create_spinbox('Width:', self.DEFAULT_WIDTH, form_layout)
        self.height_label, self.height_spinbox = self.create_spinbox('Height:', self.DEFAULT_HEIGHT, form_layout)
        self.bitdepth_label, self.bitdepth_spinbox = self.create_spinbox('Bitdepth:', self.DEFAULT_BITDEPTH,
                                                                         form_layout)
        self.exposure_label, self.exposure_spinbox = self.create_spinbox('Exposure (ms):', self.DEFAULT_EXPOSURE,
                                                                         form_layout)
        self.gain_label, self.gain_spinbox = self.create_spinbox('Gain:', self.DEFAULT_GAIN, form_layout)
        self.frame_rate_label, self.frame_rate_spinbox = self.create_spinbox('Frame Rate (fps):',
                                                                             self.DEFAULT_FRAME_RATE, form_layout)

        self.apply_button = QPushButton('Apply Settings')
        self.apply_button.clicked.connect(self.apply_camera_settings)

        layout.addLayout(form_layout)
        layout.addWidget(self.apply_button)
        layout.addStretch()

        self.setLayout(layout)

    def create_spinbox(self, label: str, default_value: int, layout: QFormLayout):
        """
        Creates a labeled QSpinBox and adds it to the specified layout.

        :param label: The label text.
        :param default_value: The default value of the spinbox.
        :param layout: The layout to add the widgets to.
        :return: Tuple containing the label widget and spinbox widget.
        """
        label_widget = QLabel(label)
        spinbox = QSpinBox()
        spinbox.setRange(1, 1000)
        spinbox.setValue(default_value)
        spinbox.valueChanged.connect(self.update_setting_value(label.lower()))
        layout.addRow(label_widget, spinbox)
        return label_widget, spinbox

    def update_setting_value(self, setting_name: str):
        """
        Returns a function to update the setting value in the camera_settings dictionary.

        :param setting_name: The key for the setting to update.
        :return: Function that updates the setting value.
        """

        def updater(value: int):
            self.camera_settings[setting_name] = value

        return updater

    def fetch_camera_settings(self, camera_id: int, settings: dict) -> None:
        """
        Fetch and apply settings for a camera.

        :param camera_id: The ID of the camera.
        :param settings: The settings dictionary for the camera.
        """
        self.camera_id = camera_id
        self.device_name = settings['name']
        for key in self.camera_settings.keys():
            self.camera_settings[key] = settings.get(key, None)

        self.show_all()
        self.update_gui()

    def hide_all(self) -> None:
        """
        Hides all the GUI components.
        """
        for label, widget in self.get_all_widgets():
            label.hide()
            widget.hide()
        self.apply_button.hide()

    def show_all(self) -> None:
        """
        Shows all the GUI components.
        """
        for label, widget in self.get_all_widgets():
            label.show()
            widget.show()
        self.apply_button.show()

    def get_all_widgets(self):
        """
        Returns a list of tuples containing all the label and spinbox pairs.

        :return: List of tuples (label, spinbox)
        """
        return [
            (self.width_label, self.width_spinbox),
            (self.height_label, self.height_spinbox),
            (self.bitdepth_label, self.bitdepth_spinbox),
            (self.exposure_label, self.exposure_spinbox),
            (self.gain_label, self.gain_spinbox),
            (self.frame_rate_label, self.frame_rate_spinbox)
        ]

    def apply_camera_settings(self) -> None:
        """
        Emits a signal with the current camera settings when the apply button is clicked.
        """
        settings = {key: self.camera_settings[key] for key in self.camera_settings if
                    self.camera_settings[key] is not None}
        self.settings_applied.emit(settings)

    def update_gui(self) -> None:
        """
        Updates the GUI to display the current camera settings.
        """
        self.device_name_label.setText(f'Device: {self.device_name}')

        self.width_spinbox.setRange(self.camera_settings['width_min'], self.camera_settings['width_max'])
        self.width_spinbox.setValue(self.camera_settings['width'])

        self.height_spinbox.setRange(self.camera_settings['height_min'], self.camera_settings['height_max'])
        self.height_spinbox.setValue(self.camera_settings['height'])

        self.bitdepth_spinbox.setRange(self.camera_settings['bitdepth'], self.camera_settings['bitdepth'])
        self.bitdepth_spinbox.setValue(self.camera_settings['bitdepth'])

        self.exposure_spinbox.setRange(self.camera_settings['exposure_min'], self.camera_settings['exposure_max'])
        self.exposure_spinbox.setValue(self.camera_settings['exposure'])

        self.gain_spinbox.setRange(self.camera_settings['gain_min'], self.camera_settings['gain_max'])
        self.gain_spinbox.setValue(self.camera_settings['gain'])

        self.frame_rate_spinbox.setRange(self.camera_settings['frame_rate_min'], self.camera_settings['frame_rate_max'])
        self.frame_rate_spinbox.setValue(self.camera_settings['frame_rate'])