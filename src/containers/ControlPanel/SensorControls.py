from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class SensorControls(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Sensor Controls")
        self.label.setObjectName("container-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.collect_btn = QPushButton("Collect")
        self.collect_btn.clicked.connect(self.send_data)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.send_data)

        self.display_btn = QPushButton("Display")
        self.display_btn.clicked.connect(self.send_data)
        
        mainbox = QVBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainbox.addWidget(self.label)
        mainbox.addWidget(self.connect_btn)
        mainbox.addWidget(self.collect_btn)
        mainbox.addWidget(self.display_btn)

    def send_data(self):
        print(self.sender().text())