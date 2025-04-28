from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QColor, QPalette, QFont
from PySide6.QtWidgets import QMainWindow, QToolBar, QStatusBar, QWidget, QHBoxLayout, QSplitter, QMenu, QVBoxLayout, \
    QTabWidget, QLabel, QPushButton, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QHeaderView, \
    QAbstractItemView, QDialog
from functools import partial
from typing import Dict, Any


class StartUpWindow(QMainWindow):
    """
    A class used to represent the View.
    """

    # Define the signal
    device_activate_click = Signal(str, bool)
    on_settings_clicked = Signal(str)
    new_project = Signal(str)

    def __init__(self):
        """
        Initialize the View class.
        This method sets up initial values for the toolbar actions and central widget.
        """
        super().__init__()

        self.setWindowTitle("SPR UP 2")

        self.connected_devices = {}

        # Set up the central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Set a consistent font for the whole window
        font = QFont("Arial", 10)  # You can adjust the font name and size here
        self.setFont(font)

        # Create QTabWidget for tabs
        tab_widget = QTabWidget()

        # Create and populate the tabs
        tab1 = QWidget()
        self.tab1_widget = self.fill_tab_Available_Devices(tab1)

        tab2 = QWidget()
        self.fill_tab_Active_Projects(tab2)

        tab3 = QWidget()
        self.fill_tab_Active_Threads(tab3)

        # Add the tabs to the tab widget
        tab_widget.addTab(tab1, "Available Devices")
        tab_widget.addTab(tab2, "Active Projects")
        tab_widget.addTab(tab3, "Active Threads")

        # Set a dark brown background color behind the tabs
        #tab_widget.setAutoFillBackground(True)
        #tab_widget.setPalette(palette)

        # Set font for the tab widget
        tab_widget.setStyleSheet("QTabWidget::pane { border: 1px solid #4a2c1f; }")  # Optional style for tabs
        tab_widget.setFont(font)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Create buttons
        new_project_button = QPushButton("New Project")
        open_project_button = QPushButton("Open Project")
        reload_button = QPushButton("Reload")
        about_button = QPushButton("About")
        exit_button = QPushButton("Exit")

        # Set a fixed size for each button
        new_project_button.setFixedSize(110, 30)
        open_project_button.setFixedSize(100, 30)
        reload_button.setFixedSize(100, 30)
        about_button.setFixedSize(100, 30)
        exit_button.setFixedSize(100, 30)

        # Create a spacer to push the buttons to the right
        spacer = QSpacerItem(100, 30, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Add spacer and buttons to the layout
        button_layout.addItem(spacer)
        button_layout.addWidget(new_project_button)
        button_layout.addWidget(open_project_button)
        button_layout.addWidget(reload_button)
        button_layout.addWidget(about_button)
        button_layout.addWidget(exit_button)

        # Add the tab widget and buttons layout to the main layout
        layout.addWidget(tab_widget)
        layout.addLayout(button_layout)

        # Set the layout to the central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Automatically adjust the window size to fit the contents
        self.setMinimumSize(750, 200)  # Increase this to fit everything nicely
        self.adjustSize()

        # Create the QMenu for "New Project" dropdown
        self.project_menu = QMenu(new_project_button)
        # Use lambda to delay the function call
        self.project_menu.addAction("Imaging", lambda: self.select_project("Imaging"))
        self.project_menu.addAction("Spectroscopy", lambda: self.select_project("Spectroscopy"))
        self.project_menu.addAction("Camera FPS meter", lambda: self.select_project("Camera_FPS_meter"))
        self.project_menu.addAction("SLM", lambda: self.select_project("SLM"))

        # Connect the "New Project" button to show the menu
        new_project_button.setMenu(self.project_menu)

    def select_project(self, project_type):
        """ Handle selection of Project A """
        self.new_project.emit(project_type)

    def fill_tab_Available_Devices(self, tab_widget):
        """Fill the content of Tab 1 (Available Devices)."""
        layout = QVBoxLayout()

        # Create the table widget
        table_widget = QTableWidget()

        # Remove the margins and borders between tab and table
        table_widget.setStyleSheet("QTableWidget { border: none; margin: 0px; padding: 0px; }")

        layout.addWidget(table_widget)

        # Hide the row headers to remove row numbers
        table_widget.verticalHeader().setVisible(False)

        # Set up the table with 5 columns: Model, Vendor, Serial, Project, and Activation
        table_widget.setColumnCount(5)
        table_widget.setHorizontalHeaderLabels(['Model', 'Vendor', 'Serial', 'Project', 'Activation'])

        # Adjust column width for readability
        table_widget.setColumnWidth(0, 150)
        table_widget.setColumnWidth(1, 150)
        table_widget.setColumnWidth(2, 150)
        table_widget.setColumnWidth(3, 150)
        table_widget.setColumnWidth(4, 100)

        # Make the last column non-resizable
        table_widget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)

        # Enable row selection
        table_widget.setSelectionMode(QTableWidget.NoSelection)
        table_widget.setSelectionBehavior(QTableWidget.SelectItems)

        # Load devices (example data)
        devices = [
            {"model": "Camera X1", "vendor": "Vendor A", "serial": "12345", "project": "Project Alpha"},
            {"model": "SLM Y2", "vendor": "Vendor B", "serial": "67890", "project": "Project Beta"},
            {"model": "Motion Control Z3", "vendor": "Vendor C", "serial": "11223", "project": "Project Gamma"}
        ]

        # Set the row count based on the number of devices
        table_widget.setRowCount(len(devices))

        # Add devices to the table
        for row, device in enumerate(devices):
            table_widget.setItem(row, 0, QTableWidgetItem(device["model"]))
            table_widget.setItem(row, 1, QTableWidgetItem(device["vendor"]))
            table_widget.setItem(row, 2, QTableWidgetItem(device["serial"]))
            table_widget.setItem(row, 3, QTableWidgetItem(device["project"]))

            # Create an activation button for the last column
            activate_button = QPushButton("Activate")
            activate_button.setProperty("activated", False)
            activate_button.setFixedSize(100, 30)
            # Connect the activation button to a handler function
            activate_button.clicked.connect(partial(self.toggle_activation, table_widget, row))
            table_widget.setCellWidget(row, 4, activate_button)

        # Set the layout of the tab
        tab_widget.setLayout(layout)

        # Enable right-click context menu
        table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        table_widget.customContextMenuRequested.connect(self.show_context_menu)

        # Set size policy of table to expand to fill space
        #table_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #table_widget.horizontalHeader().setStretchLastSection(True)
        #table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        #table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Apply the same font to the table
        table_widget.setFont(self.font())

        return table_widget

    def show_context_menu(self, position):
        """Show context menu on right-click in the table."""

        # Get the item at the clicked position
        index = self.tab1_widget.indexAt(position)
        if not index.isValid():
            return

        row = index.row()
        button = self.tab1_widget.cellWidget(row, 4)

        if button is None:
            return

        # Check if device is activated
        is_activated = button.property("activated")
        if not is_activated:
            # If not activated, do nothing
            return


        if index.isValid():
            # Get the serial number from the clicked row (column 2)
            serial = self.tab1_widget.item(row, 2).text()

            # Create the context menu
            menu = QMenu(self)

            # Add actions to the menu
            load_conf_action = QAction("Load Configuration", self)
            save_conf_action = QAction("Save Configuration", self)
            settings_action = QAction("Settings", self)

            # Emit signal when the settings action is triggered
            settings_action.triggered.connect(partial(self.emit_settings_signal, serial))

            # Add actions to the menu
            menu.addAction(load_conf_action)
            menu.addAction(save_conf_action)
            menu.addAction(settings_action)

            # Show the menu at the position of the right-click
            menu.exec_(self.tab1_widget.viewport().mapToGlobal(position))

    def emit_settings_signal(self, serial):
        """Emit the on_settings_clicked signal with the serial number."""
        self.on_settings_clicked.emit(serial)

    def fill_tab_Active_Projects(self, tab_widget):
        """Fill the content of Tab 2 (Active Projects)."""
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel("Active Projects Overview"))
        # Add more content related to Active Projects here.
        tab_widget.setLayout(tab_layout)

    def fill_tab_Active_Threads(self, tab_widget):
        """Fill the content of Tab 3 (Active Threads)."""
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel("Currently Active Threads"))
        # Add more content related to Active Threads here.
        tab_widget.setLayout(tab_layout)

    def toggle_activation(self, table_widget, row: int):
        """
        Handle activation/deactivation button click.
        This will change the background color of the row based on activation.
        """
        # Check the current state of the button (Activate or Deactivate)
        button = table_widget.cellWidget(row, 4)

        # Emit the signal with the serial number of the device
        serial = table_widget.item(row, 2).text()  # Assuming serial is in the third column
        self.device_activate_click.emit(serial, button.property("activated"))  # Emit the signal

    def activation_response(self, serial: str, state: int):
        """
        Handle activation/deactivation response.
        This will find the row with the given serial and change the background color
        based on the activation state (green for success, red for failure).

        Args:
            table_widget (QTableWidget): The table widget containing the devices.
            serial (str): The serial number of the device.
            state (int): The activation state (1 for success, 0 for failure).
        """
        # Find the row with the given serial number
        row = -1
        for r in range(self.tab1_widget.rowCount()):
            if self.tab1_widget.item(r, 2).text() == serial:  # Serial is assumed to be in the 3rd column (index 2)
                row = r
                break

        # If the row with the given serial was found
        if row != -1:
            # Find the button in the last column (column index 4)
            button = self.tab1_widget.cellWidget(row, 4)
            is_active = button.property("activated")

            # Check the state and update the row accordingly
            if state == 1:
                if not is_active:
                    # Activate (success): Change the background color to light green
                    self.setRowBackgroundColor(self.tab1_widget, row, QColor(144, 238, 144))  # Light Green
                    button.setText("Deactivate")  # Change the text to Deactivate
                    #button.setEnabled(False)  # Disable the button (optional)
                    button.setProperty("activated", True)  # <-- Store activation state
                if is_active:
                    # Deactive (success): Change the background color to white
                    self.setRowBackgroundColor(self.tab1_widget, row, QColor(255, 255, 255))  # White
                    button.setText("Activate")  # Change the text to Deactivate
                    #button.setEnabled(False)  # Disable the button (optional)
                    button.setProperty("activated", False)  # <-- Store activation state
            else:
                # Deactivate (failure): Change the background color to light grey
                self.setRowBackgroundColor(self.tab1_widget, row, QColor(255, 182, 193))  # Light Red
                button.setText("Activate")  # Change the text to Activate
                button.setEnabled(True)  # Re-enable the button (optional)
                button.setProperty("activated", False)  # <-- Not activated

        else:
            print(f"Device with serial {serial} not found in the table.")

    def setRowBackgroundColor(self, table_widget, row, color):
        """
        Utility method to set the background color of a table row.
        """
        for column in range(table_widget.columnCount()):
            item = table_widget.item(row, column)
            if item is not None:
                item.setBackground(color)

    def reload_tab_Available_Devices(self, devices_dict: Dict[str, Dict[str, Any]]):
        """Reload the table with new data from the provided dictionary."""

        self.connected_devices = devices_dict

        # Clear the existing rows in the table
        self.tab1_widget.setRowCount(0)

        # Loop through the dictionary and add rows to the table
        for device_id, device_data in devices_dict.items():
            # Add a new row for each device
            row_position = self.tab1_widget.rowCount()
            self.tab1_widget.insertRow(row_position)

            # Add data to the columns (name -> model, type -> vendor, id -> serial)
            self.tab1_widget.setItem(row_position, 0, QTableWidgetItem("Not yet implemented"))  # Model
            self.tab1_widget.setItem(row_position, 1, QTableWidgetItem(device_data['name']))  # Vendor
            self.tab1_widget.setItem(row_position, 2, QTableWidgetItem(device_id))  # Serial
            self.tab1_widget.setItem(row_position, 3, QTableWidgetItem(device_data.get('project', '')))  # Project (if any)

            # Create an activation button for the last column
            activate_button = QPushButton("Activate")
            # Connect the activation button to a handler function
            activate_button.clicked.connect(partial(self.toggle_activation, self.tab1_widget, row_position))
            self.tab1_widget.setCellWidget(row_position, 4, activate_button)

        # Optional: Resize columns to fit content
        #self.tab1_widget.resizeColumnsToContents()