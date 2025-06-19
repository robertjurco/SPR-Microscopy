from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSpinBox, QSpacerItem, \
    QSizePolicy, QDoubleSpinBox

from source.view.widgets.ROI_widget import ROIWidget
from source.view.widgets.image_display import ImageDisplay
from source.view.widgets.plotting_widgets import PlotWidget, HistogramPlotWidget


class CameraNoiseView(QWidget):
    set_exposure = Signal(float)
    max_frames_changed = Signal(int)

    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height

        self.spinbox_max_frames = None
        self.spinbox_exposure = None

        self.setup_content()

        self.setWindowTitle("Camera Schott Noise Measurement")

    def setup_content(self):
        # Main horizontal layout (to arrange PlotWidget on left and settings on the right)
        main_layout = QHBoxLayout()

        # Spinbox with minimum value and maximum values given by camera exposure time
        self.spinbox_exposure = QDoubleSpinBox()
        self.spinbox_exposure.setDecimals(2)  # Set to 2 decimal places
        # Label
        label_exposure = QLabel("Exposure time [ms]")
        # Button
        self.button_exposure = QPushButton("Set exposure")
        self.button_exposure.clicked.connect(self.handle_set_exposure)
        # Horizontal layout for spinbox + label
        hlayout_1 = QHBoxLayout()
        hlayout_1.addWidget(label_exposure)
        hlayout_1.addWidget(self.spinbox_exposure)
        hlayout_1.addWidget(self.button_exposure)
        # Spinbox with minimum value of 100
        self.spinbox_max_frames = QSpinBox()
        self.spinbox_max_frames.setMinimum(100)
        self.spinbox_max_frames.setMaximum(10000)
        # Connect valueChanged signal to emit your custom signal
        self.spinbox_max_frames.valueChanged.connect(self.max_frames_changed.emit)
        # Label
        label_max_frames = QLabel("Number of frames to average")
        # Horizontal layout for spinbox + label
        hlayout_2 = QHBoxLayout()
        hlayout_2.addWidget(label_max_frames)
        hlayout_2.addWidget(self.spinbox_max_frames)
        # Button
        self.button_start = QPushButton("Start noise measurement")

        # Camera image
        self.image_display = ImageDisplay(self.width, self.height)
        #self.image_display.set_image_from_file('C:/Users/jurco/Desktop/images.png')

        self.roi_widget = ROIWidget(self.width, self.height)

        # Plot
        self.plot_widget = PlotWidget(x_label="Intensity", y_label="Variance", log_scale=False, scatter_plot=True)
        self.histogram_widget = HistogramPlotWidget(x_label="Intensity", y_label="Occurence", bins=50)

        # Vertical layout
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.roi_widget)
        # Add spacer to push button to bottom
        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        vlayout.addLayout(hlayout_1)
        vlayout.addLayout(hlayout_2)
        vlayout.addWidget(self.button_start)


        # Add widgets to the main layout
        main_layout.addLayout(vlayout)
        main_layout.addWidget(self.image_display)
        main_layout.addWidget(self.plot_widget)
        main_layout.addWidget(self.histogram_widget)
        self.setLayout(main_layout)

    def handle_set_exposure(self):
        exposure_value = self.spinbox_exposure.value()
        self.set_exposure.emit(exposure_value)

    def update_frame(self, image):
        self.image_display.set_image(image, show_max_intensity=True, show_min_intensity=True)