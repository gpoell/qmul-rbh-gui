from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.collect_data = QPushButton("Collect")
        self.collect_data.setObjectName("collect")
        self.connect = QPushButton("Connect Sensor")
        self.connect.setObjectName("connect")
        
        mainbox = QVBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainbox.addWidget(self.collect_data)
        mainbox.addWidget(self.connect)