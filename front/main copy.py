import sys
from typing import List
from PySide6 import QtWidgets, QtCore, QtUiTools, QtGui
from PySide6.QtWidgets import QApplication
import threading
import time

import pymodbus.exceptions
from common_fct import refresh_ports
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import pymodbus

from table_creation import create_temp_table, create_motor_table, create_pow_table, create_other_table, create_holding_1, create_holding_2

time_between_frame = 0.05


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile("front/main_window_img.ui")
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
        self.set_menu()

    def set_menu(self) -> None:
        """Set the menu bar to add help section"""
        about_action = QtGui.QAction("Print packML", self)
        about_action.triggered.connect(self.show_about)
        self.menu_help.addAction(about_action)

    def show_about(self) -> None:
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("pack ML")
        # Load and set an image
        pixmap = QtGui.QPixmap("./front/pack_ml.jpg")  # Replace with your image path
        print(pixmap)
        msg_box.setIconPixmap(pixmap)
        msg_box.exec()

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
        self.pushButton_refresh: QtWidgets.QPushButton = self.main_window.findChild(
            QtWidgets.QPushButton, "pushButton_refresh"
        )
        self.pushButton_clean: QtWidgets.QPushButton = self.main_window.findChild(
            QtWidgets.QPushButton, "pushButton_console"
        )
        self.label_motStatus: QtWidgets.QLabel = self.main_window.findChild(
            QtWidgets.QLabel, "label_motStatus"
        )
        self.label_consol: QtWidgets.QLabel = self.main_window.findChild(
            QtWidgets.QLabel, "label_console"
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
        self.menu_help: QtWidgets.QMenu = self.main_window.findChild(
            QtWidgets.QMenu, "menuHelp"
        )

    def customize_table(self) -> None:
        """Customize the Input and Holding register tables"""
        self.table_temp.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_motor1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_motor2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_power.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_other.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.set_column_size(self.table_other, {2: 150})
        self.set_column_size(self.table_hold_regi_1, {2: 150, 3: 150})
        self.set_column_size(self.table_hold_regi_2, {0: 120, 2: 80, 6: 85})
        # INPUT
        create_temp_table(self.table_temp)
        self.set_column_size(self.table_temp, {0: 80, 1: 80, 2: 80, 3: 80, 4: 80,5: 80, 6: 80})
        create_motor_table(self.table_motor1)
        create_motor_table(self.table_motor2)
        create_pow_table(self.table_power)
        create_other_table(self.table_other)
        # HOLDING
        create_holding_1(self.table_hold_regi_1)
        create_holding_2(self.table_hold_regi_2)

    def set_column_size(
        self, table: QtWidgets.QTableWidget, col_size: dict[int, int]
    ) -> None:
        """Define the size of the column of the table"""
        for x, y in col_size.items():
            table.setColumnWidth(x, y)

    def set_row_size(self, table: QtWidgets.QTableWidget, row_size: dict[int, int]) -> None:
        """Define the row height of a table"""
        for x, y in row_size.items():
            table.setRowHeight(x, y)

    def disable_row(self, table: QtWidgets.QTableWidget, row: int) -> None:
        """Disable editing a specific row in the selected table"""
        for col in range(table.colorCount()):
            item = table.item(row, col)
            if item:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

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
        self.pushButton_refresh.clicked.connect(self.refresh_cmd)
        self.pushButton_clean.clicked.connect(self.clean_console)
        self.table_hold_regi_1.cellChanged.connect(self.write_holding_register1)
        self.table_hold_regi_2.cellChanged.connect(self.write_holding_register2)

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
                self.read_protection()
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

    def refresh_cmd(self) -> None:
        """Refresh command for COM"""
        self.set_ports()

    def clean_console(self) -> None:
        """Clean the consol"""
        self.label_consol.clear()


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
                table.setItem(2, i, QtWidgets.QTableWidgetItem(val_for_table))
                time.sleep(time_between_frame)
            else:
                table.setItem(2, i, QtWidgets.QTableWidgetItem("Error"))
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
        list_reg1 = [1001, 1002, 1003, 1004, 1005, 1006]
        self.set_holding_registers(list_reg1, self.table_hold_regi_1)
        list_reg2 = [1007, 1008, 1000, 1009, 1010, 1011, 2]
        self.set_holding_registers(list_reg2, self.table_hold_regi_2)

    def set_holding_registers(
        self, list_reg: List[int], table: QtWidgets.QTableWidget
    ) -> None:
        """Set the input in the table"""
        for i, idx in enumerate(list_reg):
            holding_reg = self.modbus_client.read_holding_registers(idx, 1, unit=1)
            if not holding_reg.isError():
                holding_reg_value = holding_reg.registers[0]
                holding_reg_frq = str(holding_reg_value / 10)
                table.setItem(0, i, QtWidgets.QTableWidgetItem(holding_reg_frq))
            else:
                table.setItem(0, i, QtWidgets.QTableWidgetItem("Error"))
            time.sleep(time_between_frame)
        self.disable_row(table, 0)
        time.sleep(time_between_frame)

    def write_holding_register1(self, row: int, col: int) -> None:
        """Write and send the holding resgister"""
        if row != 0:
            dict_col = {
                0: 1001,
                1: 1002,
                2: 1003,
                3: 1004,
                4: 1005,
                5: 1006,
            }
            self.set_writing_hr(dict_col, self.table_hold_regi_1, row, col)

    def write_holding_register2(self, row: int, col: int) -> None:
        """Write and send the holding resgister"""
        if row != 0:
            dict_col = {
                0: 1007,
                1: 1008,
                2: 1000,
                3: 1009,
                4: 1010,
                5: 1011,
            }
            self.set_writing_hr(dict_col, self.table_hold_regi_2, row, col)

    def set_writing_hr(self, dict_col: dict[int, int], table: QtWidgets.QTableWidget, row: int, col: int) -> None:
        """Write holding registers in the write table"""
        if row != 0:
            if self.modbus_client and self.modbus_client.is_socket_open():
                try:
                    value = int(table.item(row, col))
                except:
                    self.label_consol.setText("Invalid input")
                value_to_write = int(value) * 10
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    dict_col[col], value_to_write, unit=1
                )
                if response.isError():
                    self.label_consol.setText("Error writing")
            else:
                self.label_consol.setText("Not connected to any port")

    def read_protection(self) -> None:
        """Read the protection and add them to the console"""
        if self.modbus_client and self.modbus_client.is_socket_open():
            code_alarm = self.modbus_client.read_input_registers(100, 1, unit=1)


app = QApplication(sys.argv)
window = MainWindow()
window.main_window.show()
sys.exit(app.exec())
