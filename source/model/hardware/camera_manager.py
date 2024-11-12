"""
This class will manage the connected cameras and provide methods to load and unload them.
It emits signals when cameras are connected or disconnected.
"""
from warnings import catch_warnings

from PySide6.QtCore import QObject, Signal, QThread, QThreadPool, Slot
from pypylon import pylon

from source.model.hardware.camera import CameraWorker
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
    frame_acquired_ = Signal(int, object)

    def __init__(self):
        super().__init__()

        self.threads = {}
        self.connected_cameras = {}
        self.loaded_cameras = {}
        self.cam_worker = {}

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
            print("Sucesfully connected")

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

    def get_camera_settings(self, i):
        return self.loaded_cameras[i].get_all_settings()

    def start_image_acquisition_camera(self, index):
        # Manage thread for the camera
        if index not in self.threads:
            thread = QThread()
            self.threads[index] = thread
            self.cam_worker[index] = CameraWorker(self.loaded_cameras[index])
            self.cam_worker[index].moveToThread(thread)
            thread.started.connect(self.cam_worker[index].run)
            thread.start()
            print("New threat started")

    @Slot(int, object)
    def frame_acquired_with_ID(self, idx, image):
        return idx, image