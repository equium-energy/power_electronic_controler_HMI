import tkinter as tk
from tkinter import ttk
import threading
import time
from com_port import COMConnector
from motor_command import MotorCommand
from input_registers import InputRegisters
from holding_registers import HoldingRegisters

time_between_frame = 0.02

class COMConnectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("COM Port Connector")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand="yes")

        self.com_port_frame = tk.LabelFrame(self.main_frame, text="Port COM")
        self.com_port_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.motor_command_frame = tk.LabelFrame(self.main_frame, text="Commande Moteur")
        self.motor_command_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.input_registers_frame = tk.LabelFrame(self.main_frame, text="Input Registers")
        self.input_registers_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.holding_registers_frame = tk.LabelFrame(self.main_frame, text="Holding Registers")
        self.holding_registers_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

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
            self.com_port.status_label.config(text="Not connected to any port")

    def poll_data(self):
        while self.polling:
            try:
                time.sleep(time_between_frame)
                self.input_registers.read_input_registers(self.modbus_client)
                time.sleep(time_between_frame)
                self.holding_registers.read_holding_registers(self.modbus_client)
            except Exception as e:
                self.com_port.status_label.config(text=f"Failed to read data: {e}")

    def connect_to_port(self):
        self.modbus_client = self.com_port.modbus_client
        self.motor_command.modbus_client = self.modbus_client
        self.motor_command.status_label = self.com_port.status_label
        self.input_registers.modbus_client = self.modbus_client
        self.input_registers.status_label = self.com_port.status_label
        self.holding_registers.modbus_client = self.modbus_client
        self.holding_registers.status_label = self.com_port.status_label

if __name__ == "__main__":
    root = tk.Tk()
    app = COMConnectorApp(root)
    root.mainloop()
