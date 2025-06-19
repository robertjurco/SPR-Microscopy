from PySide6.QtCore import Signal
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QMessageBox, QPushButton, QListWidget, QLabel, QVBoxLayout, QDialog

from source.controller.projects.controller_camera_FPS import CameraFPSController
from source.controller.projects.controller_camera_noise import CameraNoiseController
from source.controller.settings.controller_settings_camera import CameraSettingsController
from source.view.tabs.view_camera_FPS import CameraFPSView
from source.view.tabs.view_camera_noise import CameraNoiseView
from source.view.tabs.view_imaging import ImagingView


class StartUpWindowController:
    new_frame_signal = Signal(QImage)  # Signal to send frame

    def __init__(self, model, view, logger, threadpool):
        self.threads = {}
        self.model = model
        self.view = view
        self.threadpool = threadpool
        self.logger = logger

        # Connected devices
        self.connected_devices = self.model.device_manager.list_connected_devices()

        # Connect signals to slots
        self.view.device_activate_click.connect(self.on_device_activated)
        self.view.on_settings_clicked.connect(self.open_settings_window)
        self.view.new_project.connect(self.new_project)
        self.logger.update.connect(self.view.add_log)

        # On initialization detect camera_models send reload gui
        self.reload_devices()

    def reload_devices(self):
        self.model.device_manager.auto_detect_devices()
        self.connected_devices = self.model.device_manager.list_connected_devices()

        self.view.reload_tab_Available_Devices(self.connected_devices)

    def on_device_activated(self, serial: str, already_active: bool):
        """
        Slot that will handle the signal when a device is activated.
        This will be called when the device_activated signal is emitted.

        Args:
            serial (str): The serial number of the activated device.
        """
        if not already_active:
            result = self.model.device_manager.load_device(serial)
            self.view.activation_response(serial, result)
        else:
            result = self.model.device_manager.close_device(serial)
            self.view.activation_response(serial, result)

    def open_settings_window(self, serial):
        # Get the type of the device
        connected_devices = self.model.device_manager.list_connected_devices()
        device_type = connected_devices[serial]['type']

        # Create a runnable instance for SettingsController
        match  device_type:
            case 'camera':
                camera_settings_controller = CameraSettingsController(self.model, self.view, serial)
            case 'k_cube':
                k_cube_settings_controller = CameraSettingsController(self.model, self.view, serial)

    def new_project(self, project_type: str):
        match project_type:
            case "Imaging":
                self.imaging_view = ImagingView()
                self.imaging_view.show()
            case "Spectroscopy":
                pass
            case "Camera_FPS_meter":
                self.camera_FPS_view = CameraFPSView()
                self.camera_FPS_view.show()
                self.camera_FPS_controller = CameraFPSController(self.model, self.camera_FPS_view)
            case "Camera_noise":
                dialog = CameraSelectorDialog(self.model)
                if dialog.exec() == QDialog.Accepted:
                    selected_serial = dialog.get_selected_serial()

                    camera = self.model.device_manager.loaded_devices[selected_serial]
                    width = camera.get_width_min_max()[1]
                    height = camera.get_height_min_max()[1]
                    camera.set_width(width)
                    camera.set_height(height)
                    camera.set_bitdepth(12)

                    self.camera_noise_view = CameraNoiseView(width, height)
                    self.camera_noise_view.show()
                    self.camera_noise_view.show()
                    self.camera_noise_controller = CameraNoiseController(self.model, self.camera_noise_view,
                                                                         serial=selected_serial)

                else:
                    print("Camera selection canceled.")

            case "SLM":
                pass

    def select_camera(self):
        dialog = CameraSelectorDialog(self.model, self)
        if dialog.exec() == QDialog.Accepted:
            self.selected_camera_serial = dialog.get_selected_serial()
            print("Selected camera serial:", self.selected_camera_serial)
        else:
            print("Camera selection cancelled.")

class CameraSelectorDialog(QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Camera")
        self.setModal(True)
        self.setMinimumSize(300, 200)

        self.model = model
        self.selected_serial = None

        self._setup_ui()
        self._populate_camera_list()

    def _setup_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Select camera:")
        self.device_list = QListWidget()

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self._on_ok_clicked)

        layout.addWidget(label)
        layout.addWidget(self.device_list)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def _populate_camera_list(self):
        connected_devices = self.model.device_manager.list_connected_devices()
        for serial, info in connected_devices.items():
            device_type = info.get('type', None)
            if device_type == 'camera' and self.model.device_manager.is_device_loaded(serial):
                self.device_list.addItem(serial)

    def _on_ok_clicked(self):
        selected_items = self.device_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a camera.")
            return

        self.selected_serial = selected_items[0].text()
        self.accept()  # Close dialog and return success

    def get_selected_serial(self):
        return self.selected_serial