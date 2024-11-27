from time import process_time_ns

from PySide6.QtCore import Slot, QThread

"""
Communication between Camera manager and camera GUI classes.
"""

class CameraPresenter:
    def __init__(self, model, view):
        self.threads = {}
        self.model = model
        self.view = view

        # Connect signals to slots
        # Search button
        self.view.right_bar_gui.camera_bar.search_button_pressed.connect(self.on_search_camera_button)

        # On initialization detect camera_models send reload gui
        self.reload_cameras()
        self.reload_connections()

    def reload_cameras(self):
        detected_cameras = self.model.camera_manager.detect_devices()
        info = self.model.camera_manager.get_all_cameras_info()
        self.view.right_bar_gui.camera_bar.reload(detected_cameras, info)

    def reload_connections(self):
        # We need to connect on every reload
        for i, camera_box in enumerate(self.view.right_bar_gui.camera_bar.scroll_area.device_boxes):
            camera_box.load_button_pressed.connect(lambda index=i: self.handle_load_button_pressed(index))
            camera_box.view_button_pressed.connect(lambda index=i: self.handle_view_button_pressed(index))
            camera_box.settings_button_pressed.connect(lambda index=i: self.handle_settings_button_pressed(index))
            camera_box.reload_button_pressed.connect(lambda index=i: self.handle_reload_button_pressed(index))
            camera_box.close_button_pressed.connect(lambda index=i: self.handle_close_button_pressed(index))

    @Slot()
    def on_search_camera_button(self):
        self.reload_cameras()
        self.reload_connections()

    @Slot(int)
    def handle_load_button_pressed(self, index):
        # Load camera with correct index
        # Hardware
        self.model.camera_manager.load_devices(index)

        # GUI
        self.view.right_bar_gui.camera_bar.load_device(index)


    @Slot(int)
    def handle_view_button_pressed(self, index):
        # init a view window in GUI
        self.view.central_widget_gui.add_camera_tab(index)

        # create an image acquisition link
        camera = self.model.camera_manager.loaded_devices[index]
        camera.frame_acquired.connect(lambda image, idx=index: self.view.central_widget_gui.set_image(idx, image))

        # call create new thread in camera manager
        self.model.camera_manager.start_image_acquisition_camera(index)

    @Slot(int)
    def handle_settings_button_pressed(self, index):
        settings = self.model.camera_manager.get_device_settings(index)
        self.view.right_bar_gui.settings_bar.fetch_camera_settings(index, settings)

    @Slot(int)
    def handle_reload_button_pressed(self, index):
        pass

    @Slot(int)
    def handle_close_button_pressed(self, index):
        # Close camera with correct index

        # Hardware
        self.model.camera_manager.close_device(index)

        # GUI
        camera = self.view.right_bar_gui.camera_bar.scroll_area.device_boxes[index]

        camera.status = "Not Loaded"

        camera.load_button.show()
        camera.view_button.hide()
        camera.settings_button.hide()
        camera.reload_button.hide()
        camera.close_button.hide()
