from PySide6.QtCore import QThreadPool

from source.presenter.camera_presenter import CameraPresenter


class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.threadpool = QThreadPool()

        self.cameraPresenter = CameraPresenter(model, view)