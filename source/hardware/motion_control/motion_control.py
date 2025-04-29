from PyQt5.QtCore import QObject


class MotionControl(QObject):

    def __init__(self, serial):
        super().__init__()
        self.running = False  # Is device running?

    def close(self):
        """Closes the .... connection and deletes related objects.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def reset(self):
        """Resets the .... to a default state.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

