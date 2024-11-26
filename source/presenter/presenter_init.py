from PySide6.QtCore import QThreadPool

from source.presenter.right_bar_presenter import RightBarPresenter


class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.threadpool = QThreadPool()

        self.right_bar_presenter = RightBarPresenter(model, view)