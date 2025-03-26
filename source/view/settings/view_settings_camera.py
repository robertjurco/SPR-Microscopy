from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QFormLayout, QDialog, QHBoxLayout, \
    QSizePolicy, QLayout


class ImageDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1000.0 / 60)  # 60 FPS
        self.current_image = None
        self.qimage = None  # Reusable QImage instance

    def update_image(self):
        if self.current_image is not None:
            # Check if the image is grayscale
            if len(self.current_image.shape) == 2:  # Grayscale image
                height, width = self.current_image.shape
                bytes_per_line = width  # One byte per pixel for grayscale
                qimage = QImage(self.current_image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
                self.label.setPixmap(QPixmap.fromImage(qimage))
            elif len(self.current_image.shape) == 3:  # Color image
                height, width, channel = self.current_image.shape
                bytes_per_line = channel * width

                if channel == 3:  # Assuming RGB
                    qimage = QImage(self.current_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                    self.label.setPixmap(QPixmap.fromImage(qimage))
                else:
                    print("Unsupported channel count.")
                    return
            else:
                print("Invalid image shape:", self.current_image.shape)

    def set_image(self, image):
        self.current_image = image
        self.update_image()

    def set_image_from_file(self, file_path):
        pixmap = QPixmap(file_path)
        self.label.setPixmap(pixmap)


class ViewCameraSettings(QWidget):
    """
    GUI for displaying and modifying camera settings.
    """

    settings_applied = Signal(dict)  # Signal for settings applied

    def __init__(self, serial: str, settings: dict):
        """
                Constructs the CameraSettingsGUI with the specified Camera ID.

                :param Camera_Id: The ID of the camera.
                """
        super().__init__()
        self.device_name = None
        self.serial = serial

        # Initialize GUI components
        # Main layout
        main_layout = QHBoxLayout()  # Use QHBoxLayout to align widgets horizontally

        self.settings_widget = SettingsWidget(serial, settings)
        self.image_display = ImageDisplay()
        self.image_display.set_image_from_file('C:/Users/jurco/Desktop/images.png')

        # Add widgets to the main layout
        main_layout.addWidget(self.settings_widget)
        main_layout.addWidget(self.image_display)
        self.setLayout(main_layout)

        # Set initial values
        self.settings_widget.update_camera_settings(settings)

        # Hide all widgets initially
        # self.hide_all()

    def update_frame(self, image):
        self.image_display.set_image(image)

class SettingsWidget(QWidget):
    """
    GUI for displaying and modifying camera settings.
    """
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 100
    DEFAULT_BITDEPTH = 100
    DEFAULT_EXPOSURE = 100
    DEFAULT_GAIN = 10
    DEFAULT_FRAME_RATE = 30

    settings_applied = Signal(dict)

    def __init__(self, serial: str, settings: dict):
        """
        Constructs the CameraSettingsGUI with the specified Camera ID.

        :param Camera_Id: The ID of the camera.
        """
        super().__init__()
        self.device_name = None
        self.serial = serial

        # Initialize camera settings
        self.camera_settings = None

        self.init_ui()

        # Set initial values
        self.update_camera_settings(settings)



    def init_ui(self):
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
        label_range_widget = QLabel(str(default_value))
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

    def update_camera_settings(self, settings: dict) -> None:
        """
        Update settings for a camera.

        :param camera_id: The ID of the camera.
        :param settings: The settings dictionary for the camera.
        """
        self.camera_settings = settings

        self.show_all()
        self.update_gui()

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
        settings = self.get_camera_settings()
        self.settings_applied.emit(settings)

    def update_gui(self) -> None:
        """
        Updates the GUI to display the current camera settings.
        """
        self.device_name_label.setText(f'Device: {self.device_name}')

        self.width_spinbox.setRange(self.camera_settings['width']['min'], self.camera_settings['width']['max'])
        self.width_spinbox.setValue(self.camera_settings['width']['value'])

        self.height_spinbox.setRange(self.camera_settings['height']['min'], self.camera_settings['height']['max'])
        self.height_spinbox.setValue(self.camera_settings['height']['value'])

        self.bitdepth_spinbox.setRange(self.camera_settings['bitdepth'], self.camera_settings['bitdepth'])
        self.bitdepth_spinbox.setValue(self.camera_settings['bitdepth'])

        self.exposure_spinbox.setRange(self.camera_settings['exposure']['min'], self.camera_settings['exposure']['max'])
        self.exposure_spinbox.setValue(self.camera_settings['exposure']['value'])

        self.gain_spinbox.setRange(self.camera_settings['gain']['min'], self.camera_settings['gain']['max'])
        self.gain_spinbox.setValue(self.camera_settings['gain']['value'])

        self.frame_rate_spinbox.setRange(self.camera_settings['frame_rate']['min'], self.camera_settings['frame_rate']['max'])
        self.frame_rate_spinbox.setValue(self.camera_settings['frame_rate']['value'])

    def get_camera_settings(self) -> dict:
        """
        Returns a dictionary containing the current camera settings.
        """
        self.camera_settings['width']['value'] = self.width_spinbox.value()
        self.camera_settings['height']['value'] = self.height_spinbox.value()
        self.camera_settings['bitdepth'] = self.bitdepth_spinbox.value()
        self.camera_settings['exposure']['value'] = self.exposure_spinbox.value()
        self.camera_settings['gain']['value'] = self.gain_spinbox.value()
        self.camera_settings['frame_rate']['value'] = self.frame_rate_spinbox.value()

        return self.camera_settings