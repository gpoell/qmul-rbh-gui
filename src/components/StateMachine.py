"""
The State Machine serves as a centralized orchestrator for managing the application 
state and executing sensor commands through multithreaded processes. These asynchronous
processes are created as <ThreadWorkers> and managed by the FSM's <QThreadPool> class.
Gripper commands are emitted through the GUI button clicks as "stateCommand" signals. 

Attributes:

    - previousState <str>: tracks the previous state of commands, particularly for the 'idle' and 'connected' state
                            to return to the appropriate state after any transition.
    - state <str>: the current state of the GUI
    - settings: a collection of settings outlined in the settings.yaml that inform the behavior of how the GUI
                collects and processes data.
    - threadpool <QThreadPool>: manages the execution of threadworkers that perform gripper tasks.
    - tactile_sensor <TactileSensor>: facilitates gripper tasks related to the tactile sensor.
    - motor <L9110HMotor>: facilitates motor operations for the gripper.
    - logger <ConsoleLogger>: displays informative data to the Console on the GUI
    - machine <Machine>: a state machine object that manages the transition of states on the gripper

Methods:

    - exec(<str> command)
    - set_mode
    - set_object
    - on_enter_<state>
    - previous_state
    - set_settings
"""

from PyQt6.QtCore import QThreadPool, QObject, pyqtSlot as Slot
from utils.client import TactileSensor, L9110HMotor
from components.ConsoleLogger import ConsoleLogger
from components.Threads import ThreadWorker
from transitions import Machine
import yaml

class StateMachine(QObject):

    def __init__(self):
        super().__init__()
        self.previousState = 'idle'
        self.settings = self._set_settings()
        self.threadpool = QThreadPool()
        self.tactileSensor = TactileSensor()
        self.motor = L9110HMotor()
        self.logger = ConsoleLogger()
        states = ['idle', 'connected', 'collecting', 'calibrating', 'opening', 'closing']
        transitions = [
            # Connect: transition from [idle] to [connected]
            {'trigger': 'connect', 'source': 'idle', 'dest': 'connected'},
            # Collect: transition from [connected] to [collecting] and return to previous state
            {'trigger': 'collect', 'source': 'connected', 'dest': 'collecting', 'after': 'previous_state'},
            # Calibrate: transition from [connected] to [calibrating] and return to previous state
            {'trigger': 'calibrate', 'source': 'connected', 'dest': 'calibrating', 'after': 'previous_state'},
            # Open: transition from [idle or connected] to [opening] and return to previous state
            {'trigger': 'open', 'source': ['idle', 'connected'], 'dest': 'opening', 'after': 'previous_state'},
            # Close: transition from [idle or connected] to [closing] and return to previous state
            {'trigger': 'close', 'source': ['idle', 'connected'], 'dest': 'closing', 'after': 'previous_state'},
            # Disconnect: transition from [connected] to [idle]
            {'trigger': 'idle', 'source': 'connected', 'dest': 'idle'},
        ]
        self.machine = Machine(model=self, states=states, transitions=transitions, initial='idle', auto_transitions=False)

    # Slot decorators that listen for incoming signals from GUI components and execute
    # the functions they wrap underneath.
    @Slot(str, name="stateCommand")
    def exec(self, command):
        """Signals emitted from button click events trigger state transition methods."""
        match command:
            case "connect": self.connect()
            case "collect": self.collect()
            case "calibrate": self.calibrate()
            case "open": self.open()
            case "close": self.close()
            case "disconnect": self.idle()
            case _: self.logger.warn(f"Command [{command}] not recognized by server.")

    @Slot(str, name="tactileMode")
    def set_mode(self, slot_val):
        """Sets the sensor collection mode based on dropdown selection in GUI"""
        self.settings["gripper"]["tactile"]["mode"] = slot_val

    @Slot(str, name="tactileClassifier")
    def set_object(self, slot_val):
        """Sets the classification label for the collection mode based on dropdown selection in GUI"""
        self.settings["gripper"]["tactile"]["classifier"] = slot_val


    # Transition functions between states execute sensor commands through the thread pool.
    # The state machine follows the naming convention <on_enter_[state]> for performing
    # functionality while entering the state.
    def on_enter_connected(self):
        self.logger.info("Connecting to tactile sensor and reading data...")
        self.previousState = self.state
        worker = ThreadWorker(self.tactileSensor.read, self.logger)
        self.threadpool.start(worker)

    def on_enter_calibrating(self):
        self.logger.info("Calibrating tactile sensor...")
        worker = ThreadWorker(self.tactileSensor.calibrate, self.logger)
        self.threadpool.start(worker)

    def on_enter_opening(self):
        self.logger.info("Opening gripper...")
        worker = ThreadWorker(self.motor.open, self.logger)
        self.threadpool.start(worker)

    def on_enter_closing(self):
        self.logger.info("Closing gripper...")
        worker = ThreadWorker(self.motor.close, self.logger)
        self.threadpool.start(worker)

    def on_enter_collecting(self):
        self.logger.info("Collecting tactile sensor data...")
        settings = self.settings['gripper']['tactile']
        worker = ThreadWorker(self.tactileSensor.collect, self.logger, settings)
        self.threadpool.start(worker)

    def on_enter_idle(self):
        self.logger.info("Gripper has resumed idle state...")
        self.previousState = self.state
        worker = ThreadWorker(self.tactileSensor.disconnect, self.logger)
        self.threadpool.start(worker)

    def previous_state(self):
        self.state = self.previousState


    # Initialization method for the FSM settings
    def _set_settings(self):
        """Set the State Machine settings based on the application settings"""
        with open("src/settings.yaml", 'r') as file:
            settings = yaml.safe_load(file)
            settings["gripper"]["tactile"]["mode"] = settings["gripper"]["modes"][0]
            settings["gripper"]["tactile"]["classifier"] = settings["gripper"]["classifiers"][0]
            return settings