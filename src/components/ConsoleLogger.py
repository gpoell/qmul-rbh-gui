from PyQt6.QtCore import QObject, pyqtSignal

class ConsoleLogger(QObject):
    """A very simple class for emitting messages to display on the GUI Console"""

    signal_console = pyqtSignal(str, name="consoleMessage")

    def __init__(self):
        super().__init__()

    def info(self, msg):
        console_msg = "[INFO]: " + msg
        self.signal_console.emit(console_msg)

    def warn(self, msg):
        console_msg = "[WARNING]: " + msg
        self.signal_console.emit(console_msg)

    def error(self, msg):
        console_msg = "[ERROR]: " + msg
        self.signal_console.emit(console_msg)

    def fatal(self, msg):
        console_msg = "[FATAL]: " + msg
        self.signal_console.emit(console_msg)