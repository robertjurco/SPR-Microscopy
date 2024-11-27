from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QMainWindow, QPushButton, QWidget, QSizePolicy


class ImageDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1000.0 / 60)  # 60 FPS
        self.current_image = None
        self.qimage = None  # Reusable QImage instance

    def update_image(self):
        if self.current_image is not None:
            # Check if the image is grayscale
            if len(self.current_image.shape) == 2:  # Grayscale image
                height, width = self.current_image.shape
                bytes_per_line = width  # One byte per pixel for grayscale
                qimage = QImage(self.current_image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
                self.label.setPixmap(QPixmap.fromImage(qimage))
            elif len(self.current_image.shape) == 3:  # Color image
                height, width, channel = self.current_image.shape
                bytes_per_line = channel * width

                if channel == 3:  # Assuming RGB
                    qimage = QImage(self.current_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                    self.label.setPixmap(QPixmap.fromImage(qimage))
                else:
                    print("Unsupported channel count.")
                    return
            else:
                print("Invalid image shape:", self.current_image.shape)


    def set_image(self, image):
        self.current_image = image
        self.update_image()

    def set_image_from_file(self, file_path):
        pixmap = QPixmap(file_path)
        self.label.setPixmap(pixmap)

class CameraViewGUI(QWidget):
    close = Signal(int)

    def __init__(self, serial):
        super().__init__()

        # which camera are we viewing
        self.detached_window = None
        self.serial = serial

        # Close button
        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(lambda: self.close.emit(serial))

        # Detach button
        self.detach_button = QPushButton('Detach', self)
        self.detach_button.clicked.connect(self.detach)

        # display
        self.image_display = ImageDisplay()
        #self.image_display.set_image_from_file('C:/Users/jurco/Desktop/images.png')

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