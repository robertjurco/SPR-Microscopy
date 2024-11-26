import random

from PySide6.QtGui import QIcon, QColor, QPainter, QPixmap, Qt
from PySide6.QtSvg import QSvgRenderer


def random_color():
    """
    Generates random color in rgb format, each channel has a value in the interval (0, 1)

    Returns
    -------
    tuple
        color in rgb format
    """
    return (
        random.random(),
        random.random(),
        random.random()
    )


def random_color_int():
    """
    Generates random color in rgb format, each channel has a value in the interval (0, 255)

    Returns
    -------
    tuple
        color in rgb format
    """
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def generate_random_color():
    """
    Generates random color in rgb hexadecimal format

    Returns
    -------
    str
        color in rgb format
    """
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def generate_random_color_light():
    """
    Generates light random color in rgb format, each channel has a value in the interval (0, 255)

    Returns
    -------
    str
        color in rgb format
    """
    r, g, b = 0, 0, 0
    while (r + g + b) > 2.8 * 255 or (r + g + b) < 2.5 * 255:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def QIcon_modify_color(svg_path, color):
    """
    Change the color of an SVG QIcon.

    :param svg_path: Path to the SVG file.
    :param color: The desired color as a QColor, hex string, or tuple (R, G, B).
    :return: QIcon with the specified color.
    """
    # Create a QSvgRenderer to load the SVG file
    svg_renderer = QSvgRenderer(svg_path)

    # Create a QPixmap to render the SVG onto
    pixmap = QPixmap(svg_renderer.defaultSize())

    # Start painting onto the QPixmap
    pixmap.fill(Qt.transparent)  # Fill with transparent background
    painter = QPainter(pixmap)
    svg_renderer.render(painter)

    # Change the color
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    if isinstance(color, str):
        painter.fillRect(pixmap.rect(), QColor(color))
    elif isinstance(color, tuple):
        painter.fillRect(pixmap.rect(), QColor(*color))
    else:
        painter.fillRect(pixmap.rect(), color)
    painter.end()

    # Convert the QPixmap to a QIcon
    icon = QIcon(pixmap)
    return icon