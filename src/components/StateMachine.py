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
"""

from PyQt6.QtCore import QThreadPool, QObject, pyqtSlot as Slot
from components.TactileSensor import TactileSensor
from components.L9110HMotor import L9110HMotor
from components.ThreadWorker import ThreadWorker

class StateMachine(QObject):

    def __init__(self):
        super().__init__()
        self.state = 'idle'
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
                    - open: opens motor at predetermined duration on ESP32 server
                    - close: closes motor at predetermined duration on ESP32 server
        """
        match command:
            case "connect":
                self.state = "running"
                worker = ThreadWorker(self.tactile_sensor.connect)
            case "collect":
                worker = ThreadWorker(self.tactile_sensor.collect)
            case "open":
                worker = ThreadWorker(lambda: self.motor.move("open"))
            case "close":
                worker = ThreadWorker(lambda: self.motor.move("close"))
            case "disconnect":
                self.state = "idle"
                worker = ThreadWorker(self.tactile_sensor.disconnect)
            case _:
                print("[WARNING]: Command not recognized by server.")
                return

        self.threadpool.start(worker)