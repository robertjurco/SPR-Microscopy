from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QComboBox, QPushButton, QFormLayout, QHBoxLayout

class CameraSettingsGUI(QWidget):
    def __init__(self, device_name, width, height, bitdepth):
        super().__init__()
        self.device_name = device_name
        self.width = width
        self.height = height
        self.bitdepth = bitdepth
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Settings label
        settings_label = QLabel('--- Settings ---')
        settings_label.setAlignment(Qt.AlignCenter)
        settings_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(settings_label)

        # Device name
        device_name_label = QLabel(f'Device: {self.device_name}')
        layout.addWidget(device_name_label)

        # Camera chip details
        chip_details_label = QLabel(f'Width: {self.width} px, Height: {self.height} px, Bit Depth: {self.bitdepth} bits')
        layout.addWidget(chip_details_label)

        # Exposure setting
        self.exposure_label = QLabel('Exposure (ms):')
        self.exposure_spinbox = QSpinBox()
        self.exposure_spinbox.setRange(1, 1000)
        self.exposure_spinbox.setValue(100)
        self.exposure_spinbox.valueChanged.connect(self.update_exposure)

        # Gain setting
        self.gain_label = QLabel('Gain:')
        self.gain_spinbox = QSpinBox()
        self.gain_spinbox.setRange(0, 100)
        self.gain_spinbox.setValue(10)
        self.gain_spinbox.valueChanged.connect(self.update_gain)

        # Frame rate setting
        self.frame_rate_label = QLabel('Frame Rate (fps):')
        self.frame_rate_spinbox = QSpinBox()
        self.frame_rate_spinbox.setRange(1, 120)
        self.frame_rate_spinbox.setValue(30)
        self.frame_rate_spinbox.valueChanged.connect(self.update_frame_rate)

        # Resolution setting
        self.resolution_label = QLabel('Resolution:')
        self.resolution_combobox = QComboBox()
        self.resolution_combobox.addItems(['640x480', '1280x720', '1920x1080'])
        self.resolution_combobox.currentIndexChanged.connect(self.update_resolution)

        # Apply button
        self.apply_button = QPushButton('Apply Settings')
        self.apply_button.clicked.connect(self.apply_settings)

        # Layout setup
        form_layout = QFormLayout()
        form_layout.addRow(self.exposure_label, self.exposure_spinbox)
        form_layout.addRow(self.gain_label, self.gain_spinbox)
        form_layout.addRow(self.frame_rate_label, self.frame_rate_spinbox)
        form_layout.addRow(self.resolution_label, self.resolution_combobox)


        layout.addLayout(form_layout)
        layout.addWidget(self.apply_button)


        layout.addStretch(1)

        self.setLayout(layout)

    def update_exposure(self, value):
        print(f'Exposure set to {value} ms')

    def update_gain(self, value):
        print(f'Gain set to {value}')

    def update_frame_rate(self, value):
        print(f'Frame rate set to {value} fps')

    def update_resolution(self, index):
        resolution = self.resolution_combobox.itemText(index)
        print(f'Resolution set to {resolution}')

    def apply_settings(self):
        exposure = self.exposure_spinbox.value()
        gain = self.gain_spinbox.value()
        frame_rate = self.frame_rate_spinbox.value()
        resolution = self.resolution_combobox.currentText()
        print(f'Applying settings: Exposure={exposure} ms, Gain={gain}, Frame Rate={frame_rate} fps, Resolution={resolution}')