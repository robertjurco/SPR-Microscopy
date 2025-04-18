from source.controller.CameraWorker import CameraWorkerThread
from source.view.settings.view_settings_camera import ViewCameraSettings

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