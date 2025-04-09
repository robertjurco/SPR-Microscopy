from PySide6.QtCore import Qt
from source.view.settings.view_settings_camera import ImageDisplay
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QPushButton, QHBoxLayout, QSplitter, QSpinBox
from source.view.tabs.misc import PlotWidget  # Assuming this is a custom widget for plotting

class CameraFPSView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_content()

        self.setWindowTitle("Camera FPS meter")
        #self.showMaximized()  # Show the window in fullscreen

    def setup_content(self):
        # Main horizontal layout (to arrange PlotWidget on left and settings on the right)
        main_layout = QHBoxLayout()

        # Top part - PlotWidget (on the left side)
        self.plot_widget = PlotWidget(x_label="Exposure [ms]", y_label="FPS", log_scale=True, scatter_plot=True)  # Assuming you have a PlotWidget defined elsewhere
        main_layout.addWidget(self.plot_widget)  # Give it more space with a stretch factor

        # Right part - Settings section
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)

        # Camera selection
        self.camera_select = QComboBox()
        self.camera_select.addItem("Select Camera")  # Default item
        # Populate with cameras from other parts of the code (example method call)
        self.populate_camera_list()  # Add your method to populate cameras
        settings_layout.addWidget(QLabel("Camera Selection"))
        settings_layout.addWidget(self.camera_select)

        # Add action buttons for saving the project and noise analysis
        self.save_project_button = QPushButton("Save Project")
        self.noise_analysis_button = QPushButton("Noise Analysis")
        settings_layout.addWidget(self.save_project_button)
        settings_layout.addWidget(self.noise_analysis_button)

        # Add label to display noise value (will update later based on calculations)
        self.noise_label = QLabel("Noise: Not calculated yet")
        settings_layout.addWidget(self.noise_label)

        # Create label for "Average Noise over"
        self.average_noise_label = QLabel("Noise Averaging Interval (Seconds):")
        settings_layout.addWidget(self.average_noise_label)

        # Create spinbox for positive numbers with a step size of 10
        self.noise_duration_spinbox = QSpinBox()
        self.noise_duration_spinbox.setRange(10, 3600)  # Set range from 10 seconds to 3600 seconds (1 hour)
        self.noise_duration_spinbox.setSingleStep(10)  # Set step size to 10 seconds
        self.noise_duration_spinbox.setPrefix("Seconds: ")
        settings_layout.addWidget(self.noise_duration_spinbox)

        # Add the settings widget layout to the main layout
        main_layout.addWidget(settings_widget)  # Settings take up the remaining space

        # Set the layout for this window
        self.setLayout(main_layout)

    def calculate_image_height(self):
        """Calculate height for the image display, using a fixed height as a ratio of the screen's height."""
        screen_height = self.screen().availableGeometry().height()

        # Set a fixed height ratio for the image display (this will be the height of the ImageDisplay)
        bottom_height_ratio = 1 / 3  # Set this ratio to adjust image height

        bottom_height = screen_height * bottom_height_ratio
        return int(bottom_height)

    def populate_camera_list(self):
        """Populate the camera selection list."""
        cameras = ["Camera 1", "Camera 2", "Camera 3"]
        self.camera_select.addItems(cameras)
