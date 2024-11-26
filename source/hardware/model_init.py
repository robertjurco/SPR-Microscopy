from source.hardware.device_manager import DeviceManager

class Model:
    def __init__(self):
        self.device_manager = DeviceManager()

        #self.device_manager.auto_detect_devices()
        #print(self.device_manager.list_connected_devices())