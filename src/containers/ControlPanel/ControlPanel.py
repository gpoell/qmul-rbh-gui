from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from containers.ControlPanel.MotorControls import MotorControls
from containers.ControlPanel.SensorControls import SensorControls

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.motor_ctrls = MotorControls()
        self.sensor_ctrls = SensorControls()

        mainbox = QHBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainbox.addWidget(self.sensor_ctrls)
        mainbox.addWidget(self.motor_ctrls)