from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QApplication, QScrollArea
from PyQt6.QtCore import Qt, QSize
from time import sleep
from threading import Lock

from PyQt6.QtCore import pyqtSlot as Slot

class Console(QWidget):
    def __init__(self):
        super().__init__()

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("display-box")

        layout = QVBoxLayout(self)
        layout.addWidget(self.textEdit)

    @Slot(tuple, name="tactileData")
    def tactile_data_format(self, data):
        msg = f"X: {data[0]} \t\t Y: {data[1]} \t\t Z: {data[2]}"
        self.update(msg)

    @Slot(str, name="consoleMessage")
    def update(self, msg):
        self.textEdit.insertPlainText(msg)
        self.textEdit.insertPlainText("\n")
        self.textEdit.verticalScrollBar().setSliderPosition(self.textEdit.verticalScrollBar().maximum())