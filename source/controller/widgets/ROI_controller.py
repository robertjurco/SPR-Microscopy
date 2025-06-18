
class ROIController:
    def __init__(self, model, serial, roi_widget, image_display):
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
        for region in self.rois.values():
            x, y = region["x"], region["y"]
            w, h = region["width"], region["height"]

            # Ensure coordinates are within image bounds
            x1, y1 = max(0, x), max(0, y)
            x2, y2 = min(image.shape[1], x + w), min(image.shape[0], y + h)

            cropped = image[y1:y2, x1:x2]
            cropped_images.append((region["id"], cropped))

        return cropped_images

    def required_woi(self):
        if not self.rois:
            return None # no ROI

        min_x = min(region["x"] for region in self.rois.values())
        min_y = min(region["y"] for region in self.rois.values())
        max_x = max(region["x"] + region["width"] for region in self.rois.values())
        max_y = max(region["y"] + region["height"] for region in self.rois.values())

        width = max_x - min_x
        height = max_y - min_y

        return (min_x, min_y, width, height)

    def set_ROI_settings(self):
        woi = self.required_woi() # Needs to be extended for all Serials
        woi_settings = { 'woi': woi }
        print(woi_settings)

        self.model.device_manager.set_device_settings(self.serial, woi_settings)

