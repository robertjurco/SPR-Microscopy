from PySide6.QtCore import Signal
from PySide6.QtGui import QImage

from source.controller.settings.controller_settings_camera import CameraSettingsController
from source.view.settings.view_settings_camera import ViewCameraSettings


class StartUpWindowController:
    new_frame_signal = Signal(QImage)  # Signal to send frame

    def __init__(self, model, view, threadpool):
        self.threads = {}
        self.model = model
        self.view = view
        self.threadpool = threadpool

        # Connected devices
        self.connected_devices = self.model.device_manager.list_connected_devices()

        # Connect signals to slots
        self.view.device_activate_click.connect(self.on_device_activated)
        self.view.on_settings_clicked.connect(self.open_settings_window)


        # On initialization detect camera_models send reload gui
        self.reload_devices()

    def reload_devices(self):
        self.model.device_manager.auto_detect_devices()
        self.connected_devices = self.model.device_manager.list_connected_devices()

        self.view.reload(self.connected_devices)

    def on_device_activated(self, serial: str):
        """
        Slot that will handle the signal when a device is activated.
        This will be called when the device_activated signal is emitted.

        Args:
            serial (str): The serial number of the activated device.
        """
        result = self.model.device_manager.load_device(serial)
        self.view.activation_response(serial, result)

    def open_settings_window(self, serial):
        # Create a runnable instance for CameraSettingsController
        CameraSettingsController(self.model, self.view, serial)