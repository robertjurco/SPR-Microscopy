import time

from PySide6.QtCore import QTimer, QThreadPool
from PySide6.QtCore import Signal, QRunnable, Slot
from PySide6.QtGui import QImage

from source.view.settings.view_settings_camera import ViewCameraSettings

class CameraWorker(QRunnable):
    """
    A worker to handle the camera frame acquisition at a specified FPS.
    """
    def __init__(self, camera, controller, target_fps=60):
        super().__init__()
        self.camera = camera
        self.controller = controller
        self.target_fps = target_fps  # Target FPS, e.g., 60
        self.timer = QTimer()
        self.frame_count = 0
        self.start_time = time.time()

        # Set up the timer to trigger at the target FPS
        self.timer.timeout.connect(self.acquire_frame)
        self.timer.start(1000 / self.target_fps)  # Calculate interval in ms (1000ms / target_fps)

    def run(self):
        """
        Start acquiring frames.
        This method is run on a separate thread.
        """
        pass  # The work is done in the `acquire_frame` method triggered by QTimer

    def start(self):
        """
        Start the worker.
        """
        self.timer.start(1000 / self.target_fps)

    def stop(self):
        """
        Stop the worker.
        """
        self.timer.stop()

    def acquire_frame(self):
        """
        This method is triggered by the QTimer to acquire a frame from the camera.
        It simulates acquiring a frame every frame period based on the target FPS.
        """
        image = self.camera.acquire_image()  # Acquire a frame from the camera
        self.on_frame_received(image.copy())

    def on_frame_received(self, frame: QImage):
        """
        Handle the frame received signal from the camera.
        This method processes the frame and updates the controller.
        """
        self.frame_count += 1  # Increment frame count

        # Calculate FPS (frames per second) every second
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        if elapsed_time >= 1.0:
            fps = self.frame_count / elapsed_time
            print(f"Current FPS: {fps:.2f}")  # Print FPS
            self.start_time = current_time
            self.frame_count = 0

        # Pass the frame to the controller
        self.controller.process_frame(frame)

class CameraSettingsController:

    def __init__(self, model, view, serial):
        self.model = model
        self.view = view
        self.serial = serial

        # Handle your settings functionality here
        settings = self.model.device_manager.get_device_settings(serial)

        self.settings_dialog = ViewCameraSettings(serial, settings)
        self.settings_dialog.settings_widget.settings_applied.connect(self.handle_settings_applied)

        # create an image acquisition link
        camera = self.model.device_manager.loaded_devices[serial]

        self.worker = CameraWorker(camera, self)

        # Create and start the camera worker in the thread pool
        self.thread_pool = QThreadPool()
        self.thread_pool.start(self.worker)

        # call create new thread in camera manager
        self.settings_dialog.show()

    def process_frame(self, image):
        """This method simulates acquiring a frame."""
        # Your frame acquisition logic here (e.g., from camera)
        #processing image

        self.settings_dialog.update_frame(image)

    def handle_settings_applied(self, settings):
        self.worker.stop()
        self.model.device_manager.loaded_devices[self.serial].pause()
        self.model.device_manager.set_device_settings(self.serial, settings)
        self.worker.start()
        print(f"Settings for device {settings} set................................")