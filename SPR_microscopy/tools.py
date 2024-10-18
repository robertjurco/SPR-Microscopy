import random


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