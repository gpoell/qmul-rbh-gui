from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal as Signal

class SensorControls(QWidget):

    sig_state_command = Signal(str, name="stateCommand")

    def __init__(self):
        super().__init__()

        self.label = QLabel("Sensor Controls")
        self.label.setObjectName("container-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.collect_btn = QPushButton("Collect")
        self.collect_btn.clicked.connect(lambda: self.emit_signal("collect"))

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(lambda: self.emit_signal("connect"))

        # Temporary Disconnect
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(lambda: self.emit_signal("disconnect"))

        mainbox = QVBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainbox.addWidget(self.label)
        mainbox.addWidget(self.connect_btn)
        mainbox.addWidget(self.collect_btn)
        mainbox.addWidget(self.disconnect_btn)

    def emit_signal(self, command):
        self.sig_state_command.emit(command)