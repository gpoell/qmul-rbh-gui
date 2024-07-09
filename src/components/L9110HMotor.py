"""
The L9110HMotor controls the gripper actuation.

Attributes:

    state <str>: defines the state of the motor

Methods:

    move(direction): moves the motor in the specified direction
"""

from components.EspClient import EspClient

class L9110HMotor:

    def __init__(self):
        self.state = "idle"

    def move(self, direction):
        """
        Open or close the gripper based on direction.
        
        Parameters:
            direction <str>: sends a command to the ESP32 server to rotate the motor.
                options: 
                - open
                - close
        
        """

        # Do not move if motor is running
        assert direction == "open" or direction == "close"
        if self.state == "running": return

        # Connect to server, send command, and update state
        client = EspClient()
        client.connect()
        client.send_data(direction)
        self.state = "running"

        # Read acknowledge bit response from server
        batch = client.receive_data(1)

        # Continuously process data until null bit terminator is received
        while batch != '':
            batch = client.receive_data(64)
            if not batch : break
            print(f"Motor Direction: {batch}")

        # Close client connection and reset state
        client.close()
        self.state = 'idle'