import numpy as np
from PySide6.QtCore import Qt, Signal, QTimer, QRect
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QFormLayout, QDialog, QHBoxLayout, \
    QSizePolicy, QLayout, QDoubleSpinBox, QListWidget
import cv2  # OpenCV for resizing

def filter_intensities(image, show_max_intensity=False, show_min_intensity=False):
    # Ensure the image is grayscale (2D)
    if len(image.shape) != 2:
        raise ValueError("Input must be a 2D grayscale image.")

    # Convert to 3-channel grayscale image
    color_image = cv2.merge([image, image, image])  # BGR format

    # Highlight 0-intensity pixels in blue if flag is on
    if show_min_intensity:
        zero_mask = (image == 255)
        color_image[zero_mask] = [255, 0, 0]  # Blue in BGR

    # Highlight 255-intensity pixels in red if flag is on
    if show_max_intensity:
        full_mask = (image == 0)
        color_image[full_mask] = [0, 0, 255]  # Red in BGR

    return color_image

class ImageDisplay(QWidget):
    add_ROI = Signal(list)
    test = Signal()


    def __init__(self, width, height, scale_factor: float = 0.5, preferred_width: int = None, preferred_height: int = None):
        super().__init__()

        self.width = width
        self.height = height

        self.label = QLabel(self)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Store the scaling parameters
        self.scale_factor = scale_factor
        self.preferred_width = preferred_width
        self.preferred_height = preferred_height

        # Ensure that only one parameter is set: either scale_factor or preferred dimensions
        if (self.scale_factor != 1.0 and self.preferred_width is not None and self.preferred_height is not None):
            print(
                "Warning: Both scaling factor and preferred width/height provided. Using preferred width/height instead.")

        # Timer for updating the image at 60 FPS
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_image)
        self.timer.start(1000.0 / 60)  # 60 FPS

        self.current_image = None
        self.qimage = None  # Reusable QImage instance

        # Drawing features
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.drawn_rect = None
        self.roi_added_callback = None

        self.label.mousePressEvent = self.mouse_press
        self.label.mouseMoveEvent = self.mouse_move
        self.label.mouseReleaseEvent = self.mouse_release

        self.rois = None


    def display_image(self):
        if self.current_image is None:
            return

        base_img = self.current_image

        # === Re-render overlay if needed ===
        if self.rois is not None:
            for roi in self.rois.values():
                x, y, w, h = roi["x"], roi["y"], roi["width"], roi["height"]
                cv2.rectangle(base_img, (x, y), (x + w, y + h), (51, 255, 0), 2)

        # === Draw dragging rectangle if present ===
        if self.drawing and self.start_point and self.end_point:
            # Scale mouse coords to image space
            label_width = self.label.width()
            label_height = self.label.height()
            img_height, img_width = self.current_image.shape[:2]

            scale_x = img_width / label_width
            scale_y = img_height / label_height

            x1 = int(self.start_point.x() * scale_x)
            y1 = int(self.start_point.y() * scale_y)
            x2 = int(self.end_point.x() * scale_x)
            y2 = int(self.end_point.y() * scale_y)

            cv2.rectangle(base_img, (x1, y1), (x2, y2), (51, 255, 0), 2)


        # === Apply final resizing (scaling or preferred size) ===
        img_to_show = base_img
        if self.preferred_width and self.preferred_height:
            img_to_show = self.resize_image(base_img, self.preferred_width, self.preferred_height)
        elif self.scale_factor != 1.0:
            h, w = base_img.shape[:2]
            img_to_show = self.resize_image(base_img, int(w * self.scale_factor), int(h * self.scale_factor))

        # === Convert to QImage and show ===
        height, width, channel = img_to_show.shape
        bytes_per_line = channel * width
        qimage = QImage(img_to_show.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        self.qimage = qimage
        self.label.setPixmap(QPixmap.fromImage(qimage))

    def resize_image(self, image, new_width, new_height):
        """ Resize the image to the new width and height """
        return cv2.resize(image, (new_width, new_height))

    def set_image(self, image, show_max_intensity, show_min_intensity):
        image = filter_intensities(image, show_max_intensity=show_max_intensity, show_min_intensity=show_min_intensity)
        self.current_image = image
        self.display_image()

    def set_image_from_file(self, file_path):
        pixmap = QPixmap(file_path)
        self.label.setPixmap(pixmap)

    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_point = event.pos()
            self.end_point = self.start_point

    def mouse_move(self, event):
        if self.drawing:
            self.end_point = event.pos()
            #self.display_image()  # Triggers redraw including rectangle

    def mouse_release(self, event):
        if self.drawing:
            self.end_point = event.pos()
            self.drawing = False
            rect = QRect(self.start_point, self.end_point).normalized()

            if self.qimage:
                label_width = self.label.width()
                label_height = self.label.height()

                scale_x = self.width / label_width
                scale_y = self.height / label_height

                # Clamp rectangle coordinates to within QLabel size
                x1 = max(0, min(rect.left(), label_width))
                y1 = max(0, min(rect.top(), label_height))
                x2 = max(0, min(rect.right(), label_width))
                y2 = max(0, min(rect.bottom(), label_height))

                # Map from label space to image space
                x_img = int(x1 * scale_x)
                y_img = int(y1 * scale_y)
                w_img = int((x2 - x1) * scale_x)
                h_img = int((y2 - y1) * scale_y)

                # Final clamp in image space (safety)
                x_img = max(0, min(x_img, self.width))
                y_img = max(0, min(y_img, self.height))
                w_img = max(1, min(w_img, self.width - x_img))
                h_img = max(1, min(h_img, self.height - y_img))

                roi_array = [x_img, y_img, w_img, h_img]
                self.add_ROI.emit(roi_array)

    def update_ROI_dict(self, rois):
        self.rois = rois
