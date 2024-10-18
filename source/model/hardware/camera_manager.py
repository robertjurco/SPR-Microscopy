"""
This class will manage the connected cameras and provide methods to load and unload them.
It emits signals when cameras are connected or disconnected.
"""
from warnings import catch_warnings

from PySide6.QtCore import QObject, Signal, QThread, QThreadPool
from pypylon import pylon

from source.model.hardware.cameras.basler import Basler



# QObject is the base class for most Qt classes, enabling core functions
# like signals and slots through introspection. It supports introspection
# (awareness of class name, relationships, methods, and properties) and
# memory management (parent-child object ownership and destruction).
# Exceptions include value types like QColor, QString, and QList.
class CameraManager(QObject):
    """
    This class will manage the connected cameras and provide methods to load and unload them.
    It emits signals when cameras are connected or disconnected.
    """
    # Signals to connect to slots
    camera_connected = Signal(int)
    camera_disconnected = Signal(int)

    def __init__(self):
        super().__init__()

        self.connected_cameras = {}
        self.loaded_cameras = {}

    def detect_cameras(self):
        # Detect all connected cameras, add new cameras to connected list
        devices = pylon.TlFactory.GetInstance().EnumerateDevices()
        for i, device in enumerate(devices):
            if i not in self.connected_cameras:
                self.connected_cameras[i] = device
        return len(devices)

    def load_camera(self, camera_id):
        # Load camera and add it to loaded list
        if camera_id in self.connected_cameras and camera_id not in self.loaded_cameras:
            # Load new camera
            # TODO: Make loader general, not only for Basler.
            camera = Basler(camera_id)
            self.loaded_cameras[camera_id] = camera

    def close_camera(self, camera_id):
        # Close camera and remove it from loaded list
        if camera_id in self.loaded_cameras:
            self.loaded_cameras[camera_id].stop()
            self.loaded_cameras[camera_id].close()
            del self.loaded_cameras[camera_id]

    def get_all_cameras_info(self):
        info = {
            "connected": list(self.connected_cameras.keys()),
            "loaded": list(self.loaded_cameras.keys()),
            "names": {i: self.connected_cameras[i].GetFriendlyName() for i in self.connected_cameras}
        }
        return info

    def get_all_cameras_settings(self):
        info = {
            "name": {i: self.loaded_cameras[i].get_name() for i in self.loaded_cameras},
            "exposure": {i: self.loaded_cameras[i].get_exposure() for i in self.loaded_cameras},
            "width": {i: self.loaded_cameras[i].get_width() for i in self.loaded_cameras},
            "height": {i: self.loaded_cameras[i].get_height() for i in self.loaded_cameras},
            "bitdepth": {i: self.loaded_cameras[i].get_bitdepth() for i in self.loaded_cameras}
        }
        return info
