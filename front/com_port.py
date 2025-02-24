import threading
import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


class COMConnector:
    def __init__(self, frame):
        self.frame = frame
        self.port_label = tk.Label(self.frame, text="Available COM Ports:")
        self.port_label.pack()

        self.port_combobox = ttk.Combobox(self.frame)
        self.port_combobox.pack()

        self.connect_button = tk.Button(
            self.frame, text="Connect", command=self.connect_to_port
        )
        self.connect_button.pack()

        self.status_label = tk.Label(self.frame, text="")
        self.status_label.pack()

        self.start_polling_button = tk.Button(
            self.frame, text="Start Polling", command=self.start_polling
        )
        self.start_polling_button.pack()

        self.modbus_client = None

    def refresh_ports(self):
        self.port_combobox["values"] = [
            port.device for port in serial.tools.list_ports.comports()
        ]
        if self.port_combobox["values"]:
            self.port_combobox.current(0)

    def connect_to_port(self):
        selected_port = self.port_combobox.get()
        if selected_port:
            try:
                self.modbus_client = ModbusClient(
                    method="rtu",
                    port=selected_port,
                    baudrate=115200,
                    stopbits=1,
                    parity="N",
                    bytesize=8,
                    timeout=1,
                )
                if self.modbus_client.connect():
                    self.status_label.config(text=f"Connected to {selected_port}")
                else:
                    self.status_label.config(
                        text=f"Failed to connect to {selected_port}"
                    )
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
