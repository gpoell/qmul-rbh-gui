"""
Creates a State Machine object.

The State Machine serves as a centralized orchestrator for managing the application 
state and executing sensor commands through multithreaded processes.

Sensor commands are emitted by the GUI buttons as "stateCommand" signals. Sensor functions
are processed through separate threads managed by the <ThreadWorkers> and <QThreadPool> classes.

Classes:

    StateMachine

Attributes:

    state <str>
    threadpool <QThreadPool>
    tactile_sensor <TactileSensor>
    motor <L9110HMotor>

Methods:

    exec(<str> command)
    disconnect
    set_mode
    set_option
"""

from PyQt6.QtCore import QThreadPool, QObject, QRunnable, pyqtSlot as Slot, pyqtSignal as Signal
from components.TactileSensor import TactileSensor
from components.L9110HMotor import L9110HMotor
import yaml

class StateMachine(QObject):

    sig_console_msg = Signal(dict, name="consoleMessage")

    def __init__(self):
        super().__init__()
        self.state = 'idle'
        self.settings = self._set_settings()
        self.threadpool = QThreadPool()
        self.tactile_sensor = TactileSensor()
        self.motor = L9110HMotor()

    @Slot(str, name="stateCommand")
    def exec(self, command):
        """Orchestrates commands emmited by GUI buttons.

            The GUI buttons emit signals to the State Machine which orchestrates
            which sensor functions to execute in separate threads.
    
            Parameters:
                command <str>: command emitted by buttons to execute on Esp32 server
                    options:
                    - read: continuously read tactile sensor data
                    - connect: tests connection with ESP32 server
                    - collect: collects a sample of data from tactile sensor
                    - calibrate: calibrates sensor based on sample size set on ESP32 server
                    - open: opens motor at predetermined duration on ESP32 server
                    - close: closes motor at predetermined duration on ESP32 server
        """
        console_message = {
            "header": "",
            "body": ""
        }
        match command:
            case "connect":
                console_message["body"] = "Connecting to tactile sensor."
                self.state = "running"
                worker = ThreadWorker(self.tactile_sensor.connect)
            case "collect":
                console_message["body"] = "Collecting tactile sensor data..."
                worker = ThreadWorker(self.tactile_sensor.collect, config=self.settings["gripper"]["tactile"])
            case "calibrate":
                console_message["body"] = "Calibrating tactile sensor..."
                worker = ThreadWorker(self.tactile_sensor.calibrate)
            case "open":
                console_message["body"] = "Opening Gripper..."
                self.sig_console_msg.emit(console_message)
                worker = ThreadWorker(lambda: self.motor.move("open"))
            case "close":
                console_message["body"] = "Closing Gripper..."
                worker = ThreadWorker(lambda: self.motor.move("close"))
            case "disconnect":
                console_message["body"] = "Disconnecting tactile sensor thread."
                self.state = "idle"
                worker = ThreadWorker(self.tactile_sensor.disconnect)
            case _:
                console_message["header"] = "warning"
                console_message["body"] = "Command not recognized by server."
                self.sig_console_msg.emit(console_message)
                return

        self.threadpool.start(worker)
        console_message["header"] = "info"
        self.sig_console_msg.emit(console_message)

    def _set_settings(self):
        """Set the State Machine settings based on the application settings"""
        with open("src/settings.yaml", 'r') as file:
            settings = yaml.safe_load(file)
            settings["gripper"]["tactile"]["mode"] = settings["gripper"]["modes"][0]
            settings["gripper"]["tactile"]["classifier"] = settings["gripper"]["classifiers"][0]
            return settings

    @Slot(str, name="tactileMode")
    def set_mode(self, slot_val):
        """Sets the sensor collection mode based on dropdown selection in GUI"""
        self.settings["gripper"]["tactile"]["mode"] = slot_val

    @Slot(str, name="tactileClassifier")
    def set_object(self, slot_val):
        """Sets the classification label for the collection mode based on dropdown selection in GUI"""
        self.settings["gripper"]["tactile"]["classifier"] = slot_val

class ThreadWorker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super(ThreadWorker, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    @Slot()
    def run(self):
        self.func(*self.args, **self.kwargs)