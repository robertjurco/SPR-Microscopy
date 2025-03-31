from source.view.tabs.view_imaging import ImagingView

class ImagingController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Create an instance of the ImagingView and show it
        self.imaging_view = ImagingView()
        self.imaging_view.show()