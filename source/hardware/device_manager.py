import threading
from typing import Dict, Any

from PySide6.QtCore import QThread
from adodbapi import connect
from adodbapi.apibase import pythonTimeConverter
from numba.cuda.printimpl import print_item
from pypylon import pylon
import pylablib as pll
from pylablib.devices import Thorlabs, NKT
from scipy.sparse.csgraph import connected_components

import source.hardware.slms.EXULUS_COMMAND_LIB as ThorlabsExulus
from source.hardware.camera.camera import CameraWorker
from source.hardware.camera.camera_models.basler import Basler

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
    def __init__(self):
        self.threads: Dict[str, QThread] = {}
        self.thread_workers: Dict[str, ThreadWorker] = {}
        # Dictionary to store connected devices with serial number as key
        self.connected_devices: Dict[str, Dict[str, Any]] = {}
        # Dictionary to store loaded devices
        self.loaded_devices: Dict[str, Any] = {}
        # Dictionary to keep track of device threads
        self.device_threads: Dict[str, threading.Thread] = {}

    def auto_detect_devices(self):
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
                        'type': 'motion_control',
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

    def handle_button_signal(self, message: str, serial: str, device_type: str) -> None:
        """
        Handles button signals received with appropriate actions.

        Args:
            message (str): The message to process.
            serial (str): Serial number of the device.
            device_type (str): Type of the device.
        """
        if not self.is_device_connected(serial):
            print(f"Device with serial {serial} is not connected.")
            return

        if message == "Load":
            if self.is_device_loaded(serial):
                print(f"Device with serial {serial} is already loaded.")
                return
            self.load_device(serial, device_type)
        else:
            if not self.is_device_loaded(serial):
                print(f"Device with serial {serial} is not loaded.")
                return

            self.loaded_devices[serial].handle_message(message)

            match device_type:
                case "camera":
                    self.handle_camera_message(serial, message)
                case "motion_control":
                    self.handle_motion_message(serial, message)
                case "slm":
                    self.handle_slm_message(serial, message)

                # If an exact match is not confirmed, this last case will be used if provided
                case _:
                    print("Something's wrong with the message handling.")

    def handle_camera_message(self, serial, message):
        match message:
            case ("View" | "Play"):
                # Manage thread for the camera
                if serial not in self.threads:
                    thread = QThread()
                    self.threads[serial] = thread
                    self.thread_workers[serial] = ThreadWorker(self.loaded_devices[serial])
                    self.thread_workers[serial].moveToThread(thread)
                    thread.started.connect(self.thread_workers[serial].run)
                    thread.start()
                    print("New threat started")


    def handle_motion_message(self, serial, message):
        pass

    def handle_slm_message(self, serial, message):
        pass

    def load_device(self, serial: str, device_type: str) -> None:
        """
        Loads a device based on its type.

        Args:
            serial (str): Serial number of the device.
            device_type (str): Type of the device.
        """
        try:
            if device_type == "camera":
                print(f"Attempting to load device with serial {serial} as a camera.")
                self.loaded_devices[serial] = Basler(serial)
                if self.loaded_devices[serial] is not None:
                    print(f"Device with serial {serial} loaded successfully.")
                else:
                    print(f"Device with serial {serial} is not loaded.")
            else:
                print(f"Unsupported device type: {device_type}.")
        except Exception as e:
            print(f"Failed to load device with serial {serial}. Error: {e}")

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

    def send_message_to_device(self, serial: str, message: str) -> bool:
        """
        Placeholder method to send a message to a device.

        Args:
            serial (str): Serial number of the device.
            message (str): Message to be sent.

        Returns:
            bool: Success status.
        """
        # Implement actual message sending logic here
        return False