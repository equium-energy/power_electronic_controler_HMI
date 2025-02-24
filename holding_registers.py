from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout
import time
from pymodbus.exceptions import ModbusException

time_between_frame = 0.02

class HoldingRegisters:
    def __init__(self, frame):
        self.frame = frame
        self.layout = QVBoxLayout(self.frame)
        self.create_holding_registers()

    def create_holding_registers(self):
        self.initial_frequency_label = QLabel("Initial Frequency (1000): N/A", self.frame)
        self.layout.addWidget(self.initial_frequency_label)

        self.initial_frequency_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.initial_frequency_entry)
        self.initial_frequency_entry.returnPressed.connect(self.write_initial_frequency)

        self.max_dc_voltage_label = QLabel("Max DC Bus Voltage (1001): N/A", self.frame)
        self.layout.addWidget(self.max_dc_voltage_label)

        self.max_dc_voltage_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.max_dc_voltage_entry)
        self.max_dc_voltage_entry.returnPressed.connect(self.write_max_dc_voltage)

        self.min_dc_voltage_label = QLabel("Min DC Bus Voltage (1002): N/A", self.frame)
        self.layout.addWidget(self.min_dc_voltage_label)

        self.min_dc_voltage_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.min_dc_voltage_entry)
        self.min_dc_voltage_entry.returnPressed.connect(self.write_min_dc_voltage)

        self.max_ac_voltage_motor1_label = QLabel("Max AC Voltage Motor 1 (1003): N/A", self.frame)
        self.layout.addWidget(self.max_ac_voltage_motor1_label)

        self.max_ac_voltage_motor1_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.max_ac_voltage_motor1_entry)
        self.max_ac_voltage_motor1_entry.returnPressed.connect(self.write_max_ac_voltage_motor1)

        self.max_ac_voltage_motor2_label = QLabel("Max AC Voltage Motor 2 (1004): N/A", self.frame)
        self.layout.addWidget(self.max_ac_voltage_motor2_label)

        self.max_ac_voltage_motor2_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.max_ac_voltage_motor2_entry)
        self.max_ac_voltage_motor2_entry.returnPressed.connect(self.write_max_ac_voltage_motor2)

        self.ac_current_motor1_label = QLabel("AC Current Motor 1 (1005): N/A", self.frame)
        self.layout.addWidget(self.ac_current_motor1_label)

        self.ac_current_motor1_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.ac_current_motor1_entry)
        self.ac_current_motor1_entry.returnPressed.connect(self.write_ac_current_motor1)

        self.ac_current_motor2_label = QLabel("AC Current Motor 2 (1006): N/A", self.frame)
        self.layout.addWidget(self.ac_current_motor2_label)

        self.ac_current_motor2_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.ac_current_motor2_entry)
        self.ac_current_motor2_entry.returnPressed.connect(self.write_ac_current_motor2)

        self.max_mcu_temperature_label = QLabel("Max MCU Temperature (1007): N/A", self.frame)
        self.layout.addWidget(self.max_mcu_temperature_label)

        self.max_mcu_temperature_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.max_mcu_temperature_entry)
        self.max_mcu_temperature_entry.returnPressed.connect(self.write_max_mcu_temperature)

        self.max_radiator_temperature_label = QLabel("Max Radiator Temperature (1008): N/A", self.frame)
        self.layout.addWidget(self.max_radiator_temperature_label)

        self.max_radiator_temperature_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.max_radiator_temperature_entry)
        self.max_radiator_temperature_entry.returnPressed.connect(self.write_max_radiator_temperature)

        self.sweep_min_frequency_label = QLabel("Sweep Min Frequency (1009): N/A", self.frame)
        self.layout.addWidget(self.sweep_min_frequency_label)

        self.sweep_min_frequency_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.sweep_min_frequency_entry)
        self.sweep_min_frequency_entry.returnPressed.connect(self.write_sweep_min_frequency)

        self.sweep_max_frequency_label = QLabel("Sweep Max Frequency (1010): N/A", self.frame)
        self.layout.addWidget(self.sweep_max_frequency_label)

        self.sweep_max_frequency_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.sweep_max_frequency_entry)
        self.sweep_max_frequency_entry.returnPressed.connect(self.write_sweep_max_frequency)

        self.sweep_stabilization_label = QLabel("Sweep Stabilization (1011): N/A", self.frame)
        self.layout.addWidget(self.sweep_stabilization_label)

        self.sweep_stabilization_entry = QLineEdit(self.frame)
        self.layout.addWidget(self.sweep_stabilization_entry)
        self.sweep_stabilization_entry.returnPressed.connect(self.write_sweep_stabilization)

    def write_initial_frequency(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.initial_frequency_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1000, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Initial Frequency (1000) written successfully")
                else:
                    self.status_label.setText(f"Error writing Initial Frequency: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write Initial Frequency: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_max_dc_voltage(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_dc_voltage_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1001, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Max DC Bus Voltage (1001) written successfully")
                else:
                    self.status_label.setText(f"Error writing Max DC Bus Voltage: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write Max DC Bus Voltage: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_min_dc_voltage(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.min_dc_voltage_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1002, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Min DC Bus Voltage (1002) written successfully")
                else:
                    self.status_label.setText(f"Error writing Min DC Bus Voltage: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write Min DC Bus Voltage: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_max_ac_voltage_motor1(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_ac_voltage_motor1_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1003, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Max AC Voltage Motor 1 (1003) written successfully")
                else:
                    self.status_label.setText(f"Error writing Max AC Voltage Motor 1: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write Max AC Voltage Motor 1: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_max_ac_voltage_motor2(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_ac_voltage_motor2_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1004, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Max AC Voltage Motor 2 (1004) written successfully")
                else:
                    self.status_label.setText(f"Error writing Max AC Voltage Motor 2: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write Max AC Voltage Motor 2: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_ac_current_motor1(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.ac_current_motor1_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1005, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"AC Current Motor 1 (1005) written successfully")
                else:
                    self.status_label.setText(f"Error writing AC Current Motor 1: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write AC Current Motor 1: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_ac_current_motor2(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.ac_current_motor2_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1006, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"AC Current Motor 2 (1006) written successfully")
                else:
                    self.status_label.setText(f"Error writing AC Current Motor 2: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write AC Current Motor 2: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_max_mcu_temperature(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_mcu_temperature_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1007, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Max MCU Temperature (1007) written successfully")
                else:
                    self.status_label.setText(f"Error writing Max MCU Temperature: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write Max MCU Temperature: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_max_radiator_temperature(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_radiator_temperature_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1008, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Max Radiator Temperature (1008) written successfully")
                else:
                    self.status_label.setText(f"Error writing Max Radiator Temperature: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write Max Radiator Temperature: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_sweep_min_frequency(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.sweep_min_frequency_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1009, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Sweep Min Frequency (1009) written successfully")
                else:
                    self.status_label.setText(f"Error writing Sweep Min Frequency: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write Sweep Min Frequency: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_sweep_max_frequency(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.sweep_max_frequency_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1010, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Sweep Max Frequency (1010) written successfully")
                else:
                    self.status_label.setText(f"Error writing Sweep Max Frequency: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write Sweep Max Frequency: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def write_sweep_stabilization(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.sweep_stabilization_entry.text())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1011, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.setText(f"Sweep Stabilization (1011) written successfully")
                else:
                    self.status_label.setText(f"Error writing Sweep Stabilization: {response}")
            except ValueError:
                self.status_label.setText("Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.setText(f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.setText(f"Failed to write Sweep Stabilization: {e}")
        else:
            self.status_label.setText("Not connected to any port")

    def read_holding_registers(self):
        try:
            time.sleep(time_between_frame)
            initial_frequency_response = self.modbus_client.read_holding_registers(1000, 1, unit=1)
            time.sleep(time_between_frame)
            max_dc_voltage_response = self.modbus_client.read_holding_registers(1001, 1, unit=1)
            time.sleep(time_between_frame)
            min_dc_voltage_response = self.modbus_client.read_holding_registers(1002, 1, unit=1)
            time.sleep(time_between_frame)
            max_ac_voltage_motor1_response = self.modbus_client.read_holding_registers(1003, 1, unit=1)
            time.sleep(time_between_frame)
            max_ac_voltage_motor2_response = self.modbus_client.read_holding_registers(1004, 1, unit=1)
            time.sleep(time_between_frame)
            ac_current_motor1_response = self.modbus_client.read_holding_registers(1005, 1, unit=1)
            time.sleep(time_between_frame)
            ac_current_motor2_response = self.modbus_client.read_holding_registers(1006, 1, unit=1)
            time.sleep(time_between_frame)
            max_mcu_temperature_response = self.modbus_client.read_holding_registers(1007, 1, unit=1)
            time.sleep(time_between_frame)
            max_radiator_temperature_response = self.modbus_client.read_holding_registers(1008, 1, unit=1)
            time.sleep(time_between_frame)
            sweep_min_frequency_response = self.modbus_client.read_holding_registers(1009, 1, unit=1)
            time.sleep(time_between_frame)
            sweep_max_frequency_response = self.modbus_client.read_holding_registers(1010, 1, unit=1)
            time.sleep(time_between_frame)
            sweep_stabilization_response = self.modbus_client.read_holding_registers(1011, 1, unit=1)

            if not initial_frequency_response.isError():
                raw_initial_frequency_value = initial_frequency_response.registers[0]
                initial_frequency = raw_initial_frequency_value / 10
                self.initial_frequency_label.setText(f"Initial Frequency: {initial_frequency} Hz")
            else:
                self.initial_frequency_label.setText(f"Error reading Initial Frequency")

            if not max_dc_voltage_response.isError():
                raw_max_dc_voltage_value = max_dc_voltage_response.registers[0]
                max_dc_voltage = raw_max_dc_voltage_value / 10
                self.max_dc_voltage_label.setText(f"Max DC Bus Voltage: {max_dc_voltage} V")
            else:
                self.max_dc_voltage_label.setText(f"Error reading Max DC Bus Voltage")

            if not min_dc_voltage_response.isError():
                raw_min_dc_voltage_value = min_dc_voltage_response.registers[0]
                min_dc_voltage = raw_min_dc_voltage_value / 10
                self.min_dc_voltage_label.setText(f"Min DC Bus Voltage: {min_dc_voltage} V")
            else:
                self.min_dc_voltage_label.setText(f"Error reading Min DC Bus Voltage")

            if not max_ac_voltage_motor1_response.isError():
                raw_max_ac_voltage_motor1_value = max_ac_voltage_motor1_response.registers[0]
                max_ac_voltage_motor1 = raw_max_ac_voltage_motor1_value / 10
                self.max_ac_voltage_motor1_label.setText(f"Max AC Voltage Motor 1: {max_ac_voltage_motor1} V")
            else:
                self.max_ac_voltage_motor1_label.setText(f"Error reading Max AC Voltage Motor 1")

            if not max_ac_voltage_motor2_response.isError():
                raw_max_ac_voltage_motor2_value = max_ac_voltage_motor2_response.registers[0]
                max_ac_voltage_motor2 = raw_max_ac_voltage_motor2_value / 10
                self.max_ac_voltage_motor2_label.setText(f"Max AC Voltage Motor 2: {max_ac_voltage_motor2} V")
            else:
                self.max_ac_voltage_motor2_label.setText(f"Error reading Max AC Voltage Motor 2")

            if not ac_current_motor1_response.isError():
                raw_ac_current_motor1_value = ac_current_motor1_response.registers[0]
                ac_current_motor1 = raw_ac_current_motor1_value / 10
                self.ac_current_motor1_label.setText(f"AC Current Motor 1: {ac_current_motor1} A")
            else:
                self.ac_current_motor1_label.setText(f"Error reading AC Current Motor")

            if not ac_current_motor2_response.isError():
                raw_ac_current_motor2_value = ac_current_motor2_response.registers[0]
                ac_current_motor2 = raw_ac_current_motor2_value / 10
                self.ac_current_motor2_label.setText(f"AC Current Motor 2: {ac_current_motor2} A")
            else:
                self.ac_current_motor2_label.setText(f"Error reading AC Current Motor 2")

            if not max_mcu_temperature_response.isError():
                raw_max_mcu_temperature_value = max_mcu_temperature_response.registers[0]
                max_mcu_temperature = raw_max_mcu_temperature_value / 10
                self.max_mcu_temperature_label.setText(f"Max MCU Temperature: {max_mcu_temperature} °C")
            else:
                self.max_mcu_temperature_label.setText(f"Error reading Max MCU Temperature")

            if not max_radiator_temperature_response.isError():
                raw_max_radiator_temperature_value = max_radiator_temperature_response.registers[0]
                max_radiator_temperature = raw_max_radiator_temperature_value / 10
                self.max_radiator_temperature_label.setText(f"Max Radiator Temperature: {max_radiator_temperature} °C")
            else:
                self.max_radiator_temperature_label.setText(f"Error reading Max Radiator Temperature")

            if not sweep_min_frequency_response.isError():
                raw_sweep_min_frequency_value = sweep_min_frequency_response.registers[0]
                sweep_min_frequency = raw_sweep_min_frequency_value / 10
                self.sweep_min_frequency_label.setText(f"Sweep Min Frequency: {sweep_min_frequency} Hz")
            else:
                self.sweep_min_frequency_label.setText(f"Error reading Sweep Min Frequency")

            if not sweep_max_frequency_response.isError():
                raw_sweep_max_frequency_value = sweep_max_frequency_response.registers[0]
                sweep_max_frequency = raw_sweep_max_frequency_value / 10
                self.sweep_max_frequency_label.setText(f"Sweep Max Frequency: {sweep_max_frequency} Hz")
            else:
                self.sweep_max_frequency_label.setText(f"Error reading Sweep Max Frequency")

            if not sweep_stabilization_response.isError():
                raw_sweep_stabilization_value = sweep_stabilization_response.registers[0]
                sweep_stabilization = raw_sweep_stabilization_value / 10
                self.sweep_stabilization_label.setText(f"Sweep Stabilization: {sweep_stabilization} ms")
            else:
                self.sweep_stabilization_label.setText(f"Error reading Sweep Stabilization")

        except ModbusException as e:
            self.status_label.setText(f"Modbus Exception: {e}")
        except Exception as e:
            self.status_label.setText(f"Failed to read holding registers: {e}")
