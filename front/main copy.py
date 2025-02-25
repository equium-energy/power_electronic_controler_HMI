import sys
from typing import List
from PySide6 import QtWidgets, QtCore, QtUiTools
from PySide6.QtWidgets import QApplication
import threading
import time

import pymodbus.exceptions
from common_fct import refresh_ports
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import pymodbus

time_between_frame = 0.1


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile("front/main_window.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        self.main_window = loader.load(ui_file, self)
        ui_file.close()
        self.modbus_client = None
        self.polling = False
        self.initialize_window()

    def initialize_window(self) -> None:
        """Initialize the window"""
        self.get_ui_element()
        self.setCentralWidget(self.main_window)
        self.set_ports()
        self.set_connection()
        self.customize_table()

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
        self.label_consol: QtWidgets.QLabel = self.main_window.findChild(
            QtWidgets.QLabel, "label_consol"
        )
        self.table_temp: QtWidgets.QTableWidget = self.main_window.findChild(
            QtWidgets.QTableWidget, "table_temp"
        )
        self.table_motor1: QtWidgets.QTableWidget = self.main_window.findChild(
            QtWidgets.QTableWidget, "table_motor1"
        )
        self.table_motor2: QtWidgets.QTableWidget = self.main_window.findChild(
            QtWidgets.QTableWidget, "table_motor2"
        )
        self.table_power: QtWidgets.QTableWidget = self.main_window.findChild(
            QtWidgets.QTableWidget, "table_power"
        )
        self.table_other: QtWidgets.QTableWidget = self.main_window.findChild(
            QtWidgets.QTableWidget, "table_other"
        )
        self.table_hold_regi_1: QtWidgets.QTableWidget = self.main_window.findChild(
            QtWidgets.QTableWidget, "table_holdRegi1"
        )
        self.table_hold_regi_2: QtWidgets.QTableWidget = self.main_window.findChild(
            QtWidgets.QTableWidget, "table_holdRegi2"
        )

    def customize_table(self) -> None:
        """Customize the Input and Holding register tables"""
        self.table_temp.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_motor1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_motor2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_power.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_other.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def set_connection(self) -> None:
        """Define the connections fot the Q objects"""
        self.comboBox_ComPorts.activated.connect(self.set_ports)
        self.pushButton_connect.clicked.connect(self.connect_to_port)
        self.pushButton_start.clicked.connect(self.start_cmd)
        self.pushButton_stop.clicked.connect(self.stop_cmd)
        self.pushButton_abort.clicked.connect(self.abort_cmd)
        self.pushButton_clear.clicked.connect(self.clear_cmd)
        self.pushButton_suspend.clicked.connect(self.suspend_cmd)
        self.pushButton_unsuspend.clicked.connect(self.unsuspend_cmd)
        self.pushButton_reset.clicked.connect(self.reset_cmd)

    def set_ports(self) -> None:
        """Call functtion to refresh the ports"""
        refresh_ports(self.comboBox_ComPorts)

    def connect_to_port(self) -> None:
        """Connection to the port for COM Port ComboBox"""
        current_port = self.comboBox_ComPorts.currentText()
        if current_port:
            try:
                self.modbus_client = ModbusClient(
                    method="rtu",
                    port=current_port,
                    baudrate=19200,
                    stopbits=1,
                    parity="N",
                    bytesize=8,
                    timeout=1,
                )
                if self.modbus_client.connect():
                    self.label_consol.setText(
                        self.label_consol.text() + "\n" + f"Connected to {current_port}"
                    )
                    self.start_polling()
                else:
                    self.label_consol.setText(
                        self.label_consol.text()
                        + "\n"
                        + f"Failed to connect to {current_port}"
                    )
            except Exception as e:
                self.label_consol.setText(
                    self.label_consol.text() + "\n" + f"Failed to connect: {e}"
                )
        else:
            self.label_consol.setText(
                self.label_consol.text() + "\n" + "No port selected"
            )

    def start_polling(self) -> None:
        """Start the polling after the connection"""
        if self.modbus_client and self.modbus_client.is_socket_open():
            self.polling = True
            threading.Thread(target=self.poll_data).start()
        else:
            self.label_consol.setText(
                self.label_consol.text() + "\n" + "Not connected to any port"
            )

    def poll_data(self) -> None:
        """Poll the data from input and golding registers"""
        while self.polling:
            try:
                time.sleep(time_between_frame)
                self.read_input_register()
                time.sleep(time_between_frame)
                self.read_holding_registers()
            except Exception as e:
                self.label_consol.setText(
                    self.label_consol.text() + "\n" + f"Failed to read data: {e}"
                )
                self.polling = False

    def start_cmd(self) -> None:
        """Start button signal"""
        self.send_command(1)

    def stop_cmd(self) -> None:
        """Start button signal"""
        self.send_command(2)

    def abort_cmd(self) -> None:
        """Start button signal"""
        self.send_command(3)

    def clear_cmd(self) -> None:
        """Start button signal"""
        self.send_command(4)

    def suspend_cmd(self) -> None:
        """Start button signal"""
        self.send_command(5)

    def unsuspend_cmd(self) -> None:
        """Start button signal"""
        self.send_command(6)

    def reset_cmd(self) -> None:
        """Start button signal"""
        self.send_command(7)

    def send_command(self, command: int):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                response = self.modbus_client.write_register(0, command, unit=1)
                if not response.isError():
                    self.label_consol.setText(
                        self.label_consol.text()
                        + "\n"
                        + f"Command {command} sent successfully"
                    )
                else:
                    self.label_consol.setText(
                        self.label_consol.text()
                        + "\n"
                        + f"Error sending command {command}: {response}"
                    )
            except pymodbus.exceptions.ModbusException as e:
                self.label_consol.setText(
                    self.label_consol.text() + "\n" + f"Modbus Exception: {e}"
                )
            except Exception as e:
                self.label_consol.setText(
                    self.label_consol.text() + "\n" + f"Failed to send command: {e}"
                )
        else:
            self.label_consol.setText(
                self.label_consol.text() + "\n" + "Not connected to any port"
            )

    def read_input_register(self) -> None:
        """Read the input registers to write them in the corresponding table"""
        table_data = {
            self.table_temp: [10, 19, 20, 9, 17, 29],
            self.table_motor1: [3, 11, 13, 12, 5, 7, 26],
            self.table_motor2: [18, 14, 16, 15, 6, 8, 27],
            self.table_power: [21, 22],
            self.table_other: [4, 20, 28],
        }

        # Iterate over the dictionary and set table values
        for table, values in table_data.items():
            self.set_table_value(values, table)

        motor_status = self.modbus_client.read_input_registers(0, 1, unit=1)
        if not motor_status.isError():
            motor_status_value = motor_status.registers[0]
            motor_status_text = self.convert_motor_status(motor_status_value)
            self.label_motStatus.setText(motor_status_text)
        else:
            self.label_motStatus.setText("Error reading Motor Status")

    def set_table_value(
        self, input_list: List[int], table: QtWidgets.QTableWidget
    ) -> None:
        """Set the value in the Input register table"""
        for i, idx in enumerate(input_list):
            gain = 10
            if idx in [26, 27]:
                gain = 100
            input_reg = self.modbus_client.read_input_registers(idx, 1, unit=1)
            if not input_reg.isError():
                val_for_table = str(input_reg.registers[0] / gain)
                table.setItem(0, i, QtWidgets.QTableWidgetItem(val_for_table))
                time.sleep(time_between_frame)
            else:
                table.setItem(0, i, QtWidgets.QTableWidgetItem("Error"))
        time.sleep(time_between_frame)

    def convert_motor_status(self, status_code) -> dict[int, str]:
        """Get the str motor status based on its input response"""
        status_mapping = {
            0: "null",
            1: "idle",
            2: "starting",
            3: "execute",
            4: "holding",
            5: "held",
            6: "unholding",
            7: "suspending",
            8: "suspended",
            9: "unsuspended",
            10: "aborting",
            11: "aborted",
            12: "clearing",
            13: "stopping",
            14: "stopped",
            15: "resetting",
            16: "completing",
            17: "complete",
        }
        return status_mapping.get(status_code, "Unknown Status")

    def read_holding_registers(self) -> None:
        """Read the holding register"""


# if __name__ == "__main__":
app = QApplication(sys.argv)
window = MainWindow()
window.main_window.show()
app.exec()
