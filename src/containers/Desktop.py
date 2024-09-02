from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from containers.ControlPanel.ControlPanel import ControlPanel
from containers.Dashboard.Dashboard import Dashboard
from components.StateMachine import StateMachine
from components.Logo import Logo

class Desktop(QWidget):
    def __init__(self):
        super().__init__()

        # Desktop Containers
        self.logo = Logo()
        self.dashboard = Dashboard()
        self.controlPanel = ControlPanel()
        self.stateMachine = StateMachine()

        # Connect Signals and Slots
        self.stateMachine.sig_console_msg.connect(self.controlPanel.console.update_console)
        self.stateMachine.tactileSensor.sig_tactile_data.connect(self.dashboard.updateDashboard)
        self.stateMachine.tactileSensor.sig_console_msg.connect(self.controlPanel.console.update_console)
        self.controlPanel.controls.motor_ctrls.sig_state_command.connect(self.stateMachine.exec)
        self.controlPanel.controls.sensor_ctrls.sig_state_command.connect(self.stateMachine.exec)
        self.controlPanel.controls.configOptions.sigTactileMode.connect(self.stateMachine.set_mode)
        self.controlPanel.controls.configOptions.sigTactileClassifier.connect(self.stateMachine.set_object)

        # Desktop Layouts
        mainLayout = QVBoxLayout(self)
        mainLayout.setObjectName("desktop")
        dashboardLayout = QHBoxLayout()
        controlPanelLayout = QHBoxLayout()

        # Add Containers to Layouts
        dashboardLayout.addWidget(self.dashboard)
        controlPanelLayout.addWidget(self.controlPanel)

        # Add Layouts to Main Layout
        mainLayout.addWidget(self.logo)
        mainLayout.addLayout(dashboardLayout)
        mainLayout.addLayout(controlPanelLayout)

        # Desktop Configuration
        self.setLayout(mainLayout)
        self.setGeometry(175, 50, 1000, 600)
        self.setWindowTitle('QMUL RBH')