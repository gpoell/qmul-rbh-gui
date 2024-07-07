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

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from containers.Dashboard.DataLabel import DataLabel

class DataLabels(QWidget):
    def __init__(self):
        super().__init__()

        self.header = QLabel("Magnetic Flux Density")
        self.header.setObjectName("dataLabelsHeader")
        self.x = DataLabel("X", "#0C746A")
        self.y = DataLabel("Y", "#AFBBAF")
        self.z = DataLabel("Z", "#6F8695")

        mainbox = QGridLayout(self)
        mainbox.setVerticalSpacing(10)
        
        mainbox.addWidget(self.header, 0, 0)
        mainbox.addWidget(self.x, 1, 0)
        mainbox.addWidget(self.y, 2, 0)
        mainbox.addWidget(self.z, 3, 0)

    def updateLabels(self, data):
        self.x.value.setText(str(float(data[0])))
        self.y.value.setText(str(float(data[1])))
        self.z.value.setText(str(float(data[2])))