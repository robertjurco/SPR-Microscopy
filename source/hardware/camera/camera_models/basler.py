from pypylon import pylon

from source.hardware.camera.camera import Camera


class Basler(Camera):
    def __init__(self, serial):
        # Initialize the transport layer factory
        tl_factory = pylon.TlFactory.GetInstance()
        # Enumerate all devices connected to the machine
        devices = tl_factory.EnumerateDevices()

        # Initialize the camera variable
        self.cam = None
        self.serial = serial

        # Search for the camera with the matching serial number
        for device in devices:
            # Retrieve the device info
            device_serial = device.GetSerialNumber()
            if device_serial == serial:
                # Create and open the camera with the specified serial number
                self.cam = pylon.InstantCamera(tl_factory.CreateDevice(device))
                self.cam.Open()
                break

        # Raise an exception if no camera with the specified serial number is found
        if self.cam is None:
            raise ValueError(f"No camera with serial number {serial} found")

        # Finally, use the superclass constructor to initialize other required variables.
        # - Gathering parameters such a width, height, and bitdepth.
        super().__init__()

        # Disable autoexposure
        self.cam.ExposureAuto.SetValue("Off")

        # Initialize default frame rate and exposure time variables
        self.target_fps = 60  # Default frame rate, this can be updated later
        self.exposure_time = None  # To track the exposure time

        self.nodemap = self.cam.GetNodeMap()

        self.multi_roi_info = {}
        self._init_multi_roi_info()

    def _init_multi_roi_info(self):
        """Detect and store multiple ROI support and limits."""
        info = {}

        # Try to read sensor size
        try:
            info["SensorWidth"] = self.nodemap.GetNode("SensorWidth").GetValue()
            info["SensorHeight"] = self.nodemap.GetNode("SensorHeight").GetValue()
        except:
            info["SensorWidth"] = None
            info["SensorHeight"] = None

        # Check if multiple ROI is supported and enabled
        try:
            info["MultiROIColumnsSupported"] = self.nodemap.GetNode("BslMultipleROIColumnsEnable").IsWritable()
            info["MultiROIRowsSupported"] = self.nodemap.GetNode("BslMultipleROIRowsEnable").IsWritable()

            if info["MultiROIColumnsSupported"]:
                col_selector = self.nodemap.GetNode("BslMultipleROIColumnSelector")
                info["MaxColumnROIs"] = col_selector.GetMax()
            else:
                info["MaxColumnROIs"] = 0

            if info["MultiROIRowsSupported"]:
                row_selector = self.nodemap.GetNode("BslMultipleROIRowSelector")
                info["MaxRowROIs"] = row_selector.GetMax()
            else:
                info["MaxRowROIs"] = 0

        except Exception as e:
            info["MultiROIColumnsSupported"] = False
            info["MultiROIRowsSupported"] = False
            info["MaxColumnROIs"] = 0
            info["MaxRowROIs"] = 0

        self.multi_roi_info = info

        self.print_roi_info()

    def print_roi_info(self):
        for key, value in self.multi_roi_info.items():
            print(f"{key}: {value}")


    def close(self):
        """See :meth:`.Camera.close`."""
        self.cam.Close()
        del self.cam

    def reset(self):
        """
        Abstract method to reset the camera to a default state.
        """
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

    def acquire_image(self):
        """Acquires an image from the camera."""
        if self.cam.IsGrabbing():
            grab_result = self.cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) # 0 or 5000 ???
            if grab_result.GrabSucceeded():
                return grab_result.Array
            grab_result.Release()
        else:
            self.cam.StartGrabbing()

    def pause(self):
        self.cam.StopGrabbing()

    def handle_message(self, massage):
        print("Cannot handle massage: " + str(massage))

    ################################################## SETTERS #########################################################
    def set_width(self, width: int):
        """Sets the camera resolution width."""
        print(width)
        self.cam.Width.SetValue(width)


    def set_height(self, height: int):
        """Sets the camera resolution height."""
        self.cam.Height.SetValue(height)

    def set_bitdepth(self, bitdepth: int):
        """Sets the camera bit depth."""
        self.cam.PixelFormat.SetValue(f"Mono{bitdepth}")


    def set_exposure(self, exposure_time: float):
        """
        Set the exposure time or enable auto-exposure.
        Ensure that exposure time does not go below the camera's minimum allowable exposure.
        """
        # Get the camera's minimum exposure time
        min_exposure_time = self.get_exposure_min_max()[0]

        if exposure_time:
            # Disable autoexposure
            self.cam.ExposureAuto.SetValue("Off")
            # Ensure that exposure time is above the minimum allowed value
            exposure_time = max(exposure_time, min_exposure_time)
            self.exposure_time = exposure_time
            self.cam.ExposureTime.SetValue(exposure_time * 1000)
        else:
            # Enable auto exposure if no exposure time is provided
            self.cam.ExposureAuto.SetValue('Continuous')

        # Adjust frame rate based on exposure time
        self.adjust_frame_rate_based_on_exposure()
        self.set_frame_rate(self.target_fps)
        self.cam.AcquisitionFrameRateEnable.Value = False

        # Prints for tests
        print(f"Exposure Time: {self.get_exposure()}")
        print(f"Target Frame Rate: {self.target_fps}")

    def adjust_frame_rate_based_on_exposure(self):
        """
        Adjust the frame rate based on the exposure time.
        If exposure time is at the minimum, set the highest possible frame rate.
        """
        min_exposure_time = self.get_exposure_min_max()[0]
        if self.exposure_time is None or self.exposure_time == min_exposure_time:
            # If exposure time is minimum or auto-exposure is used, set frame rate to maximum
            max_frame_rate = self.cam.ResultingFrameRateAbs.GetMax()
            self.target_fps = max_frame_rate
        else:
            # Calculate the optimal frame rate based on exposure time (if not at minimum exposure)
            max_frame_rate = self.get_frame_rate_min_max()[1]
            optimal_frame_rate = 1000 /  self.exposure_time  # Adjusting to exposure in miliseconds
            self.target_fps = min(optimal_frame_rate, max_frame_rate)

    def set_gain(self, gain: float):
        """Sets the camera gain."""
        self.cam.Gain.SetValue(gain)

    def set_frame_rate(self, frame_rate: float):
        """Sets the frame rate in frames per second."""
        self.cam.AcquisitionFrameRateEnable = False # Disables frame rate, otherwise we would limit the maximal frame rate
        self.cam.AcquisitionFrameRate.SetValue(frame_rate)


    def set_woi(self, woi=None):
        """Sets the Window of Interest."""
        try:
            offsetX, offsetY, width, height = woi
            self.cam.OffsetX.SetValue(offsetX)
            self.cam.OffsetY.SetValue(offsetY)
            self.set_width(width)
            self.set_height(height)
        except Exception as e:
            print(f"Camera serial: {self.serial} Invalid Window of Interest format. Expected a list of 4 integers.")

    ################################################## GETTERS #########################################################
    def get_name(self):
        """Gets the information about the camera."""
        return self.cam.GetDeviceInfo().GetFriendlyName()

    def get_width(self):
        """Gets the width of the camera's resolution."""
        return self.cam.Width.Value

    def get_width_min_max(self):
        """Gets the minimum and maximum values for width."""
        return (self.cam.Width.Min, self.cam.Width.Max)

    def get_height(self):
        """Gets the height of the camera's resolution."""
        return self.cam.Height.Value

    def get_height_min_max(self):
        """Gets the minimum and maximum values for height."""
        return (self.cam.Height.Min, self.cam.Height.Max)

    def get_bitdepth(self):
        """Gets the bit depth of the camera's resolution."""
        return int(self.cam.PixelFormat.Value.replace("Mono", ""))

    def get_exposure(self):
        """Gets the integration time in seconds."""
        return self.cam.ExposureTime.Value / 1e3  # Convert microseconds to miliseconds

    def get_exposure_min_max(self):
        """Gets the minimum and maximum exposure time."""
        return (self.cam.ExposureTime.Min / 1e3, self.cam.ExposureTime.Max / 1e3)  # Convert microseconds to miliseconds

    def get_gain(self):
        """Gets the gain value."""
        return self.cam.Gain.Value

    def get_gain_min_max(self):
        """Gets the minimum and maximum gain values."""
        return (self.cam.Gain.Min, self.cam.Gain.Max)

    def get_frame_rate(self):
        """Gets the frame rate in frames per second."""
        return self.cam.AcquisitionFrameRate.Value

    def get_frame_rate_min_max(self):
        """Gets the minimum and maximum frame rate values."""
        return (self.cam.AcquisitionFrameRate.Min, self.cam.AcquisitionFrameRate.Max)

    def get_woi(self):
        """Gets the current Window of Interest."""
        return (self.cam.OffsetX.Value, self.cam.OffsetY.Value, self.cam.Width.Value, self.cam.Height.Value)

    def get_woi_min_max(self):
        """Gets the minimum and maximum values for WOI parameters."""
        return {
            'offsetX': (self.cam.OffsetX.Min, self.cam.OffsetX.Max),
            'offsetY': (self.cam.OffsetY.Min, self.cam.OffsetY.Max),
            'width': (self.cam.Width.Min, self.cam.Width.Max),
            'height': (self.cam.Height.Min, self.cam.Height.Max)
        }
