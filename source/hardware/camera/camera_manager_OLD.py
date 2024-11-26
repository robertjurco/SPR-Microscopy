"""
This class will manage the connected camera_models and provide methods to load and unload them.
It emits signals when camera_models are connected or disconnected.
"""

from PySide6.QtCore import Signal, QThread, Slot
from pypylon import pylon

from source.model.camera.camera import CameraWorker
from source.model.camera.camera_models.basler import Basler
from source.model.device_manager import DeviceManager


class CameraManager(DeviceManager):
    """
    Class for managing connected cameras.

    This class extends DeviceManager to provide specific implementations
    for detecting, loading, and closing camera devices. It also manages
    the acquisition of images from the cameras.

    Attributes:
        frame_acquired (Signal): Signal emitted when a frame is acquired.
        threads (dict): Dictionary to store threads for camera workers.
        cam_workers (dict): Dictionary to store camera worker instances.
    """
    frame_acquired = Signal(int, object)

    def __init__(self):
        """
        Initialize the CameraManager.
        """
        super().__init__()
        self.threads = {}
        self.cam_workers = {}
        self.connected_devices = {}
        self.loaded_devices = {}

    def detect_devices(self):
        """
        Detect all connected camera devices and add new devices to the connected list.

        Returns:
            int: Number of connected devices.
        """
        devices = pylon.TlFactory.GetInstance().EnumerateDevices()
        for i, device in enumerate(devices):
            if i not in self.connected_devices:
                self.connected_devices[i] = device
        return len(devices)

    def load_devices(self, device_id):
        """
            Load a specific camera device and add it to the loaded list.
            Args:
                device_id (int): The ID of the camera device to be loaded.
            Returns:
                bool: True if the device was successfully loaded, False otherwise.
            """
        if device_id in self.connected_devices and device_id not in self.loaded_devices:
            try:
                camera = Basler(device_id)
                self.loaded_devices[device_id] = camera
                print(f"Successfully connected to device {device_id}.")  # Prefer using logging or emit a signal
                return True
            except Exception as e:
                print(f"Failed to connect to device {device_id}: {e}")  # Prefer using logging or emit a signal
                return False
        return False

    def close_device(self, device_id):
        """
        Close a specific camera device and remove it from the loaded list.

        Args:
            device_id (int): The ID of the camera device to be closed.
        """
        # Close camera and remove it from loaded list
        if device_id in self.loaded_devices:
            # Stop the camera worker
            if device_id in self.cam_workers:
                self.cam_workers[device_id].stop()
                self.cam_workers[device_id].wait()  # Wait for the thread to finish
                del self.cam_workers[device_id]

            # Close the camera
            self.loaded_devices[device_id].close()
            del self.loaded_devices[device_id]

            # Stop and delete the thread
            if device_id in self.threads:
                self.threads[device_id].quit()  # Request the thread to quit
                self.threads[device_id].wait()  # Wait for the thread to finish
                del self.threads[device_id]

    def get_all_cameras_info(self):
        info = {
            "connected": list(self.connected_devices.keys()),
            "loaded": list(self.loaded_devices.keys()),
            "names": {i: self.connected_devices[i].GetFriendlyName() for i in self.connected_devices}
        }
        return info

    def get_device_settings(self, i):
        return self.loaded_devices[i].get_all_settings()

    def start_image_acquisition_camera(self, index):
        # Manage thread for the camera
        if index not in self.threads:
            thread = QThread()
            self.threads[index] = thread
            self.cam_workers[index] = CameraWorker(self.loaded_devices[index])
            self.cam_workers[index].moveToThread(thread)
            thread.started.connect(self.cam_workers[index].run)
            thread.start()
            print("New threat started")

    @Slot(int, object)
    def frame_acquired_with_ID(self, idx, image):
        return idx, image