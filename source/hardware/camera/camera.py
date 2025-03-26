import time

import numpy as np
from PySide6.QtGui import QImage
from PySide6.QtCore import QObject, Signal, QThread, QRunnable, QThreadPool

class Camera(QObject):
    """Abstract class for camera_models."""

    def __init__(self):
        super().__init__()
        self.average = 100

    def close(self):
        """Closes the camera connection and deletes related objects.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def reset(self):
        """Resets the camera to a default state.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def autoexposure(self):
        """Enables the camera's auto exposure feature."""
        pass

    def flush(self):
        """Cycles the image buffer so that all new get_image() calls yield fresh frames.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def acquire_image(self):
        """Acquires an image from the camera.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def step(self):
        image = self.acquire_image()

        image_array = np.array(image)
        avg_signal = np.mean(image_array)

        time.sleep(1.0 / self.get_frame_rate())

    def set_average(self, average):
        self.average = average

    def get_average(self):
        return self.average


    ################################################## SETTERS #########################################################

    def set_width(self, width):
        """Sets the camera resolution width.

        Parameters
        ----------
        width : int
            The width of the camera resolution.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def set_height(self, height):
        """Sets the camera resolution height.

        Parameters
        ----------
        height : int
            The height of the camera resolution.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def set_bitdepth(self, bitdepth):
        """Sets the camera bit depth.

        Parameters
        ----------
        bitdepth : int
            The bit depth of the camera resolution.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def set_exposure(self, exposure_s):
        """Sets the integration time in seconds.

        Parameters
        ----------
        exposure_s : float
            The integration time in seconds.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def set_gain(self, gain):
        """Sets the camera gain.

        Parameters
        ----------
        gain : float
            The gain value.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def set_frame_rate(self, frame_rate):
        """Sets the frame rate in frames per second.

        Parameters
        ----------
        frame_rate : float
            The frame rate in frames per second.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def set_woi(self, woi=None):
        """Sets the Window of Interest.

        Parameters
        ----------
        woi : tuple
            A tuple (offsetX, offsetY, width, height) defining the window of interest.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def set_brightness(self, brightness):
        """Sets the brightness value.

        Parameters
        ----------
        brightness : float
            The brightness value.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def set_contrast(self, contrast):
        """Sets the contrast value.

        Parameters
        ----------
        contrast : float
            The contrast value.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def set_saturation(self, saturation):
        """Sets the saturation value.

        Parameters
        ----------
        saturation : float
            The saturation value.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    ################################################## GETTERS #########################################################

    def get_name(self):
        """Gets the information about the camera.

        Returns
        -------
        string
            Friendly version of the camera name.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_width(self):
        """Gets the width of the camera's resolution.

        Returns
        -------
        int
            The width of the camera's resolution.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        return NotImplementedError()

    def get_width_min_max(self):
        """Gets the minimum and maximum values for width.

        Returns
        -------
        tuple
            A tuple (min_width, max_width) representing the minimum and maximum width values.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_height(self):
        """Gets the height of the camera's resolution.

        Returns
        -------
        int
            The height of the camera's resolution.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        return NotImplementedError()

    def get_height_min_max(self):
        """Gets the minimum and maximum values for height.

        Returns
        -------
        tuple
            A tuple (min_height, max_height) representing the minimum and maximum height values.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_bitdepth(self):
        """Gets the bit depth of the camera's resolution.

        Returns
        -------
        int
            The bit depth of the camera's resolution.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        return NotImplementedError()

    def get_exposure(self):
        """Gets the integration time in seconds.

        Returns
        -------
        float
            Integration time in seconds.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_exposure_min_max(self):
        """Gets the minimum and maximum exposure time.

        Returns
        -------
        tuple
            A tuple (min_exposure, max_exposure) representing the minimum and maximum exposure times.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_gain(self):
        """Gets the gain value.

        Returns
        -------
        float
            Gain.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_gain_min_max(self):
        """Gets the minimum and maximum gain values.

        Returns
        -------
        tuple
            A tuple (min_gain, max_gain) representing the minimum and maximum gain values.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_frame_rate(self):
        """Gets the frame rate in frames per second.

        Returns
        -------
        float
            Frames per second.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_frame_rate_min_max(self):
        """Gets the minimum and maximum frame rate values.

        Returns
        -------
        tuple
            A tuple (min_frame_rate, max_frame_rate) representing the minimum and maximum frame rate values.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_woi(self):
        """Gets the current Window of Interest.

        Returns
        -------
        tuple
            A tuple (offsetX, offsetY, width, height) representing the current window of interest.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_woi_min_max(self):
        """Gets the minimum and maximum values for WOI parameters.

        Returns
        -------
        dict
            A dictionary with min/max values for 'offsetX', 'offsetY', 'width', 'height'.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_brightness(self):
        """Gets the brightness value.

        Returns
        -------
        float
            Brightness.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_contrast(self):
        """Gets the contrast value.

        Returns
        -------
        float
            Contrast.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    def get_saturation(self):
        """Gets the saturation value.

        Returns
        -------
        float
            Saturation.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError()

    ############################################ IMPLEMENTED FUNCTIONS #################################################

    def get_all_settings(self):
        """Gets all the current settings of the camera, including min and max values.

        Returns
        -------
        dict
            A dictionary containing all the current settings of the camera, along with their min and max values.
        """
        settings = {
            'name': self.get_name(),
            'width': {
                'value': self.get_width(),
                'min': self.get_width_min_max()[0],
                'max': self.get_width_min_max()[1]
            },
            'height': {
                'value': self.get_height(),
                'min': self.get_height_min_max()[0],
                'max': self.get_height_min_max()[1]
            },
            'bitdepth': self.get_bitdepth(),
            'exposure': {
                'value': self.get_exposure(),
                'min': self.get_exposure_min_max()[0],
                'max': self.get_exposure_min_max()[1]
            },
            'gain': {
                'value': self.get_gain(),
                'min': self.get_gain_min_max()[0],
                'max': self.get_gain_min_max()[1]
            },
            'frame_rate': {
                'value': self.get_frame_rate(),
                'min': self.get_frame_rate_min_max()[0],
                'max': self.get_frame_rate_min_max()[1]
            },
            'woi': {
                'value': self.get_woi(),
                'min_max': self.get_woi_min_max()
            }
        }
        """
        'brightness': self.get_brightness(),
        'contrast': self.get_contrast(),
        'saturation': self.get_saturation()
        """
        return settings

    def set_all_settings(self, settings):
        """Sets all the camera settings from a dictionary, ensuring values are within valid ranges.

        Parameters
        ----------
        settings : dict
            A dictionary containing all the settings to be applied to the camera.
        """
        if 'width' in settings:
            width = settings['width']
            min_width, max_width = self.get_width_min_max()
            if min_width <= width <= max_width:
                self.set_width(width)
            else:
                raise ValueError(f"Width {width} is out of range ({min_width}, {max_width})")

        if 'height' in settings:
            height = settings['height']
            min_height, max_height = self.get_height_min_max()
            if min_height <= height <= max_height:
                self.set_height(height)
            else:
                raise ValueError(f"Height {height} is out of range ({min_height}, {max_height})")

        if 'bitdepth' in settings:
            self.set_bitdepth(settings['bitdepth'])

        if 'exposure' in settings:
            exposure = settings['exposure']
            min_exposure, max_exposure = self.get_exposure_min_max()
            if min_exposure <= exposure <= max_exposure:
                self.set_exposure(exposure)
            else:
                raise ValueError(f"Exposure {exposure} is out of range ({min_exposure}, {max_exposure})")

        if 'gain' in settings:
            gain = settings['gain']
            min_gain, max_gain = self.get_gain_min_max()
            if min_gain <= gain <= max_gain:
                self.set_gain(gain)
            else:
                raise ValueError(f"Gain {gain} is out of range ({min_gain}, {max_gain})")

        if 'frame_rate' in settings:
            frame_rate = settings['frame_rate']
            min_frame_rate, max_frame_rate = self.get_frame_rate_min_max()
            if min_frame_rate <= frame_rate <= max_frame_rate:
                self.set_frame_rate(frame_rate)
            else:
                raise ValueError(f"Frame rate {frame_rate} is out of range ({min_frame_rate}, {max_frame_rate})")

        if 'woi' in settings:
            self.set_woi(settings['woi'])

        if 'brightness' in settings:
            self.set_brightness(settings['brightness'])

        if 'contrast' in settings:
            self.set_contrast(settings['contrast'])

        if 'saturation' in settings:
            self.set_saturation(settings['saturation'])