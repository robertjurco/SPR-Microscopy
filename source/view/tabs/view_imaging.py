from PySide6.QtCore import Qt
from source.view.settings.view_settings_camera import ImageDisplay
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QPushButton, QHBoxLayout, QSplitter, QSpinBox
from source.view.tabs.misc import PlotWidget  # Assuming this is a custom widget for plotting

class ImagingView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_content()
        self.showMaximized()  # Show the window in fullscreen

    def setup_content(self):
        # Main vertical layout
        main_layout = QVBoxLayout()

        # Create the main splitter for the top part (plot) and bottom part (image and buttons)
        main_splitter = QSplitter(Qt.Orientation.Vertical)

        # Top part - PlotWidget (this will be the top part of the splitter)
        plot_widget = PlotWidget()  # Assuming you have a PlotWidget defined elsewhere
        main_splitter.addWidget(plot_widget)

        # Bottom part - Horizontal layout containing ImageDisplay and Buttons
        bottom_layout = QHBoxLayout()  # Horizontal layout for the bottom part

        # Image Display (left part of the bottom layout)
        self.image_display = ImageDisplay(preferred_height=self.calculate_image_height())
        self.image_display.set_image_from_file('C:/Users/jurco/Desktop/images.png')  # Set image from file
        bottom_layout.addWidget(self.image_display)

        # Right part - Buttons and Labels
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)

        # Camera selection
        self.camera_select = QComboBox()
        self.camera_select.addItem("Select Camera")
        # Populate with cameras from other parts of the code (example method call)
        self.populate_camera_list()
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
        self.average_noise_label = QLabel("Noise Averaging interval♣:")
        settings_layout.addWidget(self.average_noise_label)

        # Create spinbox for positive numbers with a step size of 10
        self.noise_duration_spinbox = QSpinBox()
        self.noise_duration_spinbox.setRange(10, 3600)  # set seconds 1, max 1000 (you can adjust as needed)
        self.noise_duration_spinbox.setSingleStep(10)  # set step size to 10
        self.noise_duration_spinbox.setPrefix("Seconds: ")

        settings_layout.addWidget(self.noise_duration_spinbox)

        bottom_layout.addWidget(settings_widget)  # Add the settings widget with camera selection, buttons, and label

        # Add the main splitter and bottom layout to the main layout
        main_layout.addWidget(main_splitter)
        main_layout.addLayout(bottom_layout)

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
