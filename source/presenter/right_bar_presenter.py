from PySide6.QtCore import Slot


class RightBarPresenter:
    def __init__(self, model, view):
        self.threads = {}
        self.model = model
        self.view = view

        # Connect signals to slots
        # Search button
        self.view.right_bar_gui.search_button_clicked.connect(self.on_search_button)
        # Load button
        self.view.right_bar_gui.load_all_button_clicked.connect(self.on_load_button)
        # Button signals
        self.view.right_bar_gui.button_signal.connect(self.handle_button_signal)


        # On initialization detect camera_models send reload gui
        #self.reload_devices()

    def reload_devices(self):
        self.model.device_manager.auto_detect_devices()
        connected_devices = self.model.device_manager.list_connected_devices()

        self.view.right_bar_gui.test_reload(connected_devices)

    def on_search_button(self):
        self.reload_devices()

    def on_load_button(self):
        pass

    @Slot(str, str, str)
    def handle_button_signal(self, button_name, serial, device_type):
        # send signal to device manager
        self.model.device_manager.handle_button_signal(button_name, serial, device_type)

        match device_type:
            case "camera":
                self.handle_camera_button_signal(button_name, serial, device_type)
            case "motion_control":
                self.handle_motion_control_button_signal(button_name, serial, device_type)
            case "slm":
                self.handle_slm_button_signal(button_name, serial, device_type)

            # If an exact match is not confirmed, this last case will be used if provided
            case _:
                print("Something's wrong with the button click")

        print(f"Button Pressed: {button_name}, Serial: {serial}, Type: {device_type}")


    def handle_camera_button_signal(self, button_name, serial, device_type):
        match button_name:
            case "View":
                self.view.central_widget_gui.add_camera_tab(serial)

                # create an image acquisition link
                camera = self.model.device_manager.loaded_devices[serial]
                camera.frame_acquired.connect(lambda image, idx=serial: self.view.central_widget_gui.set_image(idx, image))

    def handle_motion_control_button_signal(self, button_name, serial, device_type):
        pass

    def handle_slm_button_signal(self, button_name, serial, device_type):
        pass