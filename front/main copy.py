import sys
from PySide6 import QtWidgets, QtCore, QtUiTools
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox
import threading
import time
from com_port import COMConnector
from all_functions import refresh_ports
from motor_command import MotorCommand
from input_registers import InputRegisters
from holding_registers import HoldingRegisters
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

time_between_frame = 0.02


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QtUiTools.QUiLoader()
        self.main_window = loader.load("main_window.ui", self)
        self.initialize_window()

    def initialize_window(self) -> None:
        """Initialize the window"""
        self.get_ui_element()
        self.setCentralWidget(self.main_window)
        self.modbus_client = None
        self.polling = False
        refresh_ports(self.comboBox_ComPorts)

    def get_ui_element(self) -> None:
        """Access UI elements"""
        self.comboBox_ComPorts: QtWidgets.QComboBox = self.main_window.findChild(
            QtWidgets.QComboBox, "comboBox_ComPorts"
        )
        self.pushButton_connect: QtWidgets.QPushButton = self.main_window.findChild(
            QtWidgets.QPushButton, "pushButton_conncet"
        )
        self.pushButton_start: QtWidgets.QPushButton = self.main_window.findChild(
            QtWidgets.QPushButton, "pushButton_start"
        )
        self.pushButton_stop: QtWidgets.QPushButton = self.main_window.findChild(
            QtWidgets.QPushButton, "pushButton_stop"
        )
        self.pushButton_abort: QtWidgets.QPushButton = self.main_window.findChild(
            QtWidgets.QPushButton, "pushButton_abort"
        )
        self.pushButton_clear: QtWidgets.QPushButton = self.main_window.findChild(
            QtWidgets.QPushButton, "pushButton_clear"
        )
        self.pushButton_suspend: QtWidgets.QPushButton = self.main_window.findChild(
            QtWidgets.QPushButton, "pushButton_suspend"
        )
        self.pushButton_unsuspend: QtWidgets.QPushButton = self.main_window.findChild(
            QtWidgets.QPushButton, "pushButton_unsuspend"
        )
        self.pushButton_reset: QtWidgets.QPushButton = self.main_window.findChild(
            QtWidgets.QPushButton, "pushButton_reset"
        )
        self.label_motStatus: QtWidgets.QLabel = self.main_window.findChild(
            QtWidgets.QLabel, "label_motStatus"
        )
        self.label_consol: QtWidgets.QLabel = self.main_window.findChild(QtWidgets.QLabel, "label_consol")

    def set_connection(self) -> None:
        """Define the connections"""
        self.comboBox_ComPorts.currentTextChanged.connect(self.connect_to_port)

    def connect_to_port(self, current_port: str) -> None:
        """Connection to the port for COM Port ComboBox"""
        selected_port = self.port_combobox.get()
        if selected_port:
            try:
                self.modbus_client = ModbusClient(
                    method="rtu",
                    port=current_port,
                    baudrate=115200,
                    stopbits=1,
                    parity="N",
                    bytesize=8,
                    timeout=1,
                )
                if self.modbus_client.connect():
                    self.label_consol.setText(self.label_consol.text() + "\n" + f"Connected to {current_port}")
                    self.start_polling()
                else:
                    self.label_consol.setText(self.label_consol.text() + "\n" + f"Failed to connect to {current_port}"
                    )
            except Exception as e:
                self.label_consol.setText(self.label_consol.text() + "\n" + f"Failed to connect: {e}")
        else:
            self.label_consol.setText(self.label_consol.text() + "\n" + "No port selected")

    def start_polling(self) -> None:
        """Start the polling after the connection"""
        if self.modbus_client and self.modbus_client.is_socket_open():
            self.polling = True
            threading.Thread(target=self.poll_data).start()
        else:
            self.label_consol.setText(self.label_consol.text() + "\n" + "Not connected to any port")

class TestOk():
    def __init__(self):
        self.setWindowTitle("COM Port Connector")

        main_layout = QHBoxLayout(self)

        self.com_port_frame = QGroupBox("Port COM")
        self.motor_command_frame = QGroupBox("Commande Moteur")
        self.input_registers_frame = QGroupBox("Input Registers")
        self.holding_registers_frame = QGroupBox("Holding Registers")

        main_layout.addWidget(self.com_port_frame)
        main_layout.addWidget(self.motor_command_frame)
        main_layout.addWidget(self.input_registers_frame)
        main_layout.addWidget(self.holding_registers_frame)

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
            threading.Thread(target=self.poll_data, daemon=True).start()
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


# if __name__ == "__main__":
app = QApplication(sys.argv)
window = MainWindow()
window.main_window.show()
app.exec()
