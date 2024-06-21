from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class SensorControls(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Sensor Controls")
        self.label.setObjectName("container-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.collect_btn = QPushButton("Collect")
        self.connect_btn = QPushButton("Connect")

        mainbox = QVBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainbox.addWidget(self.label)
        mainbox.addWidget(self.connect_btn)
        mainbox.addWidget(self.collect_btn)