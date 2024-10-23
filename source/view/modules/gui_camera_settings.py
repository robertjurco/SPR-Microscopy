from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QComboBox, QPushButton, QFormLayout, QHBoxLayout

class CameraSettingsGUI(QWidget):
    def __init__(self, Camera_Id):
        super().__init__()

        # Important -> Camera ID
        self.device_name = None
        self.camera_id = Camera_Id

        # Initialize camera settings
        # Camera settings
        self.width = None
        self.width_min = None
        self.width_max = None

        self.height = None
        self.height_min = None
        self.height_max = None

        self.bitdepth = None

        self.exposure = None
        self.exposure_min = None
        self.exposure_max = None

        self.gain = None
        self.gain_min = None
        self.gain_max = None

        self.frame_rate = None
        self.frame_rate_min = None
        self.frame_rate_max = None

        # Initialize components
        self.device_name_label = QLabel(f'Device:')

        self.width_label = QLabel('Width:')
        self.width_spinbox = QSpinBox()

        self.height_label = QLabel('Height:')
        self.height_spinbox = QSpinBox()

        self.bitdepth_label = QLabel('Bitdepth:')
        self.bitdepth_spinbox = QSpinBox()

        self.exposure_label = QLabel('Exposure (ms):')
        self.exposure_spinbox = QSpinBox()

        self.gain_label = QLabel('Gain:')
        self.gain_spinbox = QSpinBox()

        self.frame_rate_label = QLabel('Frame Rate (fps):')
        self.frame_rate_spinbox = QSpinBox()

        self.apply_button = QPushButton('Apply Settings')

        # Initialize GUI
        self.initUI()

        # Hide all till settings button is pressed
        self.hide_all()

    def initUI(self):
        layout = QVBoxLayout()

        # Settings label
        settings_label = QLabel('--- Settings ---')
        settings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(settings_label)

        # Device name
        layout.addWidget(self.device_name_label)

        # Width settings
        self.width_spinbox.setRange(1, 1000)
        self.width_spinbox.setValue(100)
        self.width_spinbox.valueChanged.connect(self.update_width)

        # Height settings
        self.height_spinbox.setRange(1, 1000)
        self.height_spinbox.setValue(100)
        self.height_spinbox.valueChanged.connect(self.update_height)

        # Bitdepth settings
        self.bitdepth_spinbox.setRange(1, 1000)
        self.bitdepth_spinbox.setValue(100)
        self.bitdepth_spinbox.valueChanged.connect(self.update_bitdepth)

        # Exposure setting
        self.exposure_spinbox.setRange(1, 1000)
        self.exposure_spinbox.setValue(100)
        self.exposure_spinbox.valueChanged.connect(self.update_exposure)

        # Gain setting
        self.gain_spinbox.setRange(0, 100)
        self.gain_spinbox.setValue(10)
        self.gain_spinbox.valueChanged.connect(self.update_gain)

        # Frame rate setting
        self.frame_rate_spinbox.setRange(1, 120)
        self.frame_rate_spinbox.setValue(30)
        self.frame_rate_spinbox.valueChanged.connect(self.update_frame_rate)

        # Apply button
        self.apply_button.clicked.connect(self.apply_camera_settings)

        # Layout setup
        form_layout = QFormLayout()
        form_layout.addRow(self.width_label, self.width_spinbox)
        form_layout.addRow(self.height_label, self.height_spinbox)
        form_layout.addRow(self.bitdepth_label, self.bitdepth_spinbox)
        form_layout.addRow(self.exposure_label, self.exposure_spinbox)
        form_layout.addRow(self.gain_label, self.gain_spinbox)
        form_layout.addRow(self.frame_rate_label, self.frame_rate_spinbox)

        layout.addLayout(form_layout)
        layout.addWidget(self.apply_button)


        layout.addStretch(1)

        self.setLayout(layout)

    def fetch_camera_settings(self, camera_id, settings):
        # Important -> Camera ID
        self.camera_id = camera_id

        # Camera settings
        self.device_name = settings['name']

        self.width = settings["width"]["value"]
        self.width_min = settings["width"]["min"]
        self.width_max = settings["width"]["max"]

        self.height = settings["height"]["value"]
        self.height_min = settings["height"]["min"]
        self.height_max = settings["height"]["max"]

        self.bitdepth = settings["bitdepth"]

        self.exposure = settings["exposure"]["value"]
        self.exposure_min = settings["exposure"]["min"]
        self.exposure_max = settings["exposure"]["max"]

        self.gain = settings["gain"]["value"]
        self.gain_min = settings["gain"]["min"]
        self.gain_max = settings["gain"]["max"]

        self.frame_rate = settings["frame_rate"]["value"]
        self.frame_rate_min = settings["frame_rate"]["min"]
        self.frame_rate_max = settings["frame_rate"]["max"]

        # Show settings of the corresponding camera
        self.show_all()
        self.update_GUI()

    def hide_all(self):
        self.width_label.hide()
        self.width_spinbox.hide()

        self.height_label.hide()
        self.height_spinbox.hide()

        self.bitdepth_label.hide()
        self.bitdepth_spinbox.hide()

        self.exposure_label.hide()
        self.exposure_spinbox.hide()

        self.gain_label.hide()
        self.gain_spinbox.hide()

        self.frame_rate_label.hide()
        self.frame_rate_spinbox.hide()


        self.apply_button.hide()

    def show_all(self):
        self.width_label.show()
        self.width_spinbox.show()

        self.height_label.show()
        self.height_spinbox.show()

        self.bitdepth_label.show()
        self.bitdepth_spinbox.show()

        self.exposure_label.show()
        self.exposure_spinbox.show()

        self.gain_label.show()
        self.gain_spinbox.show()

        self.frame_rate_label.show()
        self.frame_rate_spinbox.show()

        self.apply_button.show()

    ################################################## Update settings #################################################

    def update_width(self, value):
        self.width = value

    def update_height(self, value):
        self.height = value

    def update_bitdepth(self, value):
        self.bitdepth = value

    def update_exposure(self, value):
        self.exposure = value

    def update_gain(self, value):
        self.gain = value

    def update_frame_rate(self, value):
        self.frame_rate = value

    def apply_camera_settings(self):
        settings = {
            'width':  self.width,
            'height': self.height,
            'bitdepth': self.bitdepth,
            'exposure': self.exposure,
            'gain': self.gain,
            'frame_rate': self.frame_rate
        }

    #################################################### Update GUI ####################################################

    def update_GUI(self):
        self.device_name_label.setText(f'Device: {self.device_name}')

        # Width settings
        self.width_spinbox.setRange(self.width_min, self.width_max)
        self.width_spinbox.setValue(self.width)

        # Height settings
        self.height_spinbox.setRange(self.height_min, self.height_max)
        self.height_spinbox.setValue(self.height)

        # Bitdepth settings
        self.bitdepth_spinbox.setRange(self.bitdepth, self.bitdepth)
        self.bitdepth_spinbox.setValue(self.bitdepth)

        # Exposure setting
        self.exposure_spinbox.setRange(self.exposure_min, self.exposure_max)
        self.exposure_spinbox.setValue(self.exposure)

        # Gain setting
        self.gain_spinbox.setRange(self.gain_min, self.gain_max)
        self.gain_spinbox.setValue(self.gain)

        # Frame rate setting
        self.frame_rate_spinbox.setRange(self.frame_rate_min, self.frame_rate_max)
        self.frame_rate_spinbox.setValue(self.frame_rate)
