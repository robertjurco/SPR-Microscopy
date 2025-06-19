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
        self.camera_thread = None
        self.start_camera_thread()

        # RIO controller
        self.ROI_controller = ROIController(self.model, self.serial, self.project_view.roi_widget, self.project_view.image_display)
        self.ROI_controller.start_camera_thread.connect(self.start_camera_thread)
        self.ROI_controller.stop_camera_thread.connect(self.stop_camera_thread)

        # data processing initialization
        self.full_well_capacity = full_well_capacity
        self.data = None  # Will hold per-pixel intensity histories
        self.max_frames = 1000
        self.means = None  # Will be 1D array of per-pixel means
        self.stds = None   # Will be 1D array of per-pixel stds
        self.processed = False  # Flag to ensure one-time processing

        # Connects
        self.project_view.button_start.clicked.connect(self.start_measurement)

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
        self.start_processing = True


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
            # Normalize and invert: 0 → 1.0, 255 → 0.0
            inverted = 1.0 - (roi_image.astype(np.float32) / 255.0)

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
                std_image = np.std(data_array, axis=0)

                self.means = mean_image.flatten()
                self.stds = std_image.flatten()

                color = color_cycle[i % len(color_cycle)]
                self.project_view.plot_widget.plot_data(self.means, self.stds, scatter_plot=True, color=color)

            # === Plot reference curve (same for all ROIs) ===
            x = np.linspace(0, self.full_well_capacity, 1000)
            y = np.sqrt(x)
            self.project_view.plot_widget.plot_data(x, y)


    def process_frame_60FPS(self, image):
        """This method simulates acquiring a frame."""
        # Your frame acquisition logic here (e.g., from camera)
        # processing image

        self.project_view.update_frame(image)