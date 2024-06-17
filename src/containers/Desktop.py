from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QThreadPool
from containers.ControlPanel.ControlPanel import ControlPanel
from containers.Console.Console import Console
from components.L9110HMotor import L9110HMotor
from components.TactileSensor import TactileSensor
from components.ThreadWorker import ThreadWorker

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
        self.threadpool = QThreadPool()
        self.console = Console()
        self.motor = L9110HMotor("127.0.0.1", 5000) # read this from config file
        self.tactile_sensor = TactileSensor("127.0.0.1", 5000)

        # Connect Signals and Slots
        self.tactile_sensor.signal.connect(self.console.tactile_data_format)
        self.tactile_sensor.console_msg.connect(self.console.update)
        control_panel.sensor_ctrls.connect_btn.clicked.connect(self.connect_sensor)
        control_panel.sensor_ctrls.collect_btn.clicked.connect(self.collect_data)
        control_panel.motor_ctrls.open_btn.clicked.connect(lambda: self.move_motor("open"))
        control_panel.motor_ctrls.close_btn.clicked.connect(lambda: self.move_motor("close"))

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

    def connect_sensor(self):
        worker = ThreadWorker(self.tactile_sensor.connect)
        self.threadpool.start(worker)

    def collect_data(self):
        worker = ThreadWorker(self.tactile_sensor.collect)
        self.threadpool.start(worker)

    def move_motor(self, direction):
        if self.motor.state == 'inactive':
            worker = ThreadWorker(self.motor.move, direction)
            self.threadpool.start(worker)