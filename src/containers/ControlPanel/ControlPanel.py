from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.collect_btn = QPushButton("Collect")
        self.collect_btn.setObjectName("collect_btn")
        self.collect_btn.clicked.connect(self.send_data)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setObjectName("connect_btn")
        self.connect_btn.clicked.connect(self.send_data)

        self.display_btn = QPushButton("Display")
        self.display_btn.setObjectName("display_btn")
        
        mainbox = QVBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainbox.addWidget(self.connect_btn)
        mainbox.addWidget(self.collect_btn)
        mainbox.addWidget(self.display_btn)

    def send_data(self):
        print(self.sender().text())