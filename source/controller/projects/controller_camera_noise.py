import random
from collections import deque

import numpy as np

from source.controller.CameraWorker import CameraWorkerThread
from source.controller.widgets.ROI_controller import ROIController


class CameraNoiseController:

    def __init__(self, model, project_view, serial, full_well_capacity = 182000):
        self.model = model
        self.project_view = project_view

        self.serial = serial

        # Define before thread, no processing on image recieved
        self.start_processing = False

        # Setup camera
        self.camera = self.model.device_manager.loaded_devices[self.serial]
        self.camera_thread = None
        self.start_camera_thread()

        # Setup spinbox exposure values
        camera_settings = self.model.device_manager.get_device_settings(self.serial)
        exposure = camera_settings['exposure']['value']
        exposure_min= camera_settings['exposure']['min']
        exposure_max = camera_settings['exposure']['max']

        self.project_view.spinbox_exposure.setValue(exposure)
        self.project_view.spinbox_exposure.setMinimum(exposure_min)
        self.project_view.spinbox_exposure.setMaximum(exposure_max)

        self.project_view.set_exposure.connect(self.set_exposure)
        self.project_view.max_frames_changed.connect(self.set_max_frames)

        # RIO controller
        self.ROI_controller = ROIController(self.model, self.serial, self.project_view.roi_widget, self.project_view.image_display)
        self.ROI_controller.start_camera_thread.connect(self.start_camera_thread)
        self.ROI_controller.stop_camera_thread.connect(self.stop_camera_thread)

        # data processing initialization
        self.full_well_capacity = full_well_capacity
        self.data = None  # Will hold per-pixel intensity histories
        self.max_frames = 200
        self.means = None  # Will be 1D array of per-pixel means
        self.vars = None   # Will be 1D array of per-pixel stds
        self.processed = False  # Flag to ensure one-time processing

        # Connects
        self.project_view.button_start.clicked.connect(self.start_measurement)

        # Update spinbox
        self.project_view.spinbox_max_frames.setValue(self.max_frames)

    def start_camera_thread(self):
        if self.camera_thread is not None:
            self.camera_thread.stop()
            self.camera_thread.deleteLater()

        self.camera_thread = CameraWorkerThread(self.camera)
        self.camera_thread.frame_received.connect(self.process_frame)
        self.camera_thread.frame_received_6FPS.connect(self.process_frame_60FPS)
        self.camera_thread.start() # This should start the thread and call `run`

    def stop_camera_thread(self):
        if self.camera_thread is not None:
            self.camera_thread.stop()
            self.camera_thread.deleteLater()
            self.camera.pause()

    def start_measurement(self):
        self.max_frames = self.project_view.spinbox_max_frames.value()

        self.data = None
        self.processed = False
        self.start_processing = True

    def set_exposure(self, exposure: float):
        self.stop_camera_thread()

        settings = {'exposure': {'value': exposure}}
        self.model.device_manager.set_device_settings(self.serial, settings)

        self.start_camera_thread()

    def set_max_frames(self, max_frames: int):
        self.max_frames = max_frames

        # Reset data so that new deques with updated maxlen are created
        self.data = None
        self.processed = False
        self.start_processing = False  # Or True if you want to start immediately


    def process_frame(self, image):
        if not self.start_processing:
            return

        if len(image.shape) != 2:
            raise ValueError("Input must be a 2D grayscale image.")

        images = self.ROI_controller.process_ROI(image)

        # Only initialize deque once
        if self.data is None:
            self.data = {}  # Dict of {roi_id: deque}
            for roi_id, _ in images:
                self.data[roi_id] = deque(maxlen=self.max_frames)

        # === Process each ROI image individually ===
        for roi_id, roi_image in images:
            # Normalize and invert: 0 → 1.0, 4095 → 0.0
            inverted = (roi_image.astype(np.float32) / 4095.0)

            # Multiply by full well capacity
            inverted *= self.full_well_capacity

            # Append to deque for that ROI
            self.data[roi_id].append(inverted)

        # === Once we have enough frames, compute statistics ===
        if not self.processed and all(len(dq) == self.max_frames for dq in self.data.values()):
            self.stop_camera_thread()
            self.processed = True

            color_cycle = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']
            for i, (roi_id, dq) in enumerate(self.data.items()):
                data_array = np.stack(dq, axis=0)  # Shape: (max_frames, H, W)
                mean_image = np.mean(data_array, axis=0)
                var_image = np.var(data_array, axis=0)  # Var = square of STD

                self.means = mean_image.flatten()
                self.vars = var_image.flatten()

                color = color_cycle[i % len(color_cycle)]
                self.project_view.plot_widget.plot_data(self.means, self.vars, scatter_plot=True, color=color)

                if i == 0:
                    # === Pick a random pixel and plot its histogram ===
                    h, w = mean_image.shape
                    rand_y = random.randint(0, h - 1)
                    rand_x = random.randint(0, w - 1)

                    pixel_values = data_array[:, rand_y, rand_x]  # Shape: (max_frames,)
                    self.project_view.histogram_widget.plot_histogram(pixel_values, color=color)

            # === Plot reference curve (same for all ROIs) ===
            x = np.linspace(0, self.full_well_capacity, 1000)
            self.project_view.plot_widget.plot_data(x, x)


    def process_frame_60FPS(self, image):
        """This method simulates acquiring a frame."""
        # Your frame acquisition logic here (e.g., from camera)
        # processing image

        self.project_view.update_frame(image)