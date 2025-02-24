import threading
import serial
from PySide6 import QtWidgets
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


def refresh_ports(element: QtWidgets.QComboBox) -> None:
    """Refresh the port"""
    ports = [port.device for port in serial.tools.list_ports.comports()]
    element.clear()  # Clear previous values
    element.addItems(ports)  # Add new values
    # Set the first item as the default selection if there are available ports
    if ports:
        element.setCurrentIndex(0)


def connect_to_port(port_combobox: QtWidgets.QComboBox):
    selected_port = port_combobox.get()
    if selected_port:
        try:
            modbus_client = ModbusClient(
                method="rtu",
                port=selected_port,
                baudrate=115200,
                stopbits=1,
                parity="N",
                bytesize=8,
                timeout=1,
            )
            if modbus_client.connect():
                self.status_label.config(text=f"Connected to {selected_port}")
            else:
                self.status_label.config(text=f"Failed to connect to {selected_port}")
        except Exception as e:
            self.status_label.config(text=f"Failed to connect: {e}")
    else:
        self.status_label.config(text="No port selected")


def start_polling(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            self.polling = True
            threading.Thread(target=self.poll_data).start()
        else:
            self.status_label.config(text="Not connected to any port")

