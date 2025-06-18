import threading
from typing import Dict, Any

from PySide6.QtCore import QThread
from pypylon import pylon
from pylablib.devices import Thorlabs

import source.hardware.slms.EXULUS_COMMAND_LIB as ThorlabsExulus
from source.hardware.camera.camera_models.basler import Basler
from source.hardware.motion_control.motion_control_models.thorlabs_kcube_KDC101 import KinesisMotor
from source.hardware.motion_control.motion_control_models.thorlabs_kcube_KSC101 import KinesisSolenoid

#from source.hardware.usb_helper import get_usb_devices_by_serial, get_usb_info

# Define a mapping of device types to their corresponding classes
DEVICE_CLASS_REGISTRY = {
    'camera': Basler,
    'k_cube_KDC': KinesisMotor,
    'k_cube_KSC': KinesisSolenoid
    # Add new device types here
    # 'motor': MotorDevice,
    # 'sensor': SensorDevice,
}


class ThreadWorker(QThread):

    def __init__(self, device):
        super().__init__()
        self.device = device
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.device.step()

    def stop(self):
        self.running = False

class DeviceManager:
    def __init__(self, logger):
        self.threads: Dict[str, QThread] = {}
        self.thread_workers: Dict[str, ThreadWorker] = {}
        # Dictionary to store connected devices with serial number as key
        self.connected_devices: Dict[str, Dict[str, Any]] = {}
        # Dictionary to store loaded devices
        self.loaded_devices: Dict[str, Any] = {}
        # Dictionary to keep track of device threads
        self.device_threads: Dict[str, threading.Thread] = {}
        # Dictionary to store USB devices with serial number as key
        self.usb_devices_info: Dict[str, Dict[str, Any]] = {}

        self.logger = logger

    def auto_detect_devices(self):
        #get_usb_info()
        #self.usb_devices_info = get_usb_info()
        #print(self.usb_devices_info)

        try:
            # Temporary set to track currently connected devices
            current_device_serials = set()

            # Detect cameras
            camera_devices = pylon.TlFactory.GetInstance().EnumerateDevices()
            for device in camera_devices:
                serial_number = device.GetSerialNumber()
                current_device_serials.add(serial_number)
                if serial_number not in self.connected_devices:
                    self.connected_devices[serial_number] = {
                        'name': 'Basler ' + device.GetModelName(),
                        'type': 'camera',
                        'status': 'connected'
                    }

            # Detect motion control devices
            motion_devices = Thorlabs.list_kinesis_devices()
            for serial_number, description in motion_devices:
                current_device_serials.add(serial_number)
                if serial_number not in self.connected_devices:
                    self.connected_devices[serial_number] = {
                        'name': description,
                        'type': 'k_cube',
                        'status': 'connected'
                    }

            # Detect SLM devices
            slm_devices = ThorlabsExulus.EXULUSListDevices()
            for device in slm_devices:
                serial_number = device[0]
                current_device_serials.add(serial_number)
                if serial_number not in self.connected_devices:
                    self.connected_devices[serial_number] = {
                        'name': device[1],
                        'type': 'slm',
                        'status': 'connected'
                    }

            # Remove devices from dict if not connected
            disconnected_devices = [serial for serial in self.connected_devices if serial not in current_device_serials]
            for serial in disconnected_devices:
                del self.connected_devices[serial]

            print(self.connected_devices)
            return len(self.connected_devices)
        except Exception as e:
            print(f"Error during device detection: {e}")
            return 0

    def list_connected_devices(self) -> Dict[str, Dict[str, Any]]:
        """
        Lists all the connected devices.

        Returns:
            dict: Dictionary of connected devices.
        """
        return self.connected_devices

    def load_device(self, serial: str) -> int:
        """
        Loads a device based on its type.

        Args:
            serial (str): Serial number of the device.

        Returns:
            int: 1 if device loaded successfully, 0 otherwise.
        """
        try:
            device_info = self.list_connected_devices().get(serial)
            if not device_info:
                self.logger.info(f"No device found with serial {serial}.")
                return 0

            device_type = device_info['type']
            device_class = DEVICE_CLASS_REGISTRY.get(device_type)

            if not device_class:
                self.logger.info(f"Unsupported device type: {device_type}.")
                return 0

            self.logger.info(f"Attempting to load device with serial {serial} as a {device_type}.")
            self.loaded_devices[serial] = device_class(serial)

            if self.loaded_devices[serial] is not None:
                self.logger.info(f"Device with serial {serial} loaded successfully.")
                return 1
            else:
                self.logger.info(f"Device with serial {serial} failed to load.")
                return 0

        except Exception as e:
            self.logger.error(f"Failed to load device with serial {serial}. Error: {e}")
            return 0

    def close_device(self, serial: str) -> bool:
        """
        Placeholder method to close a device.

        Args:
            serial (str): Serial number of the device.

        Returns:
            bool: Success status.
        """
        # Implement actual closing logic here
        return False

    def is_device_connected(self, serial: str) -> bool:
        """
        Checks if a device is connected.

        Args:
            serial (str): Serial number of the device.

        Returns:
            bool: True if connected, False otherwise.
        """
        return serial in self.connected_devices

    def is_device_loaded(self, serial: str) -> bool:
        """
        Checks if a device is loaded.

        Args:
            serial (str): Serial number of the device.

        Returns:
            bool: True if loaded, False otherwise.
        """
        return serial in self.loaded_devices

    def get_device_settings(self, serial: str) -> dict:
        if serial in self.loaded_devices:
            return self.loaded_devices[serial].get_all_settings()
        else:
            return "Device not loaded"


    def set_device_settings(self, serial: str, settings: dict):
        self.loaded_devices[serial].set_all_settings(settings)

