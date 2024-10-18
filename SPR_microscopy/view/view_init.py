from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QToolBar, QVBoxLayout, QTabWidget, QStatusBar, QWidget, QLabel, QHBoxLayout, \
    QSplitter

import tools
from view.modules.gui_central_widget import CentralWidgetGUI
from view.modules.right_bar import RightBarGUI


class View(QMainWindow):
    """
    Class for displaying and managing the main window
    """

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)

        self.right_bar_gui = None
        self.tabs = None
        self.tool_help = None
        self.tool_file_info = None

        self.central_widget_gui = CentralWidgetGUI()

        self.initUI()

    def initUI(self):
        """
        Initialization of all PyQT elements used in the window
        """

        # header of the main window and background of plots is in light colors to distinguish
        # between various instances of the application if they are running in parallel
        color = tools.generate_random_color_light()

        ################################################################################################################
        # Toolbar
        toolbar = QToolBar("Main toolbar")
        toolbar.setStyleSheet("background-color: {};".format(color))
        self.addToolBar(toolbar)

        # Toolbar - File info
        self.tool_file_info = QAction("File info", self)
        self.tool_file_info.setStatusTip("Info about loaded file.")
        toolbar.addAction(self.tool_file_info)
        self.tool_file_info.setDisabled(True)

        # Toolbar - Help
        self.tool_help = QAction("Help", self)
        self.tool_help.setStatusTip("[help]")
        toolbar.addAction(self.tool_help)

        ################################################################################################################
        # general layout of the gui (for now just one box)
        layout = QHBoxLayout()

        # Splitter to make the separation movable
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Central widget
        splitter.addWidget(self.central_widget_gui)

        # Right panel
        self.right_bar_gui = RightBarGUI()
        self.right_bar_gui.setMinimumWidth(200)
        splitter.addWidget(self.right_bar_gui)
        splitter.setStretchFactor(0, 7)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)

        ################################################################################################################
        # Status bar
        self.setStatusBar(QStatusBar(self))
        #self.statusBar().setMinimumSize(400, 40)
        self.statusBar().setStyleSheet("border :1px solid gray;")

        ################################################################################################################
        # Show Central Widget
        widget = QWidget()
        widget.setLayout(layout)
        #widget.setMinimumSize(600, 400)
        self.setCentralWidget(widget)

        ################################################################################################################
        # window title
        self.setWindowTitle("SPR Microscopy")
        # This line makes the window start maximized
        self.showMaximized()