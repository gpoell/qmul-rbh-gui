from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtCore import pyqtSlot as Slot

class Console(QWidget):
    """
    Components within the application can emit signals with messages to the Console which
    will display them on the GUI. The Console can accept messages in any format, however,
    the ConsoleLogger component provides methods for formatting the messages to display.
    """
    def __init__(self):
        super().__init__()

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("console")
        self.__border = "-"*75
        self.__consoleHeader = "APPLICATION CONSOLE"
        self.update_console(self.__border)
        self.update_console(self.__consoleHeader)
        self.update_console(self.__border)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.textEdit)

    @Slot(str, name="consoleMessage")
    def update_console(self, msg):
        """Updates the QTextEdit component with the new messages."""
        self.textEdit.insertPlainText(msg)
        self.textEdit.insertPlainText("\n")
        self.textEdit.verticalScrollBar().setSliderPosition(self.textEdit.verticalScrollBar().maximum())