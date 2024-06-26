"""
Creates a Line Graph Widget for displaying tactile data.

This component displays three lines representing incoming tactile data received by the ESP32 server.

Attributes:

    graph <PlotWidget>:             the main graph for plotting
    time <int>:                     timestamp recording for tactile data
    tactile_data <float>:           dictionary containing arrays of 3 dimensional tactile data  
    line_x <graph>:                 line mapped to X tactile data values
    line_y <graph>:                 line mapped to Y tactile data values
    line_z <graph>:                 line mapped to Z tactile data values

Methods:

    update_plot:                    updates the line values on the graph when new tactile data is received
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

class LineGraph(QWidget):
    def __init__(self):
        super().__init__()

        mainbox = QVBoxLayout(self)

        self.graph = pg.PlotWidget()
        self.graph.setBackground("w")
        self.graph.showGrid(x=False,y=False)

        self.time = list(range(10))

        self.tactile_data = {
            "x": [0 for _ in range(10)],
            "y": [0 for _ in range(10)],
            "z": [0 for _ in range(10)]
        }

        self.line_x = self.graph.plot(
            self.time,
            self.tactile_data['x'],
            name="Tactile Sensor",
            pen=pg.mkPen(color="#061E45"),
            symbol="o",
            symbolSize=7,
            symbolBrush=0.9,
        )

        self.line_y = self.graph.plot(
            self.time,
            self.tactile_data['y'],
            name="Tactile Sensor",
            pen=pg.mkPen(color="#B87333"),
            symbol="o",
            symbolSize=7,
            symbolBrush=0.2,
        )

        self.line_z = self.graph.plot(
            self.time,
            self.tactile_data['y'],
            name="Tactile Sensor",
            pen=pg.mkPen(color="#36454F"),
            symbol="o",
            symbolSize=7,
            symbolBrush=0.2,
        )

        mainbox.addWidget(self.graph)

    def plot(self, data):
        """
        Updates the graph with new lines representing the 3 dimensional tactile data.
        The time and data values maintain their original length by removing the first
        element and appending the new data to the end.
        """
        self.time = self.time[1:]
        self.time.append(self.time[-1] + 1)
            
        self.tactile_data['x'] = self.tactile_data['x'][1:]
        self.tactile_data['y'] = self.tactile_data['y'][1:]
        self.tactile_data['z'] = self.tactile_data['z'][1:]

        self.tactile_data['x'].append(float(data[0]))
        self.tactile_data['y'].append(float(data[1]))
        self.tactile_data['z'].append(float(data[2]))

        self.line_x.setData(self.time, self.tactile_data['x'])
        self.line_y.setData(self.time, self.tactile_data['y'])
        self.line_z.setData(self.time, self.tactile_data['z'])