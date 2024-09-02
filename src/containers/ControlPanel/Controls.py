from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from containers.ControlPanel.MotorControls import MotorControls
from containers.ControlPanel.SensorControls import SensorControls
from containers.ControlPanel.ConfigOptions import ConfigOptions

class Controls(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Gripper Controls")
        self.label.setObjectName("container-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configOptions = ConfigOptions()
        self.motor_ctrls = MotorControls()
        self.sensor_ctrls = SensorControls()

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.configOptions)
        mainLayout.addWidget(self.sensor_ctrls)
        mainLayout.addWidget(self.motor_ctrls)