"""
Custom data label component for visualizing tactile data values.

Components:

    frame:      custom frame wrapping labels.
    label:      text label for axes
    value:      text label for axes value
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

class DataLabel(QWidget):
    def __init__(self, label, color="white"):
        super().__init__()

        self.frame = QFrame(self)
        self.frame.setStyleSheet(
            f"background-color: {color};"
        )
        self.frame.resize(1000,1000)
        
        self.label = QLabel(label)
        self.label.setObjectName("dataLabelLabel")
        self.label.setParent(self.frame)
        
        self.value = QLabel("0")
        self.value.setObjectName("dataLabelValue")
        self.value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setParent(self.frame)

        mainbox = QHBoxLayout(self)
        mainbox.addWidget(self.label)
        mainbox.addWidget(self.value)