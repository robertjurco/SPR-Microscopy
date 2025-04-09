import time

from PySide6.QtCore import QThread, Signal

class CameraWorkerThread(QThread):
    fps_updated = Signal(float)
    frame_received = Signal(object)

    def __init__(self, camera, target_fps = 60, FPS_averaging = 1.0):
        super().__init__()
        self.camera = camera
        self.start_time = time.time()
        self.target_fps = target_fps
        self.stop_flag = False
        self.FPS_averaging = FPS_averaging

    def run(self):
        """Override the run method to execute code in the thread."""
        frame_time = 1.0 / self.target_fps  # Time per frame in seconds

        self.stop_flag = False  # Reset stop flag

        frame_count = 0

        while not self.stop_flag:
            frame_start_time = time.time()

            # Acquire the frame from the camera
            image = self.camera.acquire_image()

            # FPS calculation
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            frame_count += 1

            if elapsed_time >= self.FPS_averaging:
                fps = frame_count / elapsed_time
                self.fps_updated.emit(fps)  # Emit signal to update FPS
                print(f"FPS: {fps}, target FPS: {self.target_fps}")
                self.start_time = current_time
                frame_count = 0
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

