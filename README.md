# QMUL MSc Advanced Robotics
# Soft Robotic Gripper: Graphical User Interface

## Overview
This application serves as an interface for operating the soft [robotic gripper,]() visualizing its tactile data, and integrating a Random Forest classification model for classifying strawberry ripeness. The GUI is developed with the Python framework [PyQt]() to simplify the composition of graphical components for managing its functionality. The documentation below provides a variety of information for installing the application dependencies and running the application, and an architectural overview explaining how the components are integrated and communicate with the Esp32 MCU to interface with the robotic gripper.

## Table of Contents
1. Installation and Dependencies
2. Running the Application
3. Application Architecture
4. PyQt Components
5. Repository Folder Structure
6. Helpful Articles

## Installation and Dependencies
### Software
Python3 is required to run this application and the latest download insturctions are found [here.](https://www.python.org/downloads/ "Python Downloads"). The current version used at the time of writing this documentation is 3.11.2.
Software     | Version
------      | ------
Python3        | latest

### Python Libraries
The following libraries are required to run the application and can be installed from the repository's [requirements.txt](https://github.com/gpoell/qmul-rbh-gui/blob/main/requirements.txt). See the next section, Running the Application, for more details. 
Library     | Version
------      | ------
PyQt        | PyQt6
pyyaml      | latest
matplotlib  | latest

## Running the Application
Below are prerequisite instructions to clone the repository using SSH and running the application. [Python virtual environments](https://docs.python.org/3/library/venv.html) are highly recommended for managing dependency version conflicts with other applications.

<details>
<summary>Cloning the repository with SSH</summary>

1. Install the latest version of [Python](https://www.python.org/downloads/ "Python Downloads")
2. Connect to your GitHub account with SSH: [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh "Connecting to GitHub with SSH"). Specifically use the instructions below
    1. <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>
    2. <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account>
3. Clone the repository: `git@github.com:gpoell/qmul-rbh-gui.git`
</details>

<details>
<summary>Running the application</summary>

1. Create a [python virtual environment](https://docs.python.org/3/library/venv.html) at the root directory level of the repository
    1. `cd qmul-rbh-gui`
    2. `python -m venv .`
2. Activate the virtual environment and install dependencies
    1. `. Scripts/activate`
    2. `pip install -r requirements.txt`
</details>


## Application Architecture
The GUI is a multithreaded application that communicates with the ESP32 server over Wi-Fi. Commands sent to the server occur during events like pressing buttons. The buttons emit commands as [PyQt signals]() which are received by the State Machine's [PyQt Slots](). The State Machine is a centralized component responsible for monitoring the state of application to ensure events are triggered at the appropriate time (e.g. the gripper cannot open and close at the same time.) and executing commands through seperate [threads]() which is vital for simultaneously reading tactile data and operating the gripper. Each thread maintains a connection with the server using [Python Sockets]() that follows the communication protocol outlined below. Incoming data received from the server is emitted to various GUI components to provide data for visualizations and information for the terminal.

<details>
<summary>PyQt Signals and Slots</summary>

[PyQt Signals and Slots]() are the primary mechanisms for how the various components communicate with each other. Components can emit signals of a specific type to be received by other components with slots that are actively listening for those signals. The functionality of pressing the connect button to read tactile data from the gripper and displaying its information on the console is a perfect example of how to use signals and slots.

When the Connect button (line 18, 19) is clicked, it executes the emit_signal() function (line 33) which broadcasts a signal with the command and signal name (line 6).

<b>SensorControls.py</b>

`6.     sig_state_command = Signal(str, name="stateCommand")`  
`18.    self.connect_btn = QPushButton("Connect")`  
`19.    self.connect_btn.clicked.connect(lambda: self.emit_signal("connect"))`  
`33.    self.sig_state_command.emit(command)`

The State Machine has a slot decorator (line 41) that actively listens for string signals with the name "stateCommand" and uses the value to determine which processes to run in seperate threads (line 42, 58). In this scenario, the "connect" signal executes the Tactile Sensor connect method (line 60).

<b>StateMachine.py</b>

`41.     @Slot(str, name="stateCommand")`  
`42.     def exec(self, command):`  
`58.     case "connect":`  
`60.     worker = ThreadWorker(self.tactile_sensor.connect)`

The Tactile Sensor connect method reads data from the tactile sensor and emits it under a new signal (line 22; 54) that is received by the Console under its Slot decorator. The Console function wrapped by the Slot decorator executes when it receives signals with a tuple type and "tactileData" name which updates the information displayed on the console (line 19, 20).

<b>TactileSensor.py</b>

`22.     sig_tactile_data = Signal(tuple, name='tactileData')`  
`54.     self.sig_tactile_data.emit((batch[0], batch[1], batch[2]))`

<b>Console.py</b>

`19.     @Slot(tuple, name="tactileData")`  
`20.     def tactile_data_format(self, data):`

</details>

<details>
<summary>Python Socket Protocol</summary>

</details>

## PyQt Components

 
## Repository Folder Structure