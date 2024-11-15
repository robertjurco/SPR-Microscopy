from source.model.hardware.camera.camera_manager import CameraManager
from source.model.hardware.motion_control.motion_control_manager import MotionControlManager


class Model:
    def __init__(self):
        self.camera_manager = CameraManager()
        self.motion_control_manager = MotionControlManager()