from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal as Signal

class MotorControls(QWidget):

    sig_state_command = Signal(str, name="stateCommand")

    def __init__(self):
        super().__init__()

        self.open_btn = QPushButton("Open")
        self.open_btn.clicked.connect(lambda: self.emit_signal("open"))

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(lambda: self.emit_signal("close"))

        mainbox = QVBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainbox.addWidget(self.open_btn)
        mainbox.addWidget(self.close_btn)

    def emit_signal(self, command):
        self.sig_state_command.emit(command)