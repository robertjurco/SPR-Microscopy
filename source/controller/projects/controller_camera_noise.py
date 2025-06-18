from collections import deque

import numpy as np

from source.controller.CameraWorker import CameraWorkerThread
from source.controller.widgets.ROI_controller import ROIController


class CameraNoiseController:

    def __init__(self, model, project_view, serial, full_well_capacity = 17200):
        self.model = model
        self.project_view = project_view

        self.serial = serial

        # Define before thread, no processing on image recieved
        self.start_processing = False

        # Setup camera
        self.camera = self.model.device_manager.loaded_devices[self.serial]

        self.worker_thread = CameraWorkerThread(self.camera)
        self.worker_thread.frame_received.connect(self.process_frame)
        self.worker_thread.frame_received_6FPS.connect(self.process_frame_60FPS)
        self.worker_thread.start()  # This should start the thread and call `run`

        # RIO controller
        self.ROI_controller = ROIController(self.model, self.serial, self.project_view.roi_widget, self.project_view.image_display)

        # data processing initialization
        self.full_well_capacity = full_well_capacity
        self.data = None  # Will hold per-pixel intensity histories
        self.max_frames = 1000
        self.means = None  # Will be 1D array of per-pixel means
        self.stds = None   # Will be 1D array of per-pixel stds
        self.processed = False  # Flag to ensure one-time processing

        # Connects
        self.project_view.button_start.clicked.connect(self.start_measurement)

    def start_measurement(self):
        self.max_frames = self.project_view.spinbox_max_frames.value()
        self.start_processing = True


    def process_frame(self, image):
        if not self.start_processing:
            return

        if len(image.shape) != 2:
            raise ValueError("Input must be a 2D grayscale image.")

        # Normalize and invert: 0 → 1.0, 255 → 0.0
        inverted = 1.0 - (image.astype(np.float32) / 255.0)

        # multiply by well capacity
        inverted *= self.full_well_capacity

        # Initialize deque with maxlen
        if self.data is None:
            self.data = deque(maxlen=self.max_frames)

        # Append new frame (2D array) to history
        self.data.append(inverted)

        # Only process once after enough frames collected
        if not self.processed and len(self.data) == self.max_frames:
            self.worker_thread.stop()

            data_array = np.stack(self.data, axis=0)
            mean_image = np.mean(data_array, axis=0)
            std_image = np.std(data_array, axis=0)
            self.means = mean_image.flatten()
            self.stds = std_image.flatten()
            self.processed = True  # Mark as processed

            self.project_view.plot_widget.plot_data(self.means, self.stds, scatter_plot=True, color='red')
            x = np.linspace(0, self.full_well_capacity, 1000)
            y = np.sqrt(x)
            self.project_view.plot_widget.plot_data(x, y)

    def process_frame_60FPS(self, image):
        """This method simulates acquiring a frame."""
        # Your frame acquisition logic here (e.g., from camera)
        # processing image

        self.project_view.update_frame(image)