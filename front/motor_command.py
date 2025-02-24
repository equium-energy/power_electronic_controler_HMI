import tkinter as tk
from pymodbus.exceptions import ModbusException


class MotorCommand:
    def __init__(self, frame):
        self.frame = frame
        self.create_motor_command_buttons()
        self.motor_status_label = tk.Label(self.frame, text="Motor Status: N/A")
        self.motor_status_label.pack(pady=5)

    def create_motor_command_buttons(self):
        self.start_button = tk.Button(
            self.frame, text="Start", command=lambda: self.send_command(1)
        )
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(
            self.frame, text="Stop", command=lambda: self.send_command(2)
        )
        self.stop_button.pack(pady=5)

        self.abort_button = tk.Button(
            self.frame, text="Abort", command=lambda: self.send_command(3)
        )
        self.abort_button.pack(pady=5)

        self.clear_button = tk.Button(
            self.frame, text="Clear", command=lambda: self.send_command(4)
        )
        self.clear_button.pack(pady=5)

        self.suspend_button = tk.Button(
            self.frame, text="Suspend", command=lambda: self.send_command(5)
        )
        self.suspend_button.pack(pady=5)

        self.unsuspend_button = tk.Button(
            self.frame, text="Unsuspend", command=lambda: self.send_command(6)
        )
        self.unsuspend_button.pack(pady=5)

        self.reset_button = tk.Button(
            self.frame, text="Reset", command=lambda: self.send_command(7)
        )
        self.reset_button.pack(pady=5)

    def send_command(self, command):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                response = self.modbus_client.write_register(0, command, unit=1)
                if not response.isError():
                    self.status_label.config(
                        text=f"Command {command} sent successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error sending command {command}: {response}"
                    )
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to send command: {e}")
        else:
            self.status_label.config(text="Not connected to any port")
