from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal as Signal

class SensorControls(QWidget):

    sig_state_command = Signal(str, name="stateCommand")

    def __init__(self):
        super().__init__()

        self.collect_btn = QPushButton("Collect")
        self.collect_btn.clicked.connect(lambda: self.emit_signal("collect"))

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(lambda: self.emit_signal("connect"))

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(lambda: self.emit_signal("disconnect"))

        self.calibrate_btn = QPushButton("Calibrate")
        self.calibrate_btn.clicked.connect(lambda: self.emit_signal("calibrate"))
        
        leftBtnLayout = QVBoxLayout()
        leftBtnLayout.addWidget(self.connect_btn)
        leftBtnLayout.addWidget(self.disconnect_btn)

        rightBtnLayout = QVBoxLayout()
        rightBtnLayout.addWidget(self.collect_btn)
        rightBtnLayout.addWidget(self.calibrate_btn)

        mainLayout = QHBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addLayout(leftBtnLayout)
        mainLayout.addLayout(rightBtnLayout)

    def emit_signal(self, command):
        self.sig_state_command.emit(command)