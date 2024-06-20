from PyQt6.QtWidgets import QWidget, QVBoxLayout
from containers.ControlPanel.ControlPanel import ControlPanel
from containers.Console.Console import Console
from components.StateMachine import StateMachine

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
        self.stateMachine = StateMachine()
        self.console = Console()

        # Connect Signals and Slots
        self.stateMachine.tactile_sensor.sig_tactile_data.connect(self.console.tactile_data_format)
        self.stateMachine.tactile_sensor.sig_console_msg.connect(self.console.update)
        control_panel.motor_ctrls.sig_state_command.connect(self.stateMachine.exec)
        control_panel.sensor_ctrls.sig_state_command.connect(self.stateMachine.exec)

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