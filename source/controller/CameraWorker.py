import time
from threading import Lock

from PySide6.QtCore import QThread, Signal

class CameraWorkerThread(QThread):
    fps_updated = Signal(float)
    frame_received = Signal(object)
    frame_received_6FPS = Signal(object)

    def __init__(self, camera, target_fps = 60, FPS_averaging = 1.0):
        super().__init__()
        self.camera = camera
        self.start_time = time.time()
        self._last_emit_6fps = time.time()
        self.target_fps = target_fps
        self._stop_flag = False
        self._lock = Lock()  # New: Lock for thread-safe flag access
        self.FPS_averaging = FPS_averaging

    def run(self):
        """Override the run method to execute code in the thread."""
        frame_time = 1.0 / self.target_fps  # Time per frame in seconds
        frame_count = 0

        while True:
            frame_start_time = time.time()  # <-- add this line here

            with self._lock:
                if self._stop_flag:
                    break

            # Acquire the frame from the camera
            image = self.camera.acquire_image()
            if image is not None:
                #images = self.camera.process_ROI(image.copy())
                self.frame_received.emit(image)

            # FPS calculation
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            frame_count += 1

            if elapsed_time >= self.FPS_averaging:
                fps = frame_count / elapsed_time
                self.fps_updated.emit(fps)  # Emit signal to update FPS
                self.start_time = current_time
                frame_count = 0

            if current_time - self._last_emit_6fps >= 1 / 6:
                if image is not None:
                    self.frame_received_6FPS.emit(image.copy())
                self._last_emit_6fps = current_time

            # Calculate the time taken to acquire the frame and adjust to hit target FPS
            frame_duration = time.time() - frame_start_time
            sleep_time = max(0.0, frame_time - frame_duration)  # Ensure we don’t sleep for a negative duration
            self.interruptible_sleep(sleep_time)

    def interruptible_sleep(self, duration):
        """Sleep in small chunks and check stop_flag to allow fast thread termination."""
        sleep_interval = 0.01  # 10 ms
        elapsed = 0
        while elapsed < duration:
            with self._lock:
                if self._stop_flag:
                    break
            remaining = duration - elapsed
            to_sleep = min(sleep_interval, remaining)
            self.msleep(int(to_sleep * 1000))  # QThread.msleep expects milliseconds
            elapsed += to_sleep

    def stop(self):
        with self._lock:
            self._stop_flag = True
        self.quit()
        if self.isRunning():
            self.wait()

    def update_fps(self, fps):
        self.target_fps = fps

