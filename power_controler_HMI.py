import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

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

        self.frame_label = tk.Label(root, text="Frame to send:")
        self.frame_label.pack()

        self.frame_entry = tk.Entry(root)
        self.frame_entry.pack()

        self.send_button = tk.Button(root, text="Send Frame", command=self.send_frame)
        self.send_button.pack()

        self.serial_connection = None
        self.refresh_ports()

    def refresh_ports(self):
        self.port_combobox['values'] = [port.device for port in serial.tools.list_ports.comports()]
        if self.port_combobox['values']:
            self.port_combobox.current(0)

    def connect_to_port(self):
        selected_port = self.port_combobox.get()
        if selected_port:
            try:
                self.serial_connection = serial.Serial(
                    selected_port,
                    115200,  # Baud rate
                    timeout=1,
                    parity=serial.PARITY_NONE,  # No parity
                    stopbits=serial.STOPBITS_ONE  # One stop bit
                )
                self.status_label.config(text=f"Connected to {selected_port}")
            except Exception as e:
                self.status_label.config(text=f"Failed to connect: {e}")
        else:
            self.status_label.config(text="No port selected")

    def send_frame(self):
        if self.serial_connection and self.serial_connection.is_open:
            frame = self.frame_entry.get()
            if frame:
                try:
                    self.serial_connection.write(frame.encode())
                    self.status_label.config(text=f"Frame sent: {frame}")
                except Exception as e:
                    self.status_label.config(text=f"Failed to send frame: {e}")
            else:
                self.status_label.config(text="No frame entered")
        else:
            self.status_label.config(text="Not connected to any port")

if __name__ == "__main__":
    root = tk.Tk()
    app = COMConnectorApp(root)
    root.mainloop()