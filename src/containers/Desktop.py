from PyQt6.QtWidgets import QWidget, QVBoxLayout
from containers.ControlPanel.ControlPanel import ControlPanel
from containers.Console.Console import Console
from components.RbhSocket import RbhSocket
from utils.datalog import write_csv, data_format_sensor

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
        control_panel.sensor_ctrls.connect_btn.clicked.connect(lambda: self.sensor_socket.connect())
        control_panel.sensor_ctrls.collect_btn.clicked.connect(self.collect_data)
        control_panel.sensor_ctrls.display_btn.clicked.connect(lambda: self.console.update_data(self.sensor_socket.data))
        control_panel.motor_ctrls.open_btn.clicked.connect(lambda: self.sensor_socket.collect_sensor_data("open"))
        control_panel.motor_ctrls.close_btn.clicked.connect(lambda: self.sensor_socket.collect_sensor_data("close"))

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
        # Write to Console
        self.console.update("--------------------------------------------------------------------------")
        self.console.update("[INFO]: Collecting data from sensor")
        self.console.update("--------------------------------------------------------------------------")

        # Collect Data from Sensor
        self.sensor_socket.collect_sensor_data("collect")

        # Format Data
        sensor_data = data_format_sensor(self.sensor_socket.data)
        
        # Write Data to Console
        for data in sensor_data:
            self.console.update(f"X: {data[0]} \t\t Y: {data[1]} \t\t Z: {data[2]}")

        # Write Data to CSV
        write_csv(sensor_data)

        # Reset Data
        self.sensor_socket.data = []
            
    def update_terminal(self):
        self.console.update_data(self.sensor_socket.data)
