"""
Wrapper for data labels section.

Components:

    header:    label for header
    x:         label for x axes value
    y:         label for y axes value
    z:         label for z axes value 

Methods:

    updateLabels: updates the data label text with tactile data
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,  QLabel
from PyQt6.QtCore import Qt
from containers.Dashboard.DataLabel import DataLabel
import decimal

class DataLabels(QWidget):
    def __init__(self):
        super().__init__()

        self.header = QLabel("Magnetic Flux Density")
        self.header.setObjectName("dataLabelsHeader")
        self.x = DataLabel("X", "#061E45")
        self.y = DataLabel("Y", "#B87333")
        self.z = DataLabel("Z", "#36454F")

        mainbox = QVBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        mainbox.addWidget(self.header)
        mainbox.addWidget(self.x)
        mainbox.addWidget(self.y)
        mainbox.addWidget(self.z)

    def updateLabels(self, data):
        self.x.value.setText(str(float(data[0])))
        self.y.value.setText(str(float(data[1])))
        self.z.value.setText(str(float(data[2])))