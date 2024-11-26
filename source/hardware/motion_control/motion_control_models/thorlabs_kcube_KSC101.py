from source.model.motion_control.motion_control import MotionControl


class KinesisSolenoid(MotionControl):
    def __init__(self, serial_number, settings=None):
        super().__init__(serial_number, 'Kinesis Solenoid', settings)
        self.state = 'closed'

    def open_solenoid(self):
        """
        Open the solenoid.
        """
        if not self.loaded:
            logging.error("Device not loaded. Cannot open solenoid.")
            return

        self.state = 'open'
        logging.info(f"Opened solenoid {self.serial_number}")

    def close_solenoid(self):
        """
        Close the solenoid.
        """
        if not self.loaded:
            logging.error("Device not loaded. Cannot close solenoid.")
            return

        self.state = 'closed'
        logging.info(f"Closed solenoid {self.serial_number}")

