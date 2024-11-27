from typing import Dict, Any

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from source.view.modules.tabs.gui_camera_speed import CameraSpeedGUI
from source.view.modules.tabs.gui_camera_view import CameraViewGUI
from source.view.modules.tabs.gui_imaging import ImaginingGUI
from source.view.modules.tabs.gui_spectroscopy import SpectroscopyGUI


class CentralWidgetGUI(QWidget):
    def __init__(self):
        super().__init__()

        # remember opened tabs
        # Dictionary to store connected devices with id number as key
        self.open_tab: Dict[str, Dict[str, Any]] = {}

        # class wise objects
        self.tabs = QTabWidget()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def add_camera_tab(self, serial):
        # Create new camera view
        new_camera_view = CameraViewGUI(serial=serial)

        # Connect to its socket
        new_camera_view.close.connect(self.close_camera_view)

        # Store the new camera view
        self.open_tab[serial] = {
                        'tab': new_camera_view,
                        'type': 'Camera_view',
                    }

        # Add the new tab
        self.tabs.addTab(new_camera_view, f'Camera {serial}')

        # Switch to the new tab
        self.tabs.setCurrentIndex(self.tabs.indexOf(new_camera_view))

    def add_tab(self,tab_type):
        new_tab = None
        index = self.find_next_index()

        if tab_type == "Imaging":
            new_tab = ImaginingGUI(index)
        elif tab_type == "Spectroscopy":
            new_tab = SpectroscopyGUI(index)
        elif tab_type == "Camera_FPS_meter":
            new_tab = CameraSpeedGUI(index)
        elif tab_type == "SPR_Microscopy":
            pass  # Placeholder
        else:
            print(f"Unknown tab type: {tab_type}")
            return

        if new_tab is not None:
            self.open_tab[f'{tab_type}_{index}'] = {
                'tab': new_tab,
                'type': tab_type,
            }

            self.tabs.addTab(new_tab, f'{tab_type} {index}')
            self.tabs.setCurrentIndex(self.tabs.indexOf(new_tab))
            new_tab.close.connect(self.close_tab)

    def find_next_index(self) -> int:
        return self.tabs.count()

    @Slot(int)
    def close_tab(self, index: int):
        widget = self.tabs.widget(index)
        if widget:
            for key, value in self.open_tab.items():
                if value['tab'] == widget:
                    del self.open_tab[key]
                    break
            widget.deleteLater()
            self.tabs.removeTab(index)


    @Slot(int, object)
    def set_image(self, idx, image):
        self.camera_views[idx].image_display.set_image(image)