from PySide6.QtCore import QThreadPool

from source.controller.controller_StartUpWindow import StartUpWindowController


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.threadpool = QThreadPool()

        self.start_up_window_controller = StartUpWindowController(model, view, self.threadpool)