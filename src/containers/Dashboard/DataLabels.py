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
        self.xLabel = DataLabel(label="X", color="#0C746A")
        self.yLabel = DataLabel(label="Y", color="#AFBBAF")
        self.zLabel = DataLabel(label="Z", color="#6F8695")

        mainLayout = QGridLayout(self)
        mainLayout.setVerticalSpacing(10)
        mainLayout.addWidget(self.header, 0, 0)
        mainLayout.addWidget(self.xLabel, 1, 0)
        mainLayout.addWidget(self.yLabel, 2, 0)
        mainLayout.addWidget(self.zLabel, 3, 0)

    def updateLabels(self, data):
        self.xLabel.value.setText(data[0])
        self.yLabel.value.setText(data[1])
        self.zLabel.value.setText(data[2])