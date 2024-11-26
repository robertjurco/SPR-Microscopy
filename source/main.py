import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from hardware.model_init import Model
from presenter.presenter_init import Presenter
from view.view_init import View


def __excepthook(exc_type, exc_value, exc_tb):
    """
    Catches exceptions and errors and displays them in the OKDialog
    """
    pass


if __name__ == '__main__':
    """
    Runs the application
    """

    # If an unhandled exception occurs, the excepthook function will be called instead of the default handler.
    sys.excepthook = __excepthook

    # Creates an instance of the QApplication class.
    # This is necessary for any PyQt5 application as it manages application-wide resources and settings.
    # sys.argv is passed to allow command-line arguments to be used.
    app = QApplication(sys.argv)
    app.setFont(QFont('Courier', 8))

    # Set style sheet for application
    # Load the QSS file
    with open('styles.qss', 'r') as file:
        style_sheet = file.read()
    app.setStyleSheet(style_sheet)


    # The Model-View-Presenter (MVP) architecture separates an application into three components:
    # the Model, which handles data and business logic; the View, which manages the user interface and displays data;
    # and the Presenter, which acts as an intermediary, processing user input, updating the Model, and refreshing the View.
    # This separation of concerns makes the codebase easier to manage, test, and maintain,
    # as each component can be developed independently. The Presenter ensures that the View remains passive and
    # focused on UI tasks, while the Model remains unaware of the UI, leading to a more modular and maintainable
    # application structure.

    # Model: Contains the data and the long-running task.
    model = Model()
    print("Model initialized")

    # View: Manages the GUI components.
    # .show() is a property of QWidget: View extends QMainWindow, QMainWindow extends QWidget.
    view = View()
    view.show()
    print("View initialized")

    # Presenter: Handles the interaction between the Model and the View,
    # including starting the background task and updating the view when the task is complete.
    presenter = Presenter(model, view)

    # Starts the application’s event loop, which waits for user interactions and updates the GUI accordingly.
    # The application will keep running until app.quit() is called or the main window is closed.
    sys.exit(app.exec())