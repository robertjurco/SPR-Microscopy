"""
Abstract camera functionality.
"""
import traceback

from PySide6.QtCore import QRunnable, QObject, Signal

class Camera():
    """
    Abstract class for cameras.
    """
    def __init__(self, width, height, bitdepth):
        super().__init__()

        # Unchangeable parameters
        self.width = width
        self.height = height
        self.bitdepth = bitdepth

        # Is camera running?
        self.running = False

    def close(self):
        """
        Abstract method to close the camera and delete related objects.
        """
        raise NotImplementedError()

    def reset(self):
        """
        Abstract method to reset the camera to a default state.
        """
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def autoexposure(self):
        pass

    def flush(self):
        """
        Abstract method to cycle the image buffer (if any)
        such that all new :meth:`.get_image()`
        calls yield fresh frames.
        """
        raise NotImplementedError()

    NotImplementedError()

    ################################################## SETTERS #########################################################
    def set_exposure(self, exposure_s):
        """Abstract method to set the integration time in seconds."""
        raise NotImplementedError()

    def set_gain(self, gain):
        raise NotImplementedError()

    def set_frame_rate(self, frame_rate):
        raise NotImplementedError()

    def set_woi(self, woi=None):
        raise NotImplementedError()

    def set_brightness(self, brightness):
        """Abstract method to set brightness."""
        raise NotImplementedError()

    def set_contrast(self, contrast):
        """Abstract method to set contrast."""
        raise NotImplementedError()

    def set_saturation(self, saturation):
        """Abstract method to set saturation."""
        raise NotImplementedError()

    ################################################## GETTERS #########################################################
    def get_name(self):
        """Abstract method to get the information about the camera."""
        raise NotImplementedError()

    def get_exposure(self):
        """Abstract method to get the integration time in seconds."""
        raise NotImplementedError()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_bitdepth(self):
        return self.bitdepth

    def get_gain(self):
        """Abstract method to get the gain."""
        raise NotImplementedError()

    def get_frame_rate(self):
        """Abstract method to get the frame rate time in frames per seconds."""
        raise NotImplementedError()

    def get_brightness(self):
        """Abstract method to get brightness."""
        raise NotImplementedError()

    def get_contrast(self):
        """Abstract method to get contrast."""
        raise NotImplementedError()

    def get_saturation(self):
        """Abstract method to get saturation."""
        raise NotImplementedError()

    def get_exposure_min_max(self):
        """Abstract method to get the minimum and maximum exposure time."""
        raise NotImplementedError()

    def get_gain_min_max(self):
        """Abstract method to get the minimum and maximum gain."""
        raise NotImplementedError()

    def get_frame_rate_min_max(self):
        """Abstract method to get the minimum and maximum frame rate."""
        raise NotImplementedError()
