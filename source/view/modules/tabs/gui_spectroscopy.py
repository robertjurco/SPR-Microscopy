from PySide6.QtWidgets import QLabel

from source.view.modules.gui_tab import TabGUI


class SpectroscopyGUI(TabGUI):
    def __init__(self, index):
        super().__init__(index)
        self.setup_content()

    def setup_content(self):
        # Example: Adding a label and any other widgets to the custom tab content layout
        custom_label = QLabel('Custom Content')
        self.content_layout.addWidget(custom_label)
        # You can add more widgets as needed