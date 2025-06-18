from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSpinBox, QSpacerItem, \
    QSizePolicy

from source.view.widgets.ROI_widget import ROIWidget
from source.view.widgets.image_display import ImageDisplay
from source.view.tabs.misc import PlotWidget


class CameraNoiseView(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.setup_content()

        self.setWindowTitle("Camera Schott Noise Measurement")

    def setup_content(self):
        # Main horizontal layout (to arrange PlotWidget on left and settings on the right)
        main_layout = QHBoxLayout()

        # Spinbox with minimum value of 100
        self.spinbox_max_frames = QSpinBox()
        self.spinbox_max_frames.setMinimum(100)
        # Label
        self.label = QLabel("Number of frames to average")
        # Horizontal layout for spinbox + label
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.label)
        hlayout.addWidget(self.spinbox_max_frames)
        # Button
        self.button_start = QPushButton("Start noise measurement")

        # Camera image
        self.image_display = ImageDisplay(self.width, self.height)
        #self.image_display.set_image_from_file('C:/Users/jurco/Desktop/images.png')

        self.roi_widget = ROIWidget(self.width, self.height)

        # Plot
        self.plot_widget = PlotWidget(x_label="Intensity", y_label="STD", log_scale=False, scatter_plot=True)  # Assuming you have a PlotWidget defined elsewhere

        # Vertical layout
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.roi_widget)
        # Add spacer to push button to bottom
        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.button_start)


        # Add widgets to the main layout
        main_layout.addLayout(vlayout)
        main_layout.addWidget(self.image_display)
        main_layout.addWidget(self.plot_widget)
        self.setLayout(main_layout)

    def update_frame(self, image):
        self.image_display.set_image(image, show_max_intensity=True, show_min_intensity=True)