from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


def slm_gui():
    """
    Returns the Tab for Settings menu

    Returns
    -------
    QWidget
    """

    tab = QWidget()

    layout = QVBoxLayout()

    label = QLabel('-- Channels to be shown --')
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label)

    layout.addStretch(1)
    tab.setLayout(layout)
    return tab