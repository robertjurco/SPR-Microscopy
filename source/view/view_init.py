from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QToolBar, QStatusBar, QWidget, QHBoxLayout, QSplitter, QMenu
import source.tools as tools
from source.view.modules.gui_central_widget import CentralWidgetGUI
from source.view.modules.right_bar import RightBarGUI


class View(QMainWindow):
    """
    A class used to represent the View.
    """
    open_tab_signal = Signal(str)

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

        # Adding File info to the toolbar
        self.tool_file_info = QAction("File info", self)
        self.tool_file_info.setStatusTip("Info about loaded file.")
        toolbar.addAction(self.tool_file_info)
        self.tool_file_info.setDisabled(True)

        # Adding Open menu
        open_menu = QMenu("Open", self)

        self.add_actions(open_menu, "Imaging", "Imaging")
        self.add_actions(open_menu, "Spectroscopy", "Spectroscopy")
        self.add_actions(open_menu, "Camera FPS meter", "Camera_FPS_meter")
        self.add_actions(open_menu, "SPR Microscopy", "SPR_Microscopy")

        # Adding the Open menu to the toolbar
        open_menu_button = QAction("Open", self)
        open_menu_button.setMenu(open_menu)
        toolbar.addAction(open_menu_button)

        # Adding Help to the toolbar
        self.tool_help = QAction("Help", self)
        self.tool_help.setStatusTip("[help]")
        toolbar.addAction(self.tool_help)

    def add_actions(self, menu, action_name, message_name):
        action = QAction(action_name, self)
        action.triggered.connect(lambda checked, m=message_name: self.emit_option_selected(m))
        menu.addAction(action)

    def emit_option_selected(self, message):
        self.open_tab_signal.emit(message)

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