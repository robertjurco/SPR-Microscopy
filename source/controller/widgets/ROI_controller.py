from PySide6.QtCore import QObject, Signal


class ROIController(QObject):
    stop_camera_thread = Signal()
    start_camera_thread = Signal()

    def __init__(self, model, serial, roi_widget, image_display):
        super().__init__()
        self.rois = {}  # Dict of {id: region_dict}

        self.model = model
        self.serial = serial

        self.roi_widget = roi_widget
        self.roi_widget.delete_ROI.connect(self.delete_ROI)
        self.roi_widget.delete_all_ROI.connect(self.delete_all_ROI)
        self.roi_widget.modify_ROI.connect(self.modify_ROI)
        self.roi_widget.apply_changes.connect(self.set_ROI_settings)

        self.image_display = image_display
        self.image_display.add_ROI.connect(self.new_ROI)

        self.current_woi = (0, 0, self.image_display.width, self.image_display.height)

    def new_ROI(self, roi_array):
        x, y, w, h = roi_array

        # Auto-generate a unique string ID starting from "0"
        region_id = 0
        while str(region_id) in self.rois:
            region_id += 1
        region_id = str(region_id)

        self.rois[region_id] = {
            "x": x,
            "y": y,
            "width": w,
            "height": h
        }

        self.image_display.update_ROI_dict(self.rois)
        self.roi_widget.refresh_list(self.rois)

    def delete_ROI(self, roi_id: str):
        if roi_id in self.rois:
            self.rois.pop(roi_id)
            self.roi_widget.refresh_list(self.rois)

    def delete_all_ROI(self):
        self.rois.clear()

        self.roi_widget.refresh_list(self.rois)

    def modify_ROI(self, data):
        roi_id, updated_roi = data
        if roi_id in self.rois:
            self.rois[roi_id] = updated_roi
            self.image_display.update_ROI_dict(self.rois)
            self.roi_widget.refresh_list(self.rois)

    def process_ROI(self, image):
        if not self.rois:
            # No ROIs defined: return the whole image with a default ID
            return [("full_image", image.copy())]

        cropped_images = []
        for roi_id, region in self.rois.items():
            x, y = region["x"], region["y"]
            w, h = region["width"], region["height"]

            # Ensure coordinates are within image bounds
            x1, y1 = max(0, x), max(0, y)
            x2, y2 = min(image.shape[1], x + w), min(image.shape[0], y + h)

            cropped = image[y1:y2, x1:x2]
            cropped_images.append((roi_id, cropped))

        return cropped_images

    def required_woi(self):
        if not self.rois:
            return (0, 0, self.image_display.width, self.image_display.height) # no ROI

        # Calculate required WOI settings
        min_x = min(region["x"] for region in self.rois.values())
        min_y = min(region["y"] for region in self.rois.values())
        max_x = max(region["x"] + region["width"] for region in self.rois.values())
        max_y = max(region["y"] + region["height"] for region in self.rois.values())

        required_offset_x = min_x
        required_offset_y = min_y
        required_width = max_x - min_x
        required_height = max_y - min_y

        # === Get allowed WOI constraints from the camera ===
        camera_settings = self.model.device_manager.get_device_settings(self.serial)
        woi_limits = camera_settings['woi']['min_max']

        offset_x_min, offset_x_max = woi_limits['offsetX']
        offset_y_min, offset_y_max = woi_limits['offsetY']
        min_width, max_width = woi_limits['width']
        min_height, max_height = woi_limits['height']

        # Clamp offsets first
        clamped_offset_x = max(offset_x_min, min(required_offset_x, offset_x_max))
        clamped_offset_y = max(offset_y_min, min(required_offset_y, offset_y_max))

        # Adjust width/height to still cover the same area if offset was shifted
        delta_x = required_offset_x - clamped_offset_x
        delta_y = required_offset_y - clamped_offset_y

        adjusted_width = required_width + delta_x
        adjusted_height = required_height + delta_y

        clamped_width = max(min_width, min(adjusted_width, max_width))
        clamped_height = max(min_height, min(adjusted_height, max_height))

        return (clamped_offset_x, clamped_offset_y, clamped_width, clamped_height)

    def set_ROI_settings(self):
        woi = self.required_woi() # Needs to be extended for all Serials
        woi_settings = { 'woi': woi }

        self.stop_camera_thread.emit()

        self.model.device_manager.set_device_settings(self.serial, woi_settings)

        # === NEW: Save currently applied WOI ===
        self.current_woi = woi
        self.image_display.current_woi = woi

        self.start_camera_thread.emit()

