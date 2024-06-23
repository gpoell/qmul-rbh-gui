# QMUL MSc Advanced Robotics
# Soft Robotic Gripper GUI

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

PyQt signals and slots are the primary mechanisms for how the various components communicate with each other. Components can emit signals of a specific type and are received by any slot actively listening for it. The process for connecting signals and slots can be confusing, so a detailed example of how this works is outlined below.

When the user clicks the Connect button, the  "connect" command is emitted as a signal containing a string type and a name called "stateCommand".

<b>SensorControls.py</b>

`6.     sig_state_command = Signal(str, name="stateCommand")`  
`33.    self.sig_state_command.emit(command)`

The State Machine has a slot decorator that actively listens for string signals with the name "stateCommand" and uses the value to process the command in its exec() method.

<b>StateMachine.py</b>

`41.     @Slot(str, name="stateCommand")`  
`42.     def exec(self, command):`

</details>

<details>
<summary>Python Socket Protocol</summary>

</details>

## PyQt Components

 
## Repository Folder Structure