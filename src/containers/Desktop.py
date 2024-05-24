from PyQt6.QtWidgets import QWidget, QVBoxLayout
from containers.ControlPanel.ControlPanel import ControlPanel
from containers.Console.Console import Console
from components.RbhSocket import RbhSocket
from src.utils.datalog import write_csv

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
        self.sensor_socket = RbhSocket("127.0.0.1", 80) # read this from config file

        # Connect Signals and Slots
        control_panel.connect_btn.clicked.connect(lambda: self.sensor_socket.connect())
        control_panel.collect_btn.clicked.connect(self.collect_data)
        control_panel.display_btn.clicked.connect(lambda: self.console.update_data(self.sensor_socket.data))

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

    # Temporary method for testing data collection
    def collect_data(self):
        # Collect Data from Sensor
        self.sensor_socket.collect_sensor_data("collect")
        
        # Write Data to Console
        
        # Write Data to CSV
        write_csv(self.sensor_socket.data)

        # Reset Data
        self.sensor_socket.data = []
            
    def update_terminal(self):
        self.console.update_data(self.sensor_socket.data)
