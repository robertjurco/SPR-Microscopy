from source.hardware.motion_control.motion_control import MotionControl


class KinesisMotor(MotionControl):
    def __init__(self, serial_number, settings=None):
        super().__init__(serial_number, 'Kinesis Motor', settings)
        self.position = 0

    def move_to(self, position):
        """
        Move the motor to a specified position.
        Args:
            position (int): The target position to move the motor to.
        """
        if not self.loaded:
            logging.error("Device not loaded. Cannot move motor.")
            return

        if position < self.settings.get('min_position', 0) or position > self.settings.get('max_position', 100):
            logging.error(f"Position {position} is out of bounds.")
            return

        self.position = position
        logging.info(f"Moved motor {self.serial_number} to position {self.position}")

    def set_speed(self, speed):
        """
        Set the speed of the motor.
        Args:
            speed (int): The speed to set the motor to.
        """
        self.settings['speed'] = speed
        logging.info(f"Set speed of motor {self.serial_number} to {speed}")
