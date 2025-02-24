from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLineEdit, QLabel
from PySide6.QtCore import QTimer
import threading
import time
from com_port import COMConnector
from motor_command import MotorCommand
from input_registers import InputRegisters
from holding_registers import HoldingRegisters

time_between_frame = 0.02

class COMConnectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COM Port Connector")

        self.main_frame = QFrame(self)
        self.setCentralWidget(self.main_frame)

        self.layout = QHBoxLayout(self.main_frame)

        self.com_port_frame = QFrame(self.main_frame)
        self.com_port_frame.setLayout(QVBoxLayout())
        self.layout.addWidget(self.com_port_frame)

        self.motor_command_frame = QFrame(self.main_frame)
        self.motor_command_frame.setLayout(QVBoxLayout())
        self.layout.addWidget(self.motor_command_frame)

        self.input_registers_frame = QFrame(self.main_frame)
        self.input_registers_frame.setLayout(QVBoxLayout())
        self.layout.addWidget(self.input_registers_frame)

        self.holding_registers_frame = QFrame(self.main_frame)
        self.holding_registers_frame.setLayout(QVBoxLayout())
        self.layout.addWidget(self.holding_registers_frame)

        self.com_port = COMConnector(self.com_port_frame)
        self.motor_command = MotorCommand(self.motor_command_frame)
        self.input_registers = InputRegisters(self.input_registers_frame)
        self.holding_registers = HoldingRegisters(self.holding_registers_frame)

        self.modbus_client = None
        self.polling = False
        self.com_port.refresh_ports()

    def start_polling(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            self.polling = True
            threading.Thread(target=self.poll_data).start()
        else:
            self.com_port.status_label.setText("Not connected to any port")

    def poll_data(self):
        while self.polling:
            try:
                time.sleep(time_between_frame)
                self.input_registers.read_input_registers(self.modbus_client)
                time.sleep(time_between_frame)
                self.holding_registers.read_holding_registers(self.modbus_client)
            except Exception as e:
                self.com_port.status_label.setText(f"Failed to read data: {e}")

    def connect_to_port(self):
        self.modbus_client = self.com_port.modbus_client
        self.motor_command.modbus_client = self.modbus_client
        self.motor_command.status_label = self.com_port.status_label
        self.input_registers.modbus_client = self.modbus_client
        self.input_registers.status_label = self.com_port.status_label
        self.holding_registers.modbus_client = self.modbus_client
        self.holding_registers.status_label = self.com_port.status_label

if __name__ == "__main__":
    app = QApplication([])
    window = COMConnectorApp()
    window.show()
    app.exec()
