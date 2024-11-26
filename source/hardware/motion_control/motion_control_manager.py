from PySide6.QtCore import Signal
from pylablib.devices import Thorlabs

from source.model.device_manager import DeviceManager
from source.model.motion_control.motion_control import MotionControl


class MotionControlManager(DeviceManager):
    """
    Class for managing connected motion control devices.
    This class extends DeviceManager to provide specific implementations
    for detecting, loading, and closing motion control devices.
    Attributes:
        frame_acquired (Signal): Signal emitted when a frame is acquired.
        threads (dict): Dictionary to store threads for device workers.
        device_workers (dict): Dictionary to store device worker instances.
    """
    frame_acquired = Signal(int, object)

    def __init__(self):
        """
        Initialize the MotionControlManager.
        """
        super().__init__()
        self.threads = {}
        self.device_workers = {}

        self.connected_devices = {}
        self.loaded_devices = {}

    def detect_devices(self):
        """
        Detect all connected camera devices and add new devices to the connected list.
        Returns:
            int: Number of connected devices.
        """
        devices = Thorlabs.list_kinesis_devices()

        for device in devices:
            serial_number, device_type = device  # unpack the tuple
            if serial_number not in self.connected_devices:
                self.connected_devices[serial_number] = device

        return len(devices)

    def load_devices(self, serial_number):
        """
            Load a specific camera device and add it to the loaded list.
            Args:
                serial_number (int): The ID of the camera device to be loaded.
            Returns:
                bool: True if the device was successfully loaded, False otherwise.
            """
        if serial_number in self.connected_devices and serial_number not in self.loaded_devices:
            try:
                device = MotionControl(serial_number)
                self.loaded_devices[serial_number] = device
                print(f"Successfully connected to device {serial_number}.")  # Prefer using logging or emit a signal
                return True
            except Exception as e:
                print(f"Failed to connect to device {serial_number}: {e}")  # Prefer using logging or emit a signal
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
            if device_id in self.device_workers:
                self.device_workers[device_id].stop()
                self.device_workers[device_id].wait()  # Wait for the thread to finish
                del self.device_workers[device_id]

            # Close the camera
            self.loaded_devices[device_id].close()
            del self.loaded_devices[device_id]

            # Stop and delete the thread
            if device_id in self.threads:
                self.threads[device_id].quit()  # Request the thread to quit
                self.threads[device_id].wait()  # Wait for the thread to finish
                del self.threads[device_id]

    def get_all_devices_info(self):
        info = {
            "connected": list(self.connected_devices.keys()),
            "loaded": list(self.loaded_devices.keys()),
            "names": {i: self.connected_devices[i].description for i in self.connected_devices}
        }
        return info

    def get_device_settings(self, i):
        return self.loaded_devices[i].get_all_settings()
