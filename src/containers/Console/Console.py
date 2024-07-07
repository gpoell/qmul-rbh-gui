"""
The Console displays event messages.

Components within the application can emit signals with messages containing a header and body to associate
the type of message with its contents.The Console reports messages of the following types, info, warning, error, and fatal,
and all messages are typed check and validated for appropriate message contents. 

Classes:

    Console

Attributes:

    textEdit <QTextEdit>:       the QTextEdit widget to display messages
    messages <dict>:            prefixed message values based on type
    messageTypes <list>:        list of message types

Methods:

    exec(<str> command)
    disconnect
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtCore import pyqtSlot as Slot

class Console(QWidget):
    def __init__(self):
        super().__init__()

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("console")
        self.__border = "-"*75
        self.__consoleHeader = "APPLICATION CONSOLE"
        self.insert_text(self.__border)
        self.insert_text(self.__consoleHeader)
        self.insert_text(self.__border)

        self.messages = {
            "info": "[INFO]: ",
            "warning": "[WARNING]: ",
            "error": "[ERROR]: ",
            "fatal": "[FATAL]: "
        }
        self.messageTypes = list(self.messages.keys())
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.textEdit)

    @Slot(dict, name="consoleMessage")
    def update_console(self, consoleMessage):
        """
        Updates the console with incoming messages from other components.
        Validates that the message contents are of the correct type and value
        and constructs a new message to display on the Console.
        """

        assert_check(consoleMessage)
        
        message = ""
        
        if consoleMessage["header"] not in self.messageTypes:
            message = self.messages["error"] + "unsupported or missing header from message."
            return
        
        message = self.messages[consoleMessage["header"]] + consoleMessage["body"]
        self.insert_text(message)
        
    def insert_text(self, msg):
        """
        Updates the QTextEdit component with the new messages.
        """
        self.textEdit.insertPlainText(msg)
        self.textEdit.insertPlainText("\n")
        self.textEdit.verticalScrollBar().setSliderPosition(self.textEdit.verticalScrollBar().maximum())

def assert_check(msg):
        """
        Validates the message contains the appropriate header and body structure and the values are strings.
        """
        msg_properties = list(msg.keys())
        assert "header" in msg_properties and "body" in msg_properties, "[ASSERTION ERROR]: message does not contain correct properties."
        assert type(msg["header"]) == str, "[ASSERTION ERROR]: message header is not a string."
        assert type(msg["body"]) == str, "[ASSERTION ERROR]: message body is not a string."