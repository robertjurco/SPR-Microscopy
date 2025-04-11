import numpy as np

from source.controller.CameraWorker import CameraWorkerThread
from source.view.tabs.view_imaging import ImagingView

class CameraFPSController:

    def __init__(self, model, project_view, serial = '24514092'):
        self.model = model
        self.project_view = project_view

        self.serial = serial

        self.camera = self.model.device_manager.loaded_devices[self.serial]
        self.worker_thread = CameraWorkerThread(self.camera, FPS_averaging = 10.0, target_fps=1000000)

        self.worker_thread.fps_updated.connect(self.on_fps_measurement_height)

        self.start_measurement_height()

    def start_measurement_exposure(self):
        self.exposure_bounds = self.camera.get_exposure_min_max()
        self.exposure = self.get_random_exposure()
        self.worker_thread.start()

    def start_measurement_height(self):
        self.height_bounds = self.camera.get_height_min_max()
        self.height = self.height_bounds[1]
        settings = {'exposure': {'value': 0.021}, 'height': {'value': self.height}}

        self.model.device_manager.set_device_settings(self.serial, settings)
        self.worker_thread.start()

    def start_measurement_both(self):
        self.exposure_bounds = (0.02, 100)
        self.height_bounds = self.camera.get_height_min_max()
        self.exposure = self.get_random_exposure()
        self.height = int(self.get_random_height())
        settings = {'exposure': {'value': self.exposure}, 'height': {'value': self.height}}
        self.model.device_manager.set_device_settings(self.serial, settings)
        self.worker_thread.start()


    def get_random_exposure(self):
        """
        Select a random exposure time from the bounds (0.02, 100) logarithmically.
        Lower values should have a higher chance of being selected.
        """
        min_exposure, max_exposure = self.exposure_bounds

        # Logarithmic sampling:
        log_min = np.log(min_exposure)
        log_max = np.log(max_exposure)

        # Sample a value from the logarithmic range
        log_sample = np.random.uniform(log_min, log_max)

        # Exponentiate to return a value in the original exposure range
        exposure = np.exp(log_sample)

        return exposure

    def get_random_height(self):
        """
        Select a random exposure time from the bounds (0.02, 100) logarithmically.
        Lower values should have a higher chance of being selected.
        """
        min_height, max_height = self.height_bounds

        # Sample a value from the  range
        height = np.random.uniform(min_height, max_height)

        return int(height)

    def on_fps_measurement_EXP(self, fps):
        print(f"FPS: {fps}, Exposure: {self.exposure}")
        self.project_view.plot_widget.update_plot(self.exposure, fps)

        self.worker_thread.stop()
        self.model.device_manager.loaded_devices[self.serial].pause()

        self.exposure = self.get_random_exposure()

        settings = {'exposure': {'value': self.exposure}}

        self.model.device_manager.set_device_settings(self.serial, settings)
        target_fps = self.model.device_manager.loaded_devices[self.serial].target_fps

        self.worker_thread.update_fps(target_fps)
        self.worker_thread.start()

    def on_fps_measurement_height(self, fps):
        print(f"FPS: {fps}, Height: {self.height}")
        self.project_view.plot_widget_2.update_plot(self.height, fps)

        self.worker_thread.stop()
        self.model.device_manager.loaded_devices[self.serial].pause()

        if self.height > self.height_bounds[0]:
            self.height = self.height-1
        else:
            return

        settings = {'height': {'value': self.height}}

        self.model.device_manager.set_device_settings(self.serial, settings)
        self.worker_thread.start()

    def on_fps_measurement_both(self, fps):
        print(f"FPS: {fps}, Exposure: {self.exposure}, Height: {self.height}")
        self.project_view.plot_widget_3.update_plot(self.exposure, self.height, fps)

        self.worker_thread.stop()
        self.model.device_manager.loaded_devices[self.serial].pause()

        self.exposure = self.get_random_exposure()
        self.height = self.get_random_height()

        settings = {'exposure': {'value': self.exposure}, 'height': {'value': self.height}}
        self.model.device_manager.set_device_settings(self.serial, settings)
        target_fps = self.model.device_manager.loaded_devices[self.serial].target_fps * 40.0

        self.worker_thread.update_fps(target_fps)
        self.worker_thread.start()