from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from containers.ControlPanel.Controls import Controls
from containers.ControlPanel.Console import Console

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.controls = Controls()
        self.console = Console()

        mainLayout = QHBoxLayout(self)
        mainLayout.addWidget(self.controls)
        mainLayout.addWidget(self.console)