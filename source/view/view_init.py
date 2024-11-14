from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QToolBar, QStatusBar, QWidget, QHBoxLayout, QSplitter
import source.tools as tools
from source.view.modules.gui_central_widget import CentralWidgetGUI
from source.view.modules.right_bar import RightBarGUI


class View(QMainWindow):
    """
    A class used to represent the View.
    """

    def __init__(self):
        """
        Initialize the View class.
        This method sets up initial values for the toolbar actions and central widget.
        """
        super(View, self).__init__()
        self.right_bar_gui = None
        self.tabs = None
        self.tool_help = None
        self.tool_file_info = None
        self.central_widget_gui = None
        self.init_ui()

    def init_ui(self):
        """
        Initialization of all PyQT elements used in the window.
        """
        color = tools.generate_random_color_light()
        self.setup_toolbar(color)
        self.setup_layout()
        self.setup_status_bar()
        self.setWindowTitle("SPR Microscopy")
        self.showMaximized()

    def setup_toolbar(self, color):
        """
        Setup the toolbar for the main window.
        :param color: Background color for the toolbar
        """
        toolbar = QToolBar("Main toolbar")
        toolbar.setStyleSheet(f"background-color: {color};")
        self.addToolBar(toolbar)

        self.tool_file_info = QAction("File info", self)
        self.tool_file_info.setStatusTip("Info about loaded file.")
        toolbar.addAction(self.tool_file_info)
        self.tool_file_info.setDisabled(True)

        self.tool_help = QAction("Help", self)
        self.tool_help.setStatusTip("[help]")
        toolbar.addAction(self.tool_help)

    def setup_layout(self):
        """
        Setup the main layout of the GUI.
        """
        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.central_widget_gui = CentralWidgetGUI()
        splitter.addWidget(self.central_widget_gui)

        self.right_bar_gui = RightBarGUI()
        self.right_bar_gui.setMinimumWidth(200)
        splitter.addWidget(self.right_bar_gui)

        splitter.setStretchFactor(0, 7)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setup_status_bar(self):
        """
        Setup the status bar for the main window.
        """
        self.setStatusBar(QStatusBar(self))
        self.statusBar().setStyleSheet("border: 1px solid gray;")