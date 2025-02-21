import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException
import threading
import time

time_between_frame = 0.02

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

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand="yes")

        self.input_registers_frame = tk.LabelFrame(self.main_frame, text="Input Registers")
        self.input_registers_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.holding_registers_frame = tk.LabelFrame(self.main_frame, text="Holding Registers")
        self.holding_registers_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.create_input_registers()
        self.create_holding_registers()

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
                time.sleep(time_between_frame)
                self.read_input_registers()
                time.sleep(time_between_frame)
                self.read_holding_registers()
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to read data: {e}")

    def read_input_registers(self):
        try:
            time.sleep(time_between_frame)
            dc_response = self.modbus_client.read_input_registers(4, 1, unit=1)
            time.sleep(time_between_frame)
            radiator_response = self.modbus_client.read_input_registers(10, 1, unit=1)

            if not dc_response.isError():
                raw_dc_value = dc_response.registers[0]
                dc_voltage = raw_dc_value / 10
                self.dc_voltage_label.config(text=f"DC Voltage: {dc_voltage} V")
            else:
                self.dc_voltage_label.config(text=f"Error reading DC Voltage: {dc_response}")

            if not radiator_response.isError():
                raw_radiator_value = radiator_response.registers[0]/10
                self.radiator_temp_label.config(text=f"Radiator Temperature: {raw_radiator_value} °C")
            else:
                self.radiator_temp_label.config(text=f"Error reading Radiator Temperature: {radiator_response}")

            time.sleep(time_between_frame)
            live_frequency_motor1_response = self.modbus_client.read_input_registers(3, 1, unit=1)
            if not live_frequency_motor1_response.isError():
                raw_live_frequency_motor1_value = live_frequency_motor1_response.registers[0]
                live_frequency_motor1 = raw_live_frequency_motor1_value / 10
                self.live_frequency_motor1_label.config(text=f"Live Frequency Motor 1: {live_frequency_motor1} Hz")
            else:
                self.live_frequency_motor1_label.config(text=f"Error reading Live Frequency Motor 1: {live_frequency_motor1_response}")

            time.sleep(time_between_frame)
            live_frequency_motor2_response = self.modbus_client.read_input_registers(18, 1, unit=1)
            if not live_frequency_motor2_response.isError():
                raw_live_frequency_motor2_value = live_frequency_motor2_response.registers[0]
                live_frequency_motor2 = raw_live_frequency_motor2_value / 10
                self.live_frequency_motor2_label.config(text=f"Live Frequency Motor 2: {live_frequency_motor2} Hz")
            else:
                self.live_frequency_motor2_label.config(text=f"Error reading Live Frequency Motor 2: {live_frequency_motor2_response}")

            time.sleep(time_between_frame)
            dc_bus_voltage_response = self.modbus_client.read_input_registers(4, 1, unit=1)
            if not dc_bus_voltage_response.isError():
                raw_dc_bus_voltage_value = dc_bus_voltage_response.registers[0]
                dc_bus_voltage = raw_dc_bus_voltage_value / 10
                self.dc_bus_voltage_label.config(text=f"DC Bus Voltage: {dc_bus_voltage} V")
            else:
                self.dc_bus_voltage_label.config(text=f"Error reading DC Bus Voltage: {dc_bus_voltage_response}")

            time.sleep(time_between_frame)
            ac_voltage_motor1_response = self.modbus_client.read_input_registers(5, 1, unit=1)
            if not ac_voltage_motor1_response.isError():
                raw_ac_voltage_motor1_value = ac_voltage_motor1_response.registers[0]
                ac_voltage_motor1 = raw_ac_voltage_motor1_value / 10
                self.ac_voltage_motor1_label.config(text=f"AC Voltage Motor 1: {ac_voltage_motor1} V")
            else:
                self.ac_voltage_motor1_label.config(text=f"Error reading AC Voltage Motor 1: {ac_voltage_motor1_response}")

            time.sleep(time_between_frame)
            ac_voltage_motor2_response = self.modbus_client.read_input_registers(6, 1, unit=1)
            if not ac_voltage_motor2_response.isError():
                raw_ac_voltage_motor2_value = ac_voltage_motor2_response.registers[0]
                ac_voltage_motor2 = raw_ac_voltage_motor2_value / 10
                self.ac_voltage_motor2_label.config(text=f"AC Voltage Motor 2: {ac_voltage_motor2} V")
            else:
                self.ac_voltage_motor2_label.config(text=f"Error reading AC Voltage Motor 2: {ac_voltage_motor2_response}")

            time.sleep(time_between_frame)
            RMS_current_motor1_response = self.modbus_client.read_input_registers(7, 1, unit=1)
            if not RMS_current_motor1_response.isError():
                raw_ac_current_motor1_value = RMS_current_motor1_response.registers[0]
                ac_current_motor1 = raw_ac_current_motor1_value / 10
                self.ac_current_motor1_label.config(text=f"AC Current Motor 1: {ac_current_motor1} mA")
            else:
                self.ac_current_motor1_label.config(text=f"Error reading AC Current Motor 1: {RMS_current_motor1_response}")

            time.sleep(time_between_frame)
            RMS_current_motor2_response = self.modbus_client.read_input_registers(8, 1, unit=1)
            if not RMS_current_motor2_response.isError():
                raw_ac_current_motor2_value = RMS_current_motor2_response.registers[0]
                ac_current_motor2 = raw_ac_current_motor2_value / 10
                self.ac_current_motor2_label.config(text=f"AC Current Motor 2: {ac_current_motor2} mA")
            else:
                self.ac_current_motor2_label.config(text=f"Error reading AC Current Motor 2: {RMS_current_motor2_response}")

            time.sleep(time_between_frame)
            mcu_temperature_response = self.modbus_client.read_input_registers(9, 1, unit=1)
            if not mcu_temperature_response.isError():
                raw_mcu_temperature_value = mcu_temperature_response.registers[0]
                mcu_temperature = raw_mcu_temperature_value / 10
                self.mcu_temperature_label.config(text=f"MCU Temperature: {mcu_temperature} °C")
            else:
                self.mcu_temperature_label.config(text=f"Error reading MCU Temperature: {mcu_temperature_response}")

            time.sleep(time_between_frame)
            mcu_temperature_min_response = self.modbus_client.read_input_registers(17, 1, unit=1)
            if not mcu_temperature_min_response.isError():
                raw_mcu_temperature_min_value = mcu_temperature_min_response.registers[0]
                mcu_temperature_min = raw_mcu_temperature_min_value / 10
                self.mcu_temperature_min_label.config(text=f"MCU Temperature Min (life): {mcu_temperature_min} °C")
            else:
                self.mcu_temperature_min_label.config(text=f"Error reading MCU Temperature Min (life): {mcu_temperature_min_response}")

            time.sleep(time_between_frame)
            mcu_temperature_max_response = self.modbus_client.read_input_registers(18, 1, unit=1)
            if not mcu_temperature_max_response.isError():
                raw_mcu_temperature_max_value = mcu_temperature_max_response.registers[0]
                mcu_temperature_max = raw_mcu_temperature_max_value / 10
                self.mcu_temperature_max_label.config(text=f"MCU Temperature Max (life): {mcu_temperature_max} °C")
            else:
                self.mcu_temperature_max_label.config(text=f"Error reading MCU Temperature Max (life): {mcu_temperature_max_response}")

            time.sleep(time_between_frame)
            radiator_temperature_min_response = self.modbus_client.read_input_registers(19, 1, unit=1)
            if not radiator_temperature_min_response.isError():
                raw_radiator_temperature_min_value = radiator_temperature_min_response.registers[0]
                radiator_temperature_min = raw_radiator_temperature_min_value / 10
                self.radiator_temperature_min_label.config(text=f"Radiator Temperature Min (life): {radiator_temperature_min} °C")
            else:
                self.radiator_temperature_min_label.config(text=f"Error reading Radiator Temperature Min (life): {radiator_temperature_min_response}")

            time.sleep(time_between_frame)
            radiator_temperature_max_response = self.modbus_client.read_input_registers(20, 1, unit=1)
            if not radiator_temperature_max_response.isError():
                raw_radiator_temperature_max_value = radiator_temperature_max_response.registers[0]
                radiator_temperature_max = raw_radiator_temperature_max_value / 10
                self.radiator_temperature_max_label.config(text=f"Radiator Temperature Max (life): {radiator_temperature_max} °C")
            else:
                self.radiator_temperature_max_label.config(text=f"Error reading Radiator Temperature Max (life): {radiator_temperature_max_response}")

            time.sleep(time_between_frame)
            motor1_position_average_response = self.modbus_client.read_input_registers(11, 1, unit=1)
            if not motor1_position_average_response.isError():
                raw_motor1_position_average_value = motor1_position_average_response.registers[0]
                motor1_position_average = raw_motor1_position_average_value / 10
                self.motor1_position_average_label.config(text=f"Motor 1 Position Average: {motor1_position_average} mm")
            else:
                self.motor1_position_average_label.config(text=f"Error reading Motor 1 Position Average: {motor1_position_average_response}")

            time.sleep(time_between_frame)
            motor1_position_max_response = self.modbus_client.read_input_registers(12, 1, unit=1)
            if not motor1_position_max_response.isError():
                raw_motor1_position_max_value = motor1_position_max_response.registers[0]
                motor1_position_max = raw_motor1_position_max_value / 10
                self.motor1_position_max_label.config(text=f"Motor 1 Position Max: {motor1_position_max} mm")
            else:
                self.motor1_position_max_label.config(text=f"Error reading Motor 1 Position Max: {motor1_position_max_response}")

            time.sleep(time_between_frame)
            motor1_position_min_response = self.modbus_client.read_input_registers(13, 1, unit=1)
            if not motor1_position_min_response.isError():
                raw_motor1_position_min_value = motor1_position_min_response.registers[0]
                motor1_position_min = raw_motor1_position_min_value / 10
                self.motor1_position_min_label.config(text=f"Motor 1 Position Min: {motor1_position_min} mm")
            else:
                self.motor1_position_min_label.config(text=f"Error reading Motor 1 Position Min: {motor1_position_min_response}")

            time.sleep(time_between_frame)
            motor2_position_average_response = self.modbus_client.read_input_registers(14, 1, unit=1)
            if not motor2_position_average_response.isError():
                raw_motor2_position_average_value = motor2_position_average_response.registers[0]
                motor2_position_average = raw_motor2_position_average_value / 10
                self.motor2_position_average_label.config(text=f"Motor 2 Position Average: {motor2_position_average} mm")
            else:
                self.motor2_position_average_label.config(text=f"Error reading Motor 2 Position Average: {motor2_position_average_response}")

            time.sleep(time_between_frame)
            motor2_position_max_response = self.modbus_client.read_input_registers(15, 1, unit=1)
            if not motor2_position_max_response.isError():
                raw_motor2_position_max_value = motor2_position_max_response.registers[0]
                motor2_position_max = raw_motor2_position_max_value / 10
                self.motor2_position_max_label.config(text=f"Motor 2 Position Max: {motor2_position_max} mm")
            else:
                self.motor2_position_max_label.config(text=f"Error reading Motor 2 Position Max: {motor2_position_max_response}")

            time.sleep(time_between_frame)
            motor2_position_min_response = self.modbus_client.read_input_registers(16, 1, unit=1)
            if not motor2_position_min_response.isError():
                raw_motor2_position_min_value = motor2_position_min_response.registers[0]
                motor2_position_min = raw_motor2_position_min_value / 10
                self.motor2_position_min_label.config(text=f"Motor 2 Position Min: {motor2_position_min} mm")
            else:
                self.motor2_position_min_label.config(text=f"Error reading Motor 2 Position Min: {motor2_position_min_response}")

            time.sleep(time_between_frame)
            network_frequency_response = self.modbus_client.read_input_registers(20, 1, unit=1)
            if not network_frequency_response.isError():
                raw_network_frequency_value = network_frequency_response.registers[0]
                network_frequency = raw_network_frequency_value / 10
                self.network_frequency_label.config(text=f"Network Frequency: {network_frequency} Hz")
            else:
                self.network_frequency_label.config(text=f"Error reading Network Frequency: {network_frequency_response}")

            time.sleep(time_between_frame)
            apparent_power_response = self.modbus_client.read_input_registers(21, 1, unit=1)
            if not apparent_power_response.isError():
                raw_apparent_power_value = apparent_power_response.registers[0]
                apparent_power = raw_apparent_power_value / 10
                self.apparent_power_label.config(text=f"Apparent Power: {apparent_power} VA")
            else:
                self.apparent_power_label.config(text=f"Error reading Apparent Power: {apparent_power_response}")

            time.sleep(time_between_frame)
            active_power_response = self.modbus_client.read_input_registers(22, 1, unit=1)
            if not active_power_response.isError():
                raw_active_power_value = active_power_response.registers[0]
                active_power = raw_active_power_value / 10
                self.active_power_label.config(text=f"Active Power: {active_power} W")
            else:
                self.active_power_label.config(text=f"Error reading Active Power: {active_power_response}")

            time.sleep(time_between_frame)
            dc_resistance_motor1_response = self.modbus_client.read_input_registers(26, 1, unit=1)
            if not dc_resistance_motor1_response.isError():
                raw_dc_resistance_motor1_value = dc_resistance_motor1_response.registers[0]
                dc_resistance_motor1 = raw_dc_resistance_motor1_value / 100
                self.dc_resistance_motor1_label.config(text=f"DC Resistance Motor 1: {dc_resistance_motor1} mOhm")
            else:
                self.dc_resistance_motor1_label.config(text=f"Error reading DC Resistance Motor 1: {dc_resistance_motor1_response}")

            time.sleep(time_between_frame)
            dc_resistance_motor2_response = self.modbus_client.read_input_registers(27, 1, unit=1)
            if not dc_resistance_motor2_response.isError():
                raw_dc_resistance_motor2_value = dc_resistance_motor2_response.registers[0]
                dc_resistance_motor2 = raw_dc_resistance_motor2_value / 100
                self.dc_resistance_motor2_label.config(text=f"DC Resistance Motor 2: {dc_resistance_motor2} mOhm")
            else:
                self.dc_resistance_motor2_label.config(text=f"Error reading DC Resistance Motor 2: {dc_resistance_motor2_response}")

            time.sleep(time_between_frame)
            sweep_resonance_frequency_response = self.modbus_client.read_input_registers(28, 1, unit=1)
            if not sweep_resonance_frequency_response.isError():
                raw_sweep_resonance_frequency_value = sweep_resonance_frequency_response.registers[0]
                sweep_resonance_frequency = raw_sweep_resonance_frequency_value / 10
                self.sweep_resonance_frequency_label.config(text=f"Sweep Resonance Frequency: {sweep_resonance_frequency} Hz")
            else:
                self.sweep_resonance_frequency_label.config(text=f"Error reading Sweep Resonance Frequency: {sweep_resonance_frequency_response}")

        except ModbusException as e:
            self.status_label.config(text=f"Modbus Exception: {e}")
        except Exception as e:
            self.status_label.config(text=f"Failed to read input registers: {e}")

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
                self.initial_frequency_label.config(text=f"Initial Frequency: {initial_frequency} Hz")
            else:
                self.initial_frequency_label.config(text=f"Error reading Initial Frequency: {initial_frequency_response}")

            if not max_dc_voltage_response.isError():
                raw_max_dc_voltage_value = max_dc_voltage_response.registers[0]
                max_dc_voltage = raw_max_dc_voltage_value / 10
                self.max_dc_voltage_label.config(text=f"Max DC Bus Voltage: {max_dc_voltage} V")
            else:
                self.max_dc_voltage_label.config(text=f"Error reading Max DC Bus Voltage: {max_dc_voltage_response}")

            if not min_dc_voltage_response.isError():
                raw_min_dc_voltage_value = min_dc_voltage_response.registers[0]
                min_dc_voltage = raw_min_dc_voltage_value / 10
                self.min_dc_voltage_label.config(text=f"Min DC Bus Voltage: {min_dc_voltage} V")
            else:
                self.min_dc_voltage_label.config(text=f"Error reading Min DC Bus Voltage: {min_dc_voltage_response}")

            if not max_ac_voltage_motor1_response.isError():
                raw_max_ac_voltage_motor1_value = max_ac_voltage_motor1_response.registers[0]
                max_ac_voltage_motor1 = raw_max_ac_voltage_motor1_value / 10
                self.max_ac_voltage_motor1_label.config(text=f"Max AC Voltage Motor 1: {max_ac_voltage_motor1} V")
            else:
                self.max_ac_voltage_motor1_label.config(text=f"Error reading Max AC Voltage Motor 1: {max_ac_voltage_motor1_response}")

            if not max_ac_voltage_motor2_response.isError():
                raw_max_ac_voltage_motor2_value = max_ac_voltage_motor2_response.registers[0]
                max_ac_voltage_motor2 = raw_max_ac_voltage_motor2_value / 10
                self.max_ac_voltage_motor2_label.config(text=f"Max AC Voltage Motor 2: {max_ac_voltage_motor2} V")
            else:
                self.max_ac_voltage_motor2_label.config(text=f"Error reading Max AC Voltage Motor 2: {max_ac_voltage_motor2_response}")

            if not ac_current_motor1_response.isError():
                raw_ac_current_motor1_value = ac_current_motor1_response.registers[0]
                ac_current_motor1 = raw_ac_current_motor1_value / 10
                self.ac_current_motor1_label.config(text=f"AC Current Motor 1: {ac_current_motor1} A")
            else:
                self.ac_current_motor1_label.config(text=f"Error reading AC Current Motor 1: {ac_current_motor1_response}")

            if not ac_current_motor2_response.isError():
                raw_ac_current_motor2_value = ac_current_motor2_response.registers[0]
                ac_current_motor2 = raw_ac_current_motor2_value / 10
                self.ac_current_motor2_label.config(text=f"AC Current Motor 2: {ac_current_motor2} A")
            else:
                self.ac_current_motor2_label.config(text=f"Error reading AC Current Motor 2: {ac_current_motor2_response}")

            if not max_mcu_temperature_response.isError():
                raw_max_mcu_temperature_value = max_mcu_temperature_response.registers[0]
                max_mcu_temperature = raw_max_mcu_temperature_value / 10
                self.max_mcu_temperature_label.config(text=f"Max MCU Temperature: {max_mcu_temperature} °C")
            else:
                self.max_mcu_temperature_label.config(text=f"Error reading Max MCU Temperature: {max_mcu_temperature_response}")

            if not max_radiator_temperature_response.isError():
                raw_max_radiator_temperature_value = max_radiator_temperature_response.registers[0]
                max_radiator_temperature = raw_max_radiator_temperature_value / 10
                self.max_radiator_temperature_label.config(text=f"Max Radiator Temperature: {max_radiator_temperature} °C")
            else:
                self.max_radiator_temperature_label.config(text=f"Error reading Max Radiator Temperature: {max_radiator_temperature_response}")

            if not sweep_min_frequency_response.isError():
                raw_sweep_min_frequency_value = sweep_min_frequency_response.registers[0]
                sweep_min_frequency = raw_sweep_min_frequency_value / 10
                self.sweep_min_frequency_label.config(text=f"Sweep Min Frequency: {sweep_min_frequency} Hz")
            else:
                self.sweep_min_frequency_label.config(text=f"Error reading Sweep Min Frequency: {sweep_min_frequency_response}")

            if not sweep_max_frequency_response.isError():
                raw_sweep_max_frequency_value = sweep_max_frequency_response.registers[0]
                sweep_max_frequency = raw_sweep_max_frequency_value / 10
                self.sweep_max_frequency_label.config(text=f"Sweep Max Frequency: {sweep_max_frequency} Hz")
            else:
                self.sweep_max_frequency_label.config(text=f"Error reading Sweep Max Frequency: {sweep_max_frequency_response}")

            if not sweep_stabilization_response.isError():
                raw_sweep_stabilization_value = sweep_stabilization_response.registers[0]
                sweep_stabilization = raw_sweep_stabilization_value / 10
                self.sweep_stabilization_label.config(text=f"Sweep Stabilization: {sweep_stabilization} ms")
            else:
                self.sweep_stabilization_label.config(text=f"Error reading Sweep Stabilization: {sweep_stabilization_response}")

        except ModbusException as e:
            self.status_label.config(text=f"Modbus Exception: {e}")
        except Exception as e:
            self.status_label.config(text=f"Failed to read holding registers: {e}")

    def create_input_registers(self):
        self.dc_voltage_label = tk.Label(self.input_registers_frame, text="DC Voltage: N/A")
        self.dc_voltage_label.pack(anchor='w')

        self.radiator_temp_label = tk.Label(self.input_registers_frame, text="Radiator Temperature: N/A")
        self.radiator_temp_label.pack(anchor='w')

        self.live_frequency_motor1_label = tk.Label(self.input_registers_frame, text="Live Frequency Motor 1: N/A")
        self.live_frequency_motor1_label.pack(anchor='w')

        self.live_frequency_motor2_label = tk.Label(self.input_registers_frame, text="Live Frequency Motor 2: N/A")
        self.live_frequency_motor2_label.pack(anchor='w')

        self.dc_bus_voltage_label = tk.Label(self.input_registers_frame, text="DC Bus Voltage: N/A")
        self.dc_bus_voltage_label.pack(anchor='w')

        self.ac_voltage_motor1_label = tk.Label(self.input_registers_frame, text="AC Voltage Motor 1: N/A")
        self.ac_voltage_motor1_label.pack(anchor='w')

        self.ac_voltage_motor2_label = tk.Label(self.input_registers_frame, text="AC Voltage Motor 2: N/A")
        self.ac_voltage_motor2_label.pack(anchor='w')

        self.ac_current_motor1_label = tk.Label(self.input_registers_frame, text="AC Current Motor 1: N/A")
        self.ac_current_motor1_label.pack(anchor='w')

        self.ac_current_motor2_label = tk.Label(self.input_registers_frame, text="AC Current Motor 2: N/A")
        self.ac_current_motor2_label.pack(anchor='w')

        self.mcu_temperature_label = tk.Label(self.input_registers_frame, text="MCU Temperature: N/A")
        self.mcu_temperature_label.pack(anchor='w')

        self.mcu_temperature_min_label = tk.Label(self.input_registers_frame, text="MCU Temperature Min (life): N/A")
        self.mcu_temperature_min_label.pack(anchor='w')

        self.mcu_temperature_max_label = tk.Label(self.input_registers_frame, text="MCU Temperature Max (life): N/A")
        self.mcu_temperature_max_label.pack(anchor='w')

        self.radiator_temperature_min_label = tk.Label(self.input_registers_frame, text="Radiator Temperature Min (life): N/A")
        self.radiator_temperature_min_label.pack(anchor='w')

        self.radiator_temperature_max_label = tk.Label(self.input_registers_frame, text="Radiator Temperature Max (life): N/A")
        self.radiator_temperature_max_label.pack(anchor='w')

        self.motor1_position_average_label = tk.Label(self.input_registers_frame, text="Motor 1 Position Average: N/A")
        self.motor1_position_average_label.pack(anchor='w')

        self.motor1_position_max_label = tk.Label(self.input_registers_frame, text="Motor 1 Position Max: N/A")
        self.motor1_position_max_label.pack(anchor='w')

        self.motor1_position_min_label = tk.Label(self.input_registers_frame, text="Motor 1 Position Min: N/A")
        self.motor1_position_min_label.pack(anchor='w')

        self.motor2_position_average_label = tk.Label(self.input_registers_frame, text="Motor 2 Position Average: N/A")
        self.motor2_position_average_label.pack(anchor='w')

        self.motor2_position_max_label = tk.Label(self.input_registers_frame, text="Motor 2 Position Max: N/A")
        self.motor2_position_max_label.pack(anchor='w')

        self.motor2_position_min_label = tk.Label(self.input_registers_frame, text="Motor 2 Position Min: N/A")
        self.motor2_position_min_label.pack(anchor='w')

        self.network_frequency_label = tk.Label(self.input_registers_frame, text="Network Frequency: N/A")
        self.network_frequency_label.pack(anchor='w')

        self.apparent_power_label = tk.Label(self.input_registers_frame, text="Apparent Power: N/A")
        self.apparent_power_label.pack(anchor='w')

        self.active_power_label = tk.Label(self.input_registers_frame, text="Active Power: N/A")
        self.active_power_label.pack(anchor='w')

        self.dc_resistance_motor1_label = tk.Label(self.input_registers_frame, text="DC Resistance Motor 1: N/A")
        self.dc_resistance_motor1_label.pack(anchor='w')

        self.dc_resistance_motor2_label = tk.Label(self.input_registers_frame, text="DC Resistance Motor 2: N/A")
        self.dc_resistance_motor2_label.pack(anchor='w')

        self.sweep_resonance_frequency_label = tk.Label(self.input_registers_frame, text="Sweep Resonance Frequency: N/A")
        self.sweep_resonance_frequency_label.pack(anchor='w')

    def create_holding_registers(self):
        self.initial_frequency_label = tk.Label(self.holding_registers_frame, text="Initial Frequency (1000): N/A")
        self.initial_frequency_label.pack(anchor='w')

        self.initial_frequency_entry = tk.Entry(self.holding_registers_frame)
        self.initial_frequency_entry.pack(anchor='w')
        self.initial_frequency_entry.bind('<Return>', self.on_enter_pressed_initial_frequency)

        self.max_dc_voltage_label = tk.Label(self.holding_registers_frame, text="Max DC Bus Voltage (1001): N/A")
        self.max_dc_voltage_label.pack(anchor='w')

        self.max_dc_voltage_entry = tk.Entry(self.holding_registers_frame)
        self.max_dc_voltage_entry.pack(anchor='w')
        self.max_dc_voltage_entry.bind('<Return>', self.on_enter_pressed_max_dc_voltage)

        self.min_dc_voltage_label = tk.Label(self.holding_registers_frame, text="Min DC Bus Voltage (1002): N/A")
        self.min_dc_voltage_label.pack(anchor='w')

        self.min_dc_voltage_entry = tk.Entry(self.holding_registers_frame)
        self.min_dc_voltage_entry.pack(anchor='w')
        self.min_dc_voltage_entry.bind('<Return>', self.on_enter_pressed_min_dc_voltage)

        self.max_ac_voltage_motor1_label = tk.Label(self.holding_registers_frame, text="Max AC Voltage Motor 1 (1003): N/A")
        self.max_ac_voltage_motor1_label.pack(anchor='w')

        self.max_ac_voltage_motor1_entry = tk.Entry(self.holding_registers_frame)
        self.max_ac_voltage_motor1_entry.pack(anchor='w')
        self.max_ac_voltage_motor1_entry.bind('<Return>', self.on_enter_pressed_max_ac_voltage_motor1)

        self.max_ac_voltage_motor2_label = tk.Label(self.holding_registers_frame, text="Max AC Voltage Motor 2 (1004): N/A")
        self.max_ac_voltage_motor2_label.pack(anchor='w')

        self.max_ac_voltage_motor2_entry = tk.Entry(self.holding_registers_frame)
        self.max_ac_voltage_motor2_entry.pack(anchor='w')
        self.max_ac_voltage_motor2_entry.bind('<Return>', self.on_enter_pressed_max_ac_voltage_motor2)

        self.ac_current_motor1_label = tk.Label(self.holding_registers_frame, text="AC Current Motor 1 (1005): N/A")
        self.ac_current_motor1_label.pack(anchor='w')

        self.ac_current_motor1_entry = tk.Entry(self.holding_registers_frame)
        self.ac_current_motor1_entry.pack(anchor='w')
        self.ac_current_motor1_entry.bind('<Return>', self.on_enter_pressed_ac_current_motor1)

        self.ac_current_motor2_label = tk.Label(self.holding_registers_frame, text="AC Current Motor 2 (1006): N/A")
        self.ac_current_motor2_label.pack(anchor='w')

        self.ac_current_motor2_entry = tk.Entry(self.holding_registers_frame)
        self.ac_current_motor2_entry.pack(anchor='w')
        self.ac_current_motor2_entry.bind('<Return>', self.on_enter_pressed_ac_current_motor2)

        self.max_mcu_temperature_label = tk.Label(self.holding_registers_frame, text="Max MCU Temperature (1007): N/A")
        self.max_mcu_temperature_label.pack(anchor='w')

        self.max_mcu_temperature_entry = tk.Entry(self.holding_registers_frame)
        self.max_mcu_temperature_entry.pack(anchor='w')
        self.max_mcu_temperature_entry.bind('<Return>', self.on_enter_pressed_max_mcu_temperature)

        self.max_radiator_temperature_label = tk.Label(self.holding_registers_frame, text="Max Radiator Temperature (1008): N/A")
        self.max_radiator_temperature_label.pack(anchor='w')

        self.max_radiator_temperature_entry = tk.Entry(self.holding_registers_frame)
        self.max_radiator_temperature_entry.pack(anchor='w')
        self.max_radiator_temperature_entry.bind('<Return>', self.on_enter_pressed_max_radiator_temperature)

        self.sweep_min_frequency_label = tk.Label(self.holding_registers_frame, text="Sweep Min Frequency (1009): N/A")
        self.sweep_min_frequency_label.pack(anchor='w')

        self.sweep_min_frequency_entry = tk.Entry(self.holding_registers_frame)
        self.sweep_min_frequency_entry.pack(anchor='w')
        self.sweep_min_frequency_entry.bind('<Return>', self.on_enter_pressed_sweep_min_frequency)

        self.sweep_max_frequency_label = tk.Label(self.holding_registers_frame, text="Sweep Max Frequency (1010): N/A")
        self.sweep_max_frequency_label.pack(anchor='w')

        self.sweep_max_frequency_entry = tk.Entry(self.holding_registers_frame)
        self.sweep_max_frequency_entry.pack(anchor='w')
        self.sweep_max_frequency_entry.bind('<Return>', self.on_enter_pressed_sweep_max_frequency)

        self.sweep_stabilization_label = tk.Label(self.holding_registers_frame, text="Sweep Stabilization (1011): N/A")
        self.sweep_stabilization_label.pack(anchor='w')

        self.sweep_stabilization_entry = tk.Entry(self.holding_registers_frame)
        self.sweep_stabilization_entry.pack(anchor='w')
        self.sweep_stabilization_entry.bind('<Return>', self.on_enter_pressed_sweep_stabilization)

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

    def write_max_dc_voltage(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_dc_voltage_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1001, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"Max DC Bus Voltage (1001) written successfully")
                else:
                    self.status_label.config(text=f"Error writing Max DC Bus Voltage: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Max DC Bus Voltage: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_min_dc_voltage(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.min_dc_voltage_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1002, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"Min DC Bus Voltage (1002) written successfully")
                else:
                    self.status_label.config(text=f"Error writing Min DC Bus Voltage: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Min DC Bus Voltage: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_max_ac_voltage_motor1(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_ac_voltage_motor1_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1003, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"Max AC Voltage Motor 1 (1003) written successfully")
                else:
                    self.status_label.config(text=f"Error writing Max AC Voltage Motor 1: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Max AC Voltage Motor 1: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_max_ac_voltage_motor2(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_ac_voltage_motor2_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1004, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"Max AC Voltage Motor 2 (1004) written successfully")
                else:
                    self.status_label.config(text=f"Error writing Max AC Voltage Motor 2: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Max AC Voltage Motor 2: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_ac_current_motor1(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.ac_current_motor1_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1005, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"AC Current Motor 1 (1005) written successfully")
                else:
                    self.status_label.config(text=f"Error writing AC Current Motor 1: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write AC Current Motor 1: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_ac_current_motor2(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.ac_current_motor2_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1006, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"AC Current Motor 2 (1006) written successfully")
                else:
                    self.status_label.config(text=f"Error writing AC Current Motor 2: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write AC Current Motor 2: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_max_mcu_temperature(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_mcu_temperature_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1007, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"Max MCU Temperature (1007) written successfully")
                else:
                    self.status_label.config(text=f"Error writing Max MCU Temperature: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Max MCU Temperature: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_max_radiator_temperature(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.max_radiator_temperature_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1008, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"Max Radiator Temperature (1008) written successfully")
                else:
                    self.status_label.config(text=f"Error writing Max Radiator Temperature: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Max Radiator Temperature: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_sweep_min_frequency(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.sweep_min_frequency_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1009, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"Sweep Min Frequency (1009) written successfully")
                else:
                    self.status_label.config(text=f"Error writing Sweep Min Frequency: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Sweep Min Frequency: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_sweep_max_frequency(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.sweep_max_frequency_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1010, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"Sweep Max Frequency (1010) written successfully")
                else:
                    self.status_label.config(text=f"Error writing Sweep Max Frequency: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Sweep Max Frequency: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

    def write_sweep_stabilization(self):
        if self.modbus_client and self.modbus_client.is_socket_open():
            try:
                value = float(self.sweep_stabilization_entry.get())
                value_to_write = int(value * 10)
                time.sleep(time_between_frame)
                response = self.modbus_client.write_register(1011, value_to_write, unit=1)
                if not response.isError():
                    self.status_label.config(text=f"Sweep Stabilization (1011) written successfully")
                else:
                    self.status_label.config(text=f"Error writing Sweep Stabilization: {response}")
            except ValueError:
                self.status_label.config(text="Invalid value. Please enter a number.")
            except ModbusException as e:
                self.status_label.config(text=f"Modbus Exception: {e}")
            except Exception as e:
                self.status_label.config(text=f"Failed to write Sweep Stabilization: {e}")
        else:
            self.status_label.config(text="Not connected to any port")

if __name__ == "__main__":
    root = tk.Tk()
    app = COMConnectorApp(root)
    root.mainloop()
