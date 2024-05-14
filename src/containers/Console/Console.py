from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PyQt6.QtCore import Qt

class Console(QWidget):
    def __init__(self):
        super().__init__()

        # Display Area
        self.terminal = QLabel(self)
        self.terminal.setObjectName("display-box")
        self.terminal.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        # Make Terminal Scrollable
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.terminal)
        
        mainbox = QVBoxLayout(self)
        mainbox.addWidget(self.terminal)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)