from PySide6.QtCore import QThread, Signal
from pypylon import pylon

from source.model.hardware.camera import Camera


class Basler(Camera):
    frame_acquired = Signal(object)

    def __init__(self, index):
        # Mandatory functions:
        # - Opening a connection to the device
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        # selection of the camera with the specific id
        self.cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(devices[index]))
        self.cam.Open()

        # Finally, use the superclass constructor to initialize other required variables.
        # - Gathering parameters such a width, height, and bitdepth.
        super().__init__(
            width = self.cam.Width.Value,
            height = self.cam.Height.Value,
            bitdepth = self.cam.PixelFormat.IntValue,
        )

    def close(self):
        """See :meth:`.Camera.close`."""
        self.cam.Close()
        del self.cam

    def reset(self):
        """
        Abstract method to reset the camera to a default state.
        """
        raise NotImplementedError()

    def run(self):
        print("starting camera thread")
        self.running = True
        self.cam.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        while self.running:
            print("acquiring frame")
            grab_result = self.cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grab_result.GrabSucceeded():
                image = grab_result.Array
                self.frame_acquired.emit(image)
            grab_result.Release()

    def stop(self):
        self.running = False
        self.cam.StopGrabbing()

    def autoexposure(self):
        pass

    def flush(self):
        """
        Abstract method to cycle the image buffer (if any)
        such that all new :meth:`.get_image()`
        calls yield fresh frames.
        """
        raise NotImplementedError()



    ################################################## SETTERS #########################################################
    def set_exposure(self, exposure_s):
        self.cam.ExposureTime.SetValue(exposure_s)

    def set_gain(self, gain):
        self.cam.Gain.SetValue(gain)

    def set_frame_rate(self, frame_rate):
        self.cam.AcquisitionFrameRate.SetValue(frame_rate)

    def set_woi(self, woi=None):
        # Implement the set_woi logic
        pass

    def set_brightness(self, brightness):
        self.cam.Brightness.SetValue(brightness)

    def set_contrast(self, contrast):
        self.cam.Contrast.SetValue(contrast)

    def set_saturation(self, saturation):
        self.cam.Saturation.SetValue(saturation)

    ################################################## GETTERS #########################################################
    def get_name(self):
        return self.cam.GetFriendlyName()

    def get_exposure(self):
        return self.cam.ExposureTime.GetValue()

    def get_gain(self):
        return self.cam.Gain.GetValue()

    def get_frame_rate(self):
        return self.cam.AcquisitionFrameRate.GetValue()

    def get_brightness(self):
        return self.cam.Brightness.GetValue()

    def get_contrast(self):
        return self.cam.Contrast.GetValue()

    def get_saturation(self):
        return self.cam.Saturation.GetValue()

    def get_exposure_min_max(self):
        return self.cam.ExposureTime.GetMin(), self.cam.ExposureTime.GetMax()

    def get_gain_min_max(self):
        return self.cam.Gain.GetMin(), self.cam.Gain.GetMax()

    def get_frame_rate_min_max(self):
        return self.cam.AcquisitionFrameRate.GetMin(), self.cam.AcquisitionFrameRate.GetMax()
