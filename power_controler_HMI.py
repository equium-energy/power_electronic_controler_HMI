import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException
import threading
import time

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

        self.start_polling_button = tk.Button(root, text="Start Polling", command=self.start_polling)
        self.start_polling_button.pack()

        self.dc_voltage_label = tk.Label(root, text="DC Voltage: N/A")
        self.dc_voltage_label.pack()

        self.radiator_temp_label = tk.Label(root, text="Radiator Temperature: N/A")
        self.radiator_temp_label.pack()

        self.holding_register_label = tk.Label(root, text="Initial Frequency (1000): N/A")
        self.holding_register_label.pack()

        self.holding_register_entry = tk.Entry(root)
        self.holding_register_entry.pack()

        self.write_holding_register_button = tk.Button(root, text="Write Initial Frequency", command=self.write_holding_register)
        self.write_holding_register_button.pack()

        self.modbus_client = None
        self.polling = False
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

    def start_polling(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            self.polling = True
            threading.Thread(target=self.poll_data).start()
        else:
            self.status_label.config(text="Not connected to any port")

    def poll_data(self):
        while self.polling:
            try:
                time.sleep(0.25)
                dc_response = self.modbus_client.read_input_registers(4, 1, unit=1)
                time.sleep(0.25)
                radiator_response = self.modbus_client.read_input_registers(10, 1, unit=1)
                time.sleep(0.25)
                holding_response = self.modbus_client.read_holding_registers(1000, 1, unit=1)

                if not dc_response.isError():
                    raw_dc_value = dc_response.registers[0]
                    dc_voltage = raw_dc_value / 10
                    self.dc_voltage_label.config(text=f"DC Voltage: {dc_voltage} V")
                else:
                    self.dc_voltage_label.config(text=f"Error reading DC Voltage: {dc_response}")

                if not radiator_response.isError():
                    raw_radiator_value = radiator_response.registers[0]
                    self.radiator_temp_label.config(text=f"Radiator Temperature: {raw_radiator_value} °C")
                else:
                    self.radiator_temp_label.config(text=f"Error reading Radiator Temperature: {radiator_response}")

                if not holding_response.isError():
                    raw_holding_value = holding_response.registers[0]
                    initial_frequency = raw_holding_value / 10
                    self.holding_register_label.config(text=f"Initial Frequency: {initial_frequency} Hz")
                else:
                    self.holding_register_label.config(text=f"Error reading Initial Frequency: {holding_response}")

            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to read data: {e}")

    def write_holding_register(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.holding_register_entry.get())
                value_to_write = int(value * 10)
                time.sleep(0.25)
                response = self.modbus_client.write_register(1000, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"Initial Frequency (1000) written successfully")
                else:
                    self.status_label.config(text=f"Error writing Initial Frequency: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Initial Frequency: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

if __name__ == "__main__":
    root = tk.Tk()
    app = COMConnectorApp(root)
    root.mainloop()