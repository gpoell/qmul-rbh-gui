from PyQt6.QtWidgets import QWidget, QVBoxLayout
from containers.ControlPanel.ControlPanel import ControlPanel
from containers.Console.Console import Console
from components.RbhSocket import RbhSocket

class Desktop(QWidget):
    def __init__(self):
        super().__init__()

        # Create Desktop Layouts
        main = QVBoxLayout(self)
        main.setObjectName("desktop")
        top = QVBoxLayout()
        bottom = QVBoxLayout()

        # Create Components
        control_panel = ControlPanel()
        self.console = Console()
        socket = RbhSocket("127.0.0.1", 5002) # read this from config file

        # Connect Signals and Slots
        control_panel.connect_btn.clicked.connect(lambda: socket.connect())
        control_panel.collect_btn.clicked.connect(lambda: socket.collect_sensor_data())
        # control_panel.display_btn.clicked.connect(lambda: socket.get_data())
        control_panel.display_btn.clicked.connect(self.update_terminal)

        # Add Containers to Layouts
        top.addWidget(self.console)
        bottom.addWidget(control_panel)

        # Add Layouts to Main Layout
        main.addLayout(top)
        main.addLayout(bottom)

        # Desktop Configuration
        self.setLayout(main)
        self.setGeometry(175, 50, 600, 650)
        self.setWindowTitle('QMUL RBH')

    def update_terminal(self):
        data = "[INFO] This is a test message"
        self.console.update_data(data)
