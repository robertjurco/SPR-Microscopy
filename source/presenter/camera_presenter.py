from PySide6.QtCore import Slot, QThread

"""
Communication between Camera manager and camera GUI classes.
"""

class CameraPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect signals to slots
        # Search button
        self.view.right_bar_gui.camera_bar.search_button_pressed.connect(self.on_search_camera_button)

        # On initialization detect cameras send reload gui
        self.reload_cameras()
        self.reload_connections()

    def reload_cameras(self):
        detected_cameras = self.model.camera_manager.detect_cameras()
        info = self.model.camera_manager.get_all_cameras_info()
        self.view.right_bar_gui.camera_bar.reload(detected_cameras, info)

    def reload_connections(self):
        # We need to connect on every reload
        for i, camera_box in enumerate(self.view.right_bar_gui.camera_bar.scroll_area.camera_boxes):
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
        self.model.camera_manager.load_camera(index)
        # GUI
        self.view.right_bar_gui.camera_bar.load_camera(index)


    @Slot(int)
    def handle_view_button_pressed(self, index):
        # init a view window in GUI
        self.view.central_widget_gui.add_camera_tab(index)

        # create an image acquisition link
        self.model.camera_manager.loaded_cameras[index].frame_acquired.connect(self.view.central_widget_gui.camera_tab[index].set_image)

        self.thread = QThread()
        self.model.camera_manager.loaded_cameras[index].moveToThread(self.thread)
        self.thread.started.connect(self.model.camera_manager.loaded_cameras[index].run)

    @Slot(int)
    def handle_settings_button_pressed(self, index):
        pass

    @Slot(int)
    def handle_reload_button_pressed(self, index):
        pass

    @Slot(int)
    def handle_close_button_pressed(self, index):
        # Close camera with correct index

        # Hardware
        self.model.camera_manager.close_camera(index)

        # GUI
        camera = self.view.right_bar_gui.camera_bar.scroll_area.camera_boxes[index]

        camera.status = "Not Loaded"

        camera.load_button.show()
        camera.view_button.hide()
        camera.settings_button.hide()
        camera.reload_button.hide()
        camera.close_button.hide()
