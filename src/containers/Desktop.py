from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from containers.ControlPanel.ControlPanel import ControlPanel
from containers.Console.Console import Console
from containers.Dashboard.Dashboard import Dashboard
from components.StateMachine import StateMachine

class Desktop(QWidget):
    def __init__(self):
        super().__init__()

        # Desktop Layouts
        main = QVBoxLayout(self)
        main.setObjectName("desktop")
        top = QHBoxLayout()
        bottom = QHBoxLayout()

        # Create Components
        control_panel = ControlPanel()
        self.stateMachine = StateMachine()
        self.console = Console()
        self.dashboard = Dashboard()

        # Connect Signals and Slots
        self.stateMachine.sig_console_msg.connect(self.console.update_console)
        self.stateMachine.tactile_sensor.sig_tactile_data.connect(self.dashboard.updateDashboard)
        self.stateMachine.tactile_sensor.sig_console_msg.connect(self.console.update_console)
        control_panel.motor_ctrls.sig_state_command.connect(self.stateMachine.exec)
        control_panel.sensor_ctrls.sig_state_command.connect(self.stateMachine.exec)

        # Add Containers to Layouts
        top.addWidget(self.dashboard)
        bottom.addWidget(control_panel)
        bottom.addWidget(self.console)

        # Add Layouts to Main Layout
        main.addLayout(top)
        main.addLayout(bottom)

        # Desktop Configuration
        self.setLayout(main)
        self.setGeometry(175, 50, 1000, 600)
        self.setWindowTitle('QMUL RBH')