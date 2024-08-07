"""
Dashboard component for visualizing tactile sensor data.

Components:

    Data Labels:    tactile sensor data values for x, y, z axes
    Data Graph:     line graph visualization for tactile data

Methods:

    updateDashboard: updates the graph and labels with new tactile data
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSlot as Slot
from containers.Dashboard.DataLabels import DataLabels
from components.LineGraph import LineGraph

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.data_labels = DataLabels()
        self.data_graph = LineGraph()

        mainbox = QHBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        mainbox.addWidget(self.data_graph)
        mainbox.addWidget(self.data_labels)

    @Slot(tuple, name="tactileData")
    def updateDashboard(self, data):
        self.data_graph.plot(data)
        self.data_labels.updateLabels(data)