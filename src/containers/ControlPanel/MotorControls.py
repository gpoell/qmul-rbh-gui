from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class MotorControls(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Motor Controls")
        self.label.setObjectName("container-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.open_btn = QPushButton("Open")
        self.open_btn.clicked.connect(self.send_data)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.send_data)

        mainbox = QVBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainbox.addWidget(self.label)
        mainbox.addWidget(self.open_btn)
        mainbox.addWidget(self.close_btn)

    def send_data(self):
        print(self.sender().text())