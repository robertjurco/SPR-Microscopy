from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMainWindow
from PySide6.QtCore import Signal


class TabGUI(QWidget):
    close = Signal(int)

    def __init__(self, index):
        super().__init__()
        self.content_layout = None
        self.detached_window = None
        self.index = index

        # Close button
        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(lambda: self.close.emit(index))

        # Detach button
        self.detach_button = QPushButton('Detach', self)
        self.detach_button.clicked.connect(self.detach)

        # Initialize UI
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Create a button layout and align buttons to the right
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add stretch to push buttons to the right
        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.detach_button)

        main_layout.addLayout(button_layout)

        # Create an empty layout for the derived classes to add their widgets
        self.content_layout = QVBoxLayout()
        main_layout.addLayout(self.content_layout)

        self.setLayout(main_layout)

    def detach(self):
        self.detached_window = QMainWindow()
        self.detached_window.setCentralWidget(self)
        self.detached_window.show()
