from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout
from pymodbus.exceptions import ModbusException

class MotorCommand:
    def __init__(self, frame):
        self.frame = frame
        self.layout = QVBoxLayout(self.frame)
        self.create_motor_command_buttons()
        self.motor_status_label = QLabel("Motor Status: N/A", self.frame)
        self.layout.addWidget(self.motor_status_label)

    def create_motor_command_buttons(self):
        self.start_button = QPushButton("Start", self.frame)
        self.start_button.clicked.connect(lambda: self.send_command(1))
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self.frame)
        self.stop_button.clicked.connect(lambda: self.send_command(2))
        self.layout.addWidget(self.stop_button)

        self.abort_button = QPushButton("Abort", self.frame)
        self.abort_button.clicked.connect(lambda: self.send_command(3))
        self.layout.addWidget(self.abort_button)

        self.clear_button = QPushButton("Clear", self.frame)
        self.clear_button.clicked.connect(lambda: self.send_command(4))
        self.layout.addWidget(self.clear_button)

        self.suspend_button = QPushButton("Suspend", self.frame)
        self.suspend_button.clicked.connect(lambda: self.send_command(5))
        self.layout.addWidget(self.suspend_button)

        self.unsuspend_button = QPushButton("Unsuspend", self.frame)
        self.unsuspend_button.clicked.connect(lambda: self.send_command(6))
        self.layout.addWidget(self.unsuspend_button)

        self.reset_button = QPushButton("Reset", self.frame)
        self.reset_button.clicked.connect(lambda: self.send_command(7))
        self.layout.addWidget(self.reset_button)

    def send_command(self, command):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                response = self.modbus_client.write_register(0, command, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Command {command} sent successfully")
                else:
                    self.status_label.setText(f"Error sending command {command}: {response}")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to send command: {e}")
        else:
            self.status_label.setText("Not connected to any port")
