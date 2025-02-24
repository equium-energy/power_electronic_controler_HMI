import tkinter as tk
import time
from pymodbus.exceptions import ModbusException

time_between_frame = 0.02


class HoldingRegisters:
    def __init__(self, frame):
        self.frame = frame
        self.create_holding_registers()

    def create_holding_registers(self):
        self.initial_frequency_label = tk.Label(
            self.frame, text="Initial Frequency (1000): N/A"
        )
        self.initial_frequency_label.pack(anchor="w")

        self.initial_frequency_entry = tk.Entry(self.frame)
        self.initial_frequency_entry.pack(anchor="w")
        self.initial_frequency_entry.bind(
            "<Return>", self.on_enter_pressed_initial_frequency
        )

        self.max_dc_voltage_label = tk.Label(
            self.frame, text="Max DC Bus Voltage (1001): N/A"
        )
        self.max_dc_voltage_label.pack(anchor="w")

        self.max_dc_voltage_entry = tk.Entry(self.frame)
        self.max_dc_voltage_entry.pack(anchor="w")
        self.max_dc_voltage_entry.bind("<Return>", self.on_enter_pressed_max_dc_voltage)

        self.min_dc_voltage_label = tk.Label(
            self.frame, text="Min DC Bus Voltage (1002): N/A"
        )
        self.min_dc_voltage_label.pack(anchor="w")

        self.min_dc_voltage_entry = tk.Entry(self.frame)
        self.min_dc_voltage_entry.pack(anchor="w")
        self.min_dc_voltage_entry.bind("<Return>", self.on_enter_pressed_min_dc_voltage)

        self.max_ac_voltage_motor1_label = tk.Label(
            self.frame, text="Max AC Voltage Motor 1 (1003): N/A"
        )
        self.max_ac_voltage_motor1_label.pack(anchor="w")

        self.max_ac_voltage_motor1_entry = tk.Entry(self.frame)
        self.max_ac_voltage_motor1_entry.pack(anchor="w")
        self.max_ac_voltage_motor1_entry.bind(
            "<Return>", self.on_enter_pressed_max_ac_voltage_motor1
        )

        self.max_ac_voltage_motor2_label = tk.Label(
            self.frame, text="Max AC Voltage Motor 2 (1004): N/A"
        )
        self.max_ac_voltage_motor2_label.pack(anchor="w")

        self.max_ac_voltage_motor2_entry = tk.Entry(self.frame)
        self.max_ac_voltage_motor2_entry.pack(anchor="w")
        self.max_ac_voltage_motor2_entry.bind(
            "<Return>", self.on_enter_pressed_max_ac_voltage_motor2
        )

        self.ac_current_motor1_label = tk.Label(
            self.frame, text="AC Current Motor 1 (1005): N/A"
        )
        self.ac_current_motor1_label.pack(anchor="w")

        self.ac_current_motor1_entry = tk.Entry(self.frame)
        self.ac_current_motor1_entry.pack(anchor="w")
        self.ac_current_motor1_entry.bind(
            "<Return>", self.on_enter_pressed_ac_current_motor1
        )

        self.ac_current_motor2_label = tk.Label(
            self.frame, text="AC Current Motor 2 (1006): N/A"
        )
        self.ac_current_motor2_label.pack(anchor="w")

        self.ac_current_motor2_entry = tk.Entry(self.frame)
        self.ac_current_motor2_entry.pack(anchor="w")
        self.ac_current_motor2_entry.bind(
            "<Return>", self.on_enter_pressed_ac_current_motor2
        )

        self.max_mcu_temperature_label = tk.Label(
            self.frame, text="Max MCU Temperature (1007): N/A"
        )
        self.max_mcu_temperature_label.pack(anchor="w")

        self.max_mcu_temperature_entry = tk.Entry(self.frame)
        self.max_mcu_temperature_entry.pack(anchor="w")
        self.max_mcu_temperature_entry.bind(
            "<Return>", self.on_enter_pressed_max_mcu_temperature
        )

        self.max_radiator_temperature_label = tk.Label(
            self.frame, text="Max Radiator Temperature (1008): N/A"
        )
        self.max_radiator_temperature_label.pack(anchor="w")

        self.max_radiator_temperature_entry = tk.Entry(self.frame)
        self.max_radiator_temperature_entry.pack(anchor="w")
        self.max_radiator_temperature_entry.bind(
            "<Return>", self.on_enter_pressed_max_radiator_temperature
        )

        self.sweep_min_frequency_label = tk.Label(
            self.frame, text="Sweep Min Frequency (1009): N/A"
        )
        self.sweep_min_frequency_label.pack(anchor="w")

        self.sweep_min_frequency_entry = tk.Entry(self.frame)
        self.sweep_min_frequency_entry.pack(anchor="w")
        self.sweep_min_frequency_entry.bind(
            "<Return>", self.on_enter_pressed_sweep_min_frequency
        )

        self.sweep_max_frequency_label = tk.Label(
            self.frame, text="Sweep Max Frequency (1010): N/A"
        )
        self.sweep_max_frequency_label.pack(anchor="w")

        self.sweep_max_frequency_entry = tk.Entry(self.frame)
        self.sweep_max_frequency_entry.pack(anchor="w")
        self.sweep_max_frequency_entry.bind(
            "<Return>", self.on_enter_pressed_sweep_max_frequency
        )

        self.sweep_stabilization_label = tk.Label(
            self.frame, text="Sweep Stabilization (1011): N/A"
        )
        self.sweep_stabilization_label.pack(anchor="w")

        self.sweep_stabilization_entry = tk.Entry(self.frame)
        self.sweep_stabilization_entry.pack(anchor="w")
        self.sweep_stabilization_entry.bind(
            "<Return>", self.on_enter_pressed_sweep_stabilization
        )

    def on_enter_pressed_initial_frequency(self, event):
        self.write_initial_frequency()

    def on_enter_pressed_max_dc_voltage(self, event):
        self.write_max_dc_voltage()

    def on_enter_pressed_min_dc_voltage(self, event):
        self.write_min_dc_voltage()

    def on_enter_pressed_max_ac_voltage_motor1(self, event):
        self.write_max_ac_voltage_motor1()

    def on_enter_pressed_max_ac_voltage_motor2(self, event):
        self.write_max_ac_voltage_motor2()

    def on_enter_pressed_ac_current_motor1(self, event):
        self.write_ac_current_motor1()

    def on_enter_pressed_ac_current_motor2(self, event):
        self.write_ac_current_motor2()

    def on_enter_pressed_max_mcu_temperature(self, event):
        self.write_max_mcu_temperature()

    def on_enter_pressed_max_radiator_temperature(self, event):
        self.write_max_radiator_temperature()

    def on_enter_pressed_sweep_min_frequency(self, event):
        self.write_sweep_min_frequency()

    def on_enter_pressed_sweep_max_frequency(self, event):
        self.write_sweep_max_frequency()

    def on_enter_pressed_sweep_stabilization(self, event):
        self.write_sweep_stabilization()

    def write_initial_frequency(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.initial_frequency_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1000, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"Initial Frequency (1000) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing Initial Frequency: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Initial Frequency: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_max_dc_voltage(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_dc_voltage_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1001, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"Max DC Bus Voltage (1001) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing Max DC Bus Voltage: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write Max DC Bus Voltage: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def write_min_dc_voltage(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.min_dc_voltage_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1002, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"Min DC Bus Voltage (1002) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing Min DC Bus Voltage: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write Min DC Bus Voltage: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def write_max_ac_voltage_motor1(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_ac_voltage_motor1_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1003, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"Max AC Voltage Motor 1 (1003) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing Max AC Voltage Motor 1: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write Max AC Voltage Motor 1: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def write_max_ac_voltage_motor2(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_ac_voltage_motor2_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1004, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"Max AC Voltage Motor 2 (1004) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing Max AC Voltage Motor 2: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write Max AC Voltage Motor 2: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def write_ac_current_motor1(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.ac_current_motor1_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1005, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"AC Current Motor 1 (1005) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing AC Current Motor 1: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write AC Current Motor 1: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def write_ac_current_motor2(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.ac_current_motor2_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1006, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"AC Current Motor 2 (1006) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing AC Current Motor 2: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write AC Current Motor 2: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def write_max_mcu_temperature(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_mcu_temperature_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1007, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"Max MCU Temperature (1007) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing Max MCU Temperature: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write Max MCU Temperature: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def write_max_radiator_temperature(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_radiator_temperature_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1008, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"Max Radiator Temperature (1008) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing Max Radiator Temperature: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write Max Radiator Temperature: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def write_sweep_min_frequency(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.sweep_min_frequency_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1009, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"Sweep Min Frequency (1009) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing Sweep Min Frequency: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write Sweep Min Frequency: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def write_sweep_max_frequency(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.sweep_max_frequency_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1010, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"Sweep Max Frequency (1010) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing Sweep Max Frequency: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write Sweep Max Frequency: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def write_sweep_stabilization(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.sweep_stabilization_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(
                    1011, value_to_write, unit=1
                )
                if not response.isError():
                    self.status_label.config(
                        text=f"Sweep Stabilization (1011) written successfully"
                    )
                else:
                    self.status_label.config(
                        text=f"Error writing Sweep Stabilization: {response}"
                    )
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(
                    text=f"Failed to write Sweep Stabilization: {e}"
                )
        else:
            self.status_label.config(text="Not connected to any port")

    def read_holding_registers(self):
        try:
            time.sleep(time_between_frame)
            initial_frequency_response = self.modbus_client.read_holding_registers(
                1000, 1, unit=1
            )
            time.sleep(time_between_frame)
            max_dc_voltage_response = self.modbus_client.read_holding_registers(
                1001, 1, unit=1
            )
            time.sleep(time_between_frame)
            min_dc_voltage_response = self.modbus_client.read_holding_registers(
                1002, 1, unit=1
            )
            time.sleep(time_between_frame)
            max_ac_voltage_motor1_response = self.modbus_client.read_holding_registers(
                1003, 1, unit=1
            )
            time.sleep(time_between_frame)
            max_ac_voltage_motor2_response = self.modbus_client.read_holding_registers(
                1004, 1, unit=1
            )
            time.sleep(time_between_frame)
            ac_current_motor1_response = self.modbus_client.read_holding_registers(
                1005, 1, unit=1
            )
            time.sleep(time_between_frame)
            ac_current_motor2_response = self.modbus_client.read_holding_registers(
                1006, 1, unit=1
            )
            time.sleep(time_between_frame)
            max_mcu_temperature_response = self.modbus_client.read_holding_registers(
                1007, 1, unit=1
            )
            time.sleep(time_between_frame)
            max_radiator_temperature_response = (
                self.modbus_client.read_holding_registers(1008, 1, unit=1)
            )
            time.sleep(time_between_frame)
            sweep_min_frequency_response = self.modbus_client.read_holding_registers(
                1009, 1, unit=1
            )
            time.sleep(time_between_frame)
            sweep_max_frequency_response = self.modbus_client.read_holding_registers(
                1010, 1, unit=1
            )
            time.sleep(time_between_frame)
            sweep_stabilization_response = self.modbus_client.read_holding_registers(
                1011, 1, unit=1
            )

            if not initial_frequency_response.isError():
                raw_initial_frequency_value = initial_frequency_response.registers[0]
                initial_frequency = raw_initial_frequency_value / 10
                self.initial_frequency_label.config(
                    text=f"Initial Frequency: {initial_frequency} Hz"
                )
            else:
                self.initial_frequency_label.config(
                    text=f"Error reading Initial Frequency"
                )

            if not max_dc_voltage_response.isError():
                raw_max_dc_voltage_value = max_dc_voltage_response.registers[0]
                max_dc_voltage = raw_max_dc_voltage_value / 10
                self.max_dc_voltage_label.config(
                    text=f"Max DC Bus Voltage: {max_dc_voltage} V"
                )
            else:
                self.max_dc_voltage_label.config(
                    text=f"Error reading Max DC Bus Voltage"
                )

            if not min_dc_voltage_response.isError():
                raw_min_dc_voltage_value = min_dc_voltage_response.registers[0]
                min_dc_voltage = raw_min_dc_voltage_value / 10
                self.min_dc_voltage_label.config(
                    text=f"Min DC Bus Voltage: {min_dc_voltage} V"
                )
            else:
                self.min_dc_voltage_label.config(
                    text=f"Error reading Min DC Bus Voltage"
                )

            if not max_ac_voltage_motor1_response.isError():
                raw_max_ac_voltage_motor1_value = (
                    max_ac_voltage_motor1_response.registers[0]
                )
                max_ac_voltage_motor1 = raw_max_ac_voltage_motor1_value / 10
                self.max_ac_voltage_motor1_label.config(
                    text=f"Max AC Voltage Motor 1: {max_ac_voltage_motor1} V"
                )
            else:
                self.max_ac_voltage_motor1_label.config(
                    text=f"Error reading Max AC Voltage Motor 1"
                )

            if not max_ac_voltage_motor2_response.isError():
                raw_max_ac_voltage_motor2_value = (
                    max_ac_voltage_motor2_response.registers[0]
                )
                max_ac_voltage_motor2 = raw_max_ac_voltage_motor2_value / 10
                self.max_ac_voltage_motor2_label.config(
                    text=f"Max AC Voltage Motor 2: {max_ac_voltage_motor2} V"
                )
            else:
                self.max_ac_voltage_motor2_label.config(
                    text=f"Error reading Max AC Voltage Motor 2"
                )

            if not ac_current_motor1_response.isError():
                raw_ac_current_motor1_value = ac_current_motor1_response.registers[0]
                ac_current_motor1 = raw_ac_current_motor1_value / 10
                self.ac_current_motor1_label.config(
                    text=f"AC Current Motor 1: {ac_current_motor1} A"
                )
            else:
                self.ac_current_motor1_label.config(
                    text=f"Error reading AC Current Motor"
                )

            if not ac_current_motor2_response.isError():
                raw_ac_current_motor2_value = ac_current_motor2_response.registers[0]
                ac_current_motor2 = raw_ac_current_motor2_value / 10
                self.ac_current_motor2_label.config(
                    text=f"AC Current Motor 2: {ac_current_motor2} A"
                )
            else:
                self.ac_current_motor2_label.config(
                    text=f"Error reading AC Current Motor 2"
                )

            if not max_mcu_temperature_response.isError():
                raw_max_mcu_temperature_value = max_mcu_temperature_response.registers[
                    0
                ]
                max_mcu_temperature = raw_max_mcu_temperature_value / 10
                self.max_mcu_temperature_label.config(
                    text=f"Max MCU Temperature: {max_mcu_temperature} °C"
                )
            else:
                self.max_mcu_temperature_label.config(
                    text=f"Error reading Max MCU Temperature"
                )

            if not max_radiator_temperature_response.isError():
                raw_max_radiator_temperature_value = (
                    max_radiator_temperature_response.registers[0]
                )
                max_radiator_temperature = raw_max_radiator_temperature_value / 10
                self.max_radiator_temperature_label.config(
                    text=f"Max Radiator Temperature: {max_radiator_temperature} °C"
                )
            else:
                self.max_radiator_temperature_label.config(
                    text=f"Error reading Max Radiator Temperature"
                )

            if not sweep_min_frequency_response.isError():
                raw_sweep_min_frequency_value = sweep_min_frequency_response.registers[
                    0
                ]
                sweep_min_frequency = raw_sweep_min_frequency_value / 10
                self.sweep_min_frequency_label.config(
                    text=f"Sweep Min Frequency: {sweep_min_frequency} Hz"
                )
            else:
                self.sweep_min_frequency_label.config(
                    text=f"Error reading Sweep Min Frequency"
                )

            if not sweep_max_frequency_response.isError():
                raw_sweep_max_frequency_value = sweep_max_frequency_response.registers[
                    0
                ]
                sweep_max_frequency = raw_sweep_max_frequency_value / 10
                self.sweep_max_frequency_label.config(
                    text=f"Sweep Max Frequency: {sweep_max_frequency} Hz"
                )
            else:
                self.sweep_max_frequency_label.config(
                    text=f"Error reading Sweep Max Frequency"
                )

            if not sweep_stabilization_response.isError():
                raw_sweep_stabilization_value = sweep_stabilization_response.registers[
                    0
                ]
                sweep_stabilization = raw_sweep_stabilization_value / 10
                self.sweep_stabilization_label.config(
                    text=f"Sweep Stabilization: {sweep_stabilization} ms"
                )
            else:
                self.sweep_stabilization_label.config(
                    text=f"Error reading Sweep Stabilization"
                )

        except ModbusException as e:
            self.status_label.config(text=f"Modbus Exception: {e}")
        except Exception as e:
            self.status_label.config(text=f"Failed to read holding registers: {e}")
