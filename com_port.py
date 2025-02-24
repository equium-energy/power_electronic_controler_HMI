from PySide6.QtWidgets import QLabel, QComboBox, QPushButton, QVBoxLayout
import serial.tools.list_ports
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

class COMConnector:
    def __init__(self, frame):
        self.frame = frame
        self.layout = QVBoxLayout(self.frame)

        self.port_label = QLabel("Available COM Ports:", self.frame)
        self.layout.addWidget(self.port_label)

        self.port_combobox = QComboBox(self.frame)
        self.layout.addWidget(self.port_combobox)

        self.connect_button = QPushButton("Connect", self.frame)
        self.connect_button.clicked.connect(self.connect_to_port)
        self.layout.addWidget(self.connect_button)

        self.status_label = QLabel("", self.frame)
        self.layout.addWidget(self.status_label)

        self.start_polling_button = QPushButton("Start Polling", self.frame)
        self.start_polling_button.clicked.connect(self.start_polling)
        self.layout.addWidget(self.start_polling_button)

        self.modbus_client = None

    def refresh_ports(self):
        self.port_combobox.clear()
        self.port_combobox.addItems([port.device for port in serial.tools.list_ports.comports()])
        if self.port_combobox.count() > 0:
            self.port_combobox.setCurrentIndex(0)

    def connect_to_port(self):
        selected_port = self.port_combobox.currentText()
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
                    self.status_label.setText(f"Connected to {selected_port}")
                else:
                    self.status_label.setText(f"Failed to connect to {selected_port}")
            except Exception as e:
                self.status_label.setText(f"Failed to connect: {e}")
        else:
            self.status_label.setText("No port selected")

    def start_polling(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            self.polling = True
            threading.Thread(target=self.poll_data).start()
        else:
            self.status_label.setText("Not connected to any port")
