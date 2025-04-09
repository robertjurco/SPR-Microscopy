import time

from PySide6.QtCore import QTimer, QThreadPool, QObject, QThread
from PySide6.QtCore import Signal, QRunnable, Slot
from PySide6.QtGui import QImage

from source.view.settings.view_settings_camera import ViewCameraSettings

class CameraWorkerThread(QThread):
    fps_updated = Signal(float)
    frame_received = Signal(object)

    def __init__(self, camera, target_fps = 60):
        super().__init__()
        self.camera = camera
        self.frame_count = 0
        self.start_time = time.time()
        self.target_fps = target_fps
        self.stop_flag = False

    def run(self):
        """Override the run method to execute code in the thread."""
        frame_time = 1.0 / self.target_fps  # Time per frame in seconds

        self.stop_flag = False  # Reset stop flag

        while not self.stop_flag:
            frame_start_time = time.time()

            # Acquire the frame from the camera
            image = self.camera.acquire_image()

            # FPS calculation
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            self.frame_count += 1

            if elapsed_time >= 1.0:
                fps = self.frame_count / elapsed_time
                self.fps_updated.emit(fps)  # Emit signal to update FPS
                print(f"FPS: {fps}, target FPS: {self.target_fps}")
                self.start_time = current_time
                self.frame_count = 0
                if image is not None:
                    self.frame_received.emit(image.copy())  # Emit signal to send frame to the controller

            # Calculate the time taken to acquire the frame and adjust to hit target FPS
            frame_duration = time.time() - frame_start_time
            sleep_time = max(0.0, frame_time - frame_duration)  # Ensure we don’t sleep for a negative duration
            time.sleep(sleep_time)  # Sleep to hit target FPS

    def stop(self):
        self.stop_flag = True
        self.quit()  # Make sure to quit the QThread
        self.wait()  # Wait for the thread to finish

    def update_fps(self, fps):
        self.target_fps = fps

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

        # Create the worker thread
        self.worker_thread = CameraWorkerThread(camera)

        # Connect signals to the controller slots
        self.worker_thread.fps_updated.connect(self.update_fps)
        self.worker_thread.frame_received.connect(self.process_frame)

        target_fps = self.model.device_manager.loaded_devices[self.serial].target_fps
        self.worker_thread.update_fps(target_fps)
        self.worker_thread.start()  # This should start the thread and call `run`
        self.settings_dialog.show()


    def process_frame(self, image):
        """This method simulates acquiring a frame."""
        # Your frame acquisition logic here (e.g., from camera)
        #processing image

        self.settings_dialog.update_frame(image)

    def update_fps(self, fps):
        self.settings_dialog.update_fps(fps)

    def handle_settings_applied(self, settings):
        self.worker_thread.stop()
        self.model.device_manager.loaded_devices[self.serial].pause()
        self.model.device_manager.set_device_settings(self.serial, settings)
        target_fps = self.model.device_manager.loaded_devices[self.serial].target_fps
        self.worker_thread.update_fps(target_fps)
        self.worker_thread.start()
        print(f"Settings for device {settings} set.")