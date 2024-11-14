from PySide6.QtCore import QObject, Signal


class DeviceManager(QObject):
    """
    Abstract base class for managing connected devices.

    This class provides a template for device management, including
    detecting, loading, and closing devices. Subclasses must
    implement the abstract methods to handle specific device types.

    Attributes:
        device_connected (Signal): Signal emitted when a device is connected.
        device_disconnected (Signal): Signal emitted when a device is disconnected.
        connected_devices (dict): Dictionary to store connected devices.
        loaded_devices (dict): Dictionary to store loaded devices.
    """
    device_connected = Signal(int)
    device_disconnected = Signal(int)

    def __init__(self):
        """
        Initialize the DeviceManager.
        """
        super().__init__()
        self.connected_devices = {}
        self.loaded_devices = {}

    def detect_devices(self):
        """
        Detect all connected devices and add new devices to the connected list.

        Returns:
            int: Number of connected devices.
        """
        raise NotImplementedError()

    def load_device(self, device_id):
        """
        Load a specific device and add it to the loaded list.

        Args:
            device_id (int): The ID of the device to be loaded.
        """
        raise NotImplementedError()

    def close_device(self, device_id):
        """
        Close a specific device and remove it from the loaded list.

        Args:
            device_id (int): The ID of the device to be closed.
        """
        raise NotImplementedError()

    def get_device_settings(self, device_id):
        """
        Get settings for a specific device.

        Args:
            device_id (int): The ID of the device to get settings for.

        Returns:
            dict: A dictionary containing the device settings.
        """
        raise NotImplementedError()

    def get_all_devices_info(self):
        """
        Get information about all connected and loaded devices.

        Returns:
            dict: A dictionary containing lists of connected and loaded device IDs.
        """
        return {
            "connected": list(self.connected_devices.keys()),
            "loaded": list(self.loaded_devices.keys())
        }