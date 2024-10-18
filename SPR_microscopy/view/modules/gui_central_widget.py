from PySide6.QtCore import QTimer, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QPushButton, QHBoxLayout, QMainWindow


class ImageDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1000 / 60)  # 60 FPS
        self.current_image = None

    def update_image(self):
        if self.current_image is not None:
            height, width, channel = self.current_image.shape
            bytes_per_line = channel * width
            qimage = QImage(self.current_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qimage))

    def set_image(self, image):
        self.current_image = image

    def set_image_from_file(self, file_path):
        pixmap = QPixmap(file_path)
        self.label.setPixmap(pixmap)

class CameraViewGUI(QWidget):
    close = Signal(int)

    def __init__(self, camera_index):
        super().__init__()

        # which camera are we viewing
        self.detached_window = None
        self.camera_index = camera_index

        # Close button
        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(lambda: self.close.emit(camera_index))

        # Detach button
        self.detach_button = QPushButton('Detach', self)
        self.detach_button.clicked.connect(self.detach)

        # display
        self.image_display = ImageDisplay()
        self.image_display.set_image_from_file('C:/Users/jurco/Desktop/images.png')

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel('Camera Widget')
        layout.addWidget(label)

        layout.addWidget(self.image_display)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.detach_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def detach(self):
        self.detached_window = QMainWindow()
        self.detached_window.setCentralWidget(self)
        self.detached_window.show()

class CentralWidgetGUI(QWidget):
    def __init__(self):
        super().__init__()

        # remember opened tabs
        self.camera_views = []
        self.spectroscopy_views = []

        # class wise objects
        self.tabs = QTabWidget()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(self.tabs)

        self.setLayout(layout)


    def add_camera_tab(self, camera_index):
        # Create new camera view
        new_camera_view = CameraViewGUI(camera_index = camera_index)

        # Connect to its socket
        new_camera_view.close.connect(self.close_camera_view)

        self.camera_views.append(new_camera_view)
        self.tabs.addTab(new_camera_view, f'Camera {camera_index}')

    def remove_current_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            widget = self.tabs.widget(current_index)
            if widget is not None:
                widget.deleteLater()
            self.tabs.removeTab(current_index)
            if current_index < len(self.camera_views):
                del self.camera_views[current_index]
            else:
                del self.spectroscopy_views[current_index - len(self.camera_views)]

    @Slot(int)
    def close_camera_view(self, index):
        print("closing camera")
        if 0 <= index < len(self.camera_views):
            widget = self.camera_views.pop(index)
            if widget is not None:
                widget.deleteLater()

    def close_spectroscopy_view(self, index):
        print("closing spectroscopy")
        if 0 <= index < len(self.spectroscopy_views):
            widget = self.spectroscopy_views.pop(index)
            if widget is not None:
                widget.deleteLater()
