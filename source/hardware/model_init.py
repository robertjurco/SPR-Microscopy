from source.hardware.device_manager import DeviceManager

class Model:
    def __init__(self, logger):
        self.device_manager = DeviceManager(logger)

        #self.device_manager.auto_detect_devices()
        #print(self.device_manager.list_connected_devices())