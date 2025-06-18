import cv2
from PySide6.QtCore import QTimer, QRect

from PySide6.QtGui import QPixmap, QImage, Qt, QPainter, QPen
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget, QListWidget, QPushButton


def filter_intensities(image, show_max_intensity=False, show_min_intensity=False):
    # Ensure the image is grayscale (2D)
    if len(image.shape) != 2:
        raise ValueError("Input must be a 2D grayscale image.")

    # Convert to 3-channel grayscale image
    color_image = cv2.merge([image, image, image])  # BGR format

    # Highlight 0-intensity pixels in blue if flag is on
    if show_min_intensity:
        zero_mask = (image == 0)
        color_image[zero_mask] = [255, 0, 0]  # Blue in BGR

    # Highlight 255-intensity pixels in red if flag is on
    if show_max_intensity:
        full_mask = (image == 255)
        color_image[full_mask] = [0, 0, 255]  # Red in BGR

    return color_image

class ImageDisplay(QWidget):
    def __init__(self, scale_factor: float = 0.5, preferred_width: int = None, preferred_height: int = None):
        super().__init__()
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

        self.current_image = None
        self.qimage = None  # Reusable QImage instance

        # Drawing features
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.drawn_rect = None
        self.roi_manager = None  # Set externally
        self.roi_added_callback = None

        self.label.mousePressEvent = self.mouse_press
        self.label.mouseMoveEvent = self.mouse_move
        self.label.mouseReleaseEvent = self.mouse_release

        self.cached_rgb_image = None  # Converted image, updated only on new frame
        self.overlay_image = None  # Cached image with persistent ROIs
        self.needs_overlay_redraw = True  # Flag to re-render overlay

    def update_image(self):
        if self.current_image is not None:
            image_to_display = self.current_image  # Default to original image

            # Handle scaling if scale_factor is provided and no preferred width/height
            if self.scale_factor != 1.0 and self.preferred_width is None and self.preferred_height is None:
                height, width = self.current_image.shape[:2]
                new_width = int(width * self.scale_factor)
                new_height = int(height * self.scale_factor)
                image_to_display = self.resize_image(self.current_image, new_width, new_height)

            # Handle resizing to exact preferred width/height if provided
            elif self.preferred_width is not None and self.preferred_height is not None:
                image_to_display = self.resize_image(self.current_image, self.preferred_width, self.preferred_height)

            # Display the resized image
            self.display_image()

    def display_image(self):
        if self.cached_rgb_image is None:
            return

        base_img = self.cached_rgb_image.copy()

        # === Re-render overlay if needed ===
        if self.roi_manager and self.needs_overlay_redraw:
            self.overlay_image = base_img.copy()
            for roi in self.roi_manager.rois.values():
                x, y, w, h = roi["x"], roi["y"], roi["width"], roi["height"]
                cv2.rectangle(self.overlay_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.needs_overlay_redraw = False

        # Start from cached overlay
        display_img = self.overlay_image.copy() if self.overlay_image is not None else base_img

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

            cv2.rectangle(display_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # === Apply final resizing (scaling or preferred size) ===
        img_to_show = display_img
        if self.preferred_width and self.preferred_height:
            img_to_show = self.resize_image(display_img, self.preferred_width, self.preferred_height)
        elif self.scale_factor != 1.0:
            h, w = display_img.shape[:2]
            img_to_show = self.resize_image(display_img, int(w * self.scale_factor), int(h * self.scale_factor))

        # === Convert to QImage and show ===
        height, width, channel = img_to_show.shape
        bytes_per_line = channel * width
        qimage = QImage(img_to_show.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        self.qimage = qimage
        self.label.setPixmap(QPixmap.fromImage(qimage))


    def resize_image(self, image, new_width, new_height):
        """ Resize the image to the new width and height """
        return cv2.resize(image, (new_width, new_height))

    def set_image(self, image, show_max_intensity=True, show_min_intensity=True):
        image = filter_intensities(image, show_max_intensity=show_max_intensity, show_min_intensity=show_min_intensity)
        self.current_image = image
        self.cached_rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # only once
        self.needs_overlay_redraw = True
        self.update_image()

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
            self.update_image()  # Triggers redraw including rectangle

    def mouse_release(self, event):
        if self.drawing:
            self.end_point = event.pos()
            self.drawing = False
            rect = QRect(self.start_point, self.end_point).normalized()
            self.drawn_rect = rect

            if self.qimage:
                scale_x = self.current_image.shape[1] / self.label.width()
                scale_y = self.current_image.shape[0] / self.label.height()

                x = int(rect.x() * scale_x)
                y = int(rect.y() * scale_y)
                w = int(rect.width() * scale_x)
                h = int(rect.height() * scale_y)

                roi_id = f"roi_{len(self.roi_manager.rois)+1}"
                roi = {"id": roi_id, "x": x, "y": y, "width": w, "height": h}
                self.roi_manager.new_ROI(roi)
                if self.roi_added_callback:
                    self.roi_added_callback()

                self.needs_overlay_redraw = True

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.drawn_rect:
            painter = QPainter(self.label)
            painter.setPen(QPen(Qt.red, 2, Qt.DashLine))
            painter.drawRect(self.drawn_rect)
            painter.end()

class ROIManagerWidget(QWidget):
    def __init__(self, roi_manager, image_display):
        super().__init__()
        self.roi_manager = roi_manager
        self.image_display = image_display

        self.image_display.roi_manager = roi_manager

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.roi_list = QListWidget()

        self.btn_delete_selected = QPushButton("Delete Selected ROI")
        self.btn_delete_all = QPushButton("Delete All ROIs")

        layout.addWidget(QLabel("Defined ROIs:"))
        layout.addWidget(self.roi_list)
        layout.addWidget(self.btn_delete_selected)
        layout.addWidget(self.btn_delete_all)

        self.setLayout(layout)

        # Connect buttons
        self.btn_delete_selected.clicked.connect(self.delete_selected_roi)
        self.btn_delete_all.clicked.connect(self.delete_all_rois)

        # Refresh ROI list when updated externally
        self.image_display.roi_added_callback = self.refresh_list

    def delete_selected_roi(self):
        selected_items = self.roi_list.selectedItems()
        for item in selected_items:
            roi_id = item.text()
            self.roi_manager.delete_ROI(roi_id)
        self.image_display.needs_overlay_redraw = True
        self.refresh_list()

    def delete_all_rois(self):
        self.roi_manager.delete_all_ROI()
        self.image_display.needs_overlay_redraw = True
        self.refresh_list()

    def refresh_list(self):
        self.roi_list.clear()
        for roi_id in self.roi_manager.rois.keys():
            self.roi_list.addItem(roi_id)