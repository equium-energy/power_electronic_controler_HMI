import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException

class COMConnectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("COM Port Connector")

        self.port_label = tk.Label(root, text="Available COM Ports:")
        self.port_label.pack()

        self.port_combobox = ttk.Combobox(root)
        self.port_combobox.pack()

        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_port)
        self.connect_button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        self.read_dc_voltage_button = tk.Button(root, text="Read DC Voltage", command=self.read_dc_voltage)
        self.read_dc_voltage_button.pack()

        self.read_radiator_temp_button = tk.Button(root, text="Read Radiator Temperature", command=self.read_radiator_temperature)
        self.read_radiator_temp_button.pack()

        self.response_label = tk.Label(root, text="")
        self.response_label.pack()

        self.modbus_client = None
        self.refresh_ports()

    def refresh_ports(self):
        self.port_combobox['values'] = [port.device for port in serial.tools.list_ports.comports()]
        if self.port_combobox['values']:
            self.port_combobox.current(0)

    def connect_to_port(self):
        selected_port = self.port_combobox.get()
        if selected_port:
            try:
                self.modbus_client = ModbusClient(
                    method='rtu',
                    port=selected_port,
                    baudrate=115200,
                    stopbits=1,
                    parity='N',
                    bytesize=8,
                    timeout=1
                )
                if self.modbus_client.connect():
                    self.status_label.config(text=f"Connected to {selected_port}")
                else:
                    self.status_label.config(text=f"Failed to connect to {selected_port}")
            except Exception as e:
                self.status_label.config(text=f"Failed to connect: {e}")
        else:
            self.status_label.config(text="No port selected")

    def read_dc_voltage(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                response = self.modbus_client.read_input_registers(4, 1, unit=1)
                if not response.isError():
                    raw_value = response.registers[0]
                    dc_voltage = raw_value / 10
                    self.response_label.config(text=f"DC Voltage: {dc_voltage} V")
                else:
                    self.response_label.config(text=f"Error reading DC Voltage: {response}")
            except ModbusException as e:
                self.response_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.response_label.config(text=f"Failed to read DC Voltage: {e}")
        else:
            self.response_label.config(text="Not connected to any port")

    def read_radiator_temperature(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                response = self.modbus_client.read_input_registers(10, 1, unit=1)
                if not response.isError():
                    raw_value = response.registers[0]
                    self.response_label.config(text=f"Radiator Temperature: {raw_value} °C")
                else:
                    self.response_label.config(text=f"Error reading Radiator Temperature: {response}")
            except ModbusException as e:
                self.response_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.response_label.config(text=f"Failed to read Radiator Temperature: {e}")
        else:
            self.response_label.config(text="Not connected to any port")

if __name__ == "__main__":
    root = tk.Tk()
    app = COMConnectorApp(root)
    root.mainloop()