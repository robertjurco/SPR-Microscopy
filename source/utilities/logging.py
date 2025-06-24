from PySide6.QtCore import QObject, Signal
import datetime

class Logging(QObject):
    update = Signal(str, str)  # (message: str, color: str)

    def __init__(self, enable_print=True):
        super().__init__()
        self.enable_print = enable_print

    def _get_timestamp(self):
        return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    def _log(self, message, level, color_code=None, color_name=None):
        timestamp = self._get_timestamp()
        formatted = f"{timestamp} [{level.upper()}] {message}"

        if self.enable_print:
            if color_code:
                print(f"\033[{color_code}m{formatted}\033[0m")
            else:
                print(formatted)

        # Emit Qt signal with message and color
        self.update.emit(formatted, color_name or "")

    def info(self, message):
        self._log(message, "info")

    def error(self, message):
        self._log(message, "error", color_code="31", color_name="red")

# Create a globally shared logger instance
logger = Logging()