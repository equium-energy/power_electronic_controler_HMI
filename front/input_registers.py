import tkinter as tk
import time
from pymodbus.exceptions import ModbusException

time_between_frame = 0.02


class InputRegisters:
    def __init__(self, frame):
        self.frame = frame
        self.create_input_registers()

    def create_input_registers(self):
        self.radiator_temp_label = tk.Label(
            self.frame, text="Radiator Temperature: N/A"
        )
        self.radiator_temp_label.pack(anchor="w")

        self.live_frequency_motor1_label = tk.Label(
            self.frame, text="Live Frequency Motor 1: N/A"
        )
        self.live_frequency_motor1_label.pack(anchor="w")

        self.live_frequency_motor2_label = tk.Label(
            self.frame, text="Live Frequency Motor 2: N/A"
        )
        self.live_frequency_motor2_label.pack(anchor="w")

        self.dc_bus_voltage_label = tk.Label(self.frame, text="DC Bus Voltage: N/A")
        self.dc_bus_voltage_label.pack(anchor="w")

        self.ac_voltage_motor1_label = tk.Label(
            self.frame, text="AC Voltage Motor 1: N/A"
        )
        self.ac_voltage_motor1_label.pack(anchor="w")

        self.ac_voltage_motor2_label = tk.Label(
            self.frame, text="AC Voltage Motor 2: N/A"
        )
        self.ac_voltage_motor2_label.pack(anchor="w")

        self.input_RMS_current_motor1_label = tk.Label(
            self.frame, text="AC Current Motor 1: N/A"
        )
        self.input_RMS_current_motor1_label.pack(anchor="w")

        self.input_RMS_current_motor2_label = tk.Label(
            self.frame, text="AC Current Motor 2: N/A"
        )
        self.input_RMS_current_motor2_label.pack(anchor="w")

        self.mcu_temperature_label = tk.Label(self.frame, text="MCU Temperature: N/A")
        self.mcu_temperature_label.pack(anchor="w")

        self.mcu_temperature_min_label = tk.Label(
            self.frame, text="MCU Temperature Min (live): N/A"
        )
        self.mcu_temperature_min_label.pack(anchor="w")

        self.mcu_temperature_max_label = tk.Label(
            self.frame, text="MCU Temperature Max (live): N/A"
        )
        self.mcu_temperature_max_label.pack(anchor="w")

        self.radiator_temperature_min_label = tk.Label(
            self.frame, text="Radiator Temperature Min (live): N/A"
        )
        self.radiator_temperature_min_label.pack(anchor="w")

        self.radiator_temperature_max_label = tk.Label(
            self.frame, text="Radiator Temperature Max (live): N/A"
        )
        self.radiator_temperature_max_label.pack(anchor="w")

        self.motor1_position_average_label = tk.Label(
            self.frame, text="Motor 1 Position Average: N/A"
        )
        self.motor1_position_average_label.pack(anchor="w")

        self.motor1_position_max_label = tk.Label(
            self.frame, text="Motor 1 Position Max: N/A"
        )
        self.motor1_position_max_label.pack(anchor="w")

        self.motor1_position_min_label = tk.Label(
            self.frame, text="Motor 1 Position Min: N/A"
        )
        self.motor1_position_min_label.pack(anchor="w")

        self.motor2_position_average_label = tk.Label(
            self.frame, text="Motor 2 Position Average: N/A"
        )
        self.motor2_position_average_label.pack(anchor="w")

        self.motor2_position_max_label = tk.Label(
            self.frame, text="Motor 2 Position Max: N/A"
        )
        self.motor2_position_max_label.pack(anchor="w")

        self.motor2_position_min_label = tk.Label(
            self.frame, text="Motor 2 Position Min: N/A"
        )
        self.motor2_position_min_label.pack(anchor="w")

        self.network_frequency_label = tk.Label(
            self.frame, text="Network Frequency: N/A"
        )
        self.network_frequency_label.pack(anchor="w")

        self.apparent_power_label = tk.Label(self.frame, text="Apparent Power: N/A")
        self.apparent_power_label.pack(anchor="w")

        self.active_power_label = tk.Label(self.frame, text="Active Power: N/A")
        self.active_power_label.pack(anchor="w")

        self.dc_resistance_motor1_label = tk.Label(
            self.frame, text="DC Resistance Motor 1: N/A"
        )
        self.dc_resistance_motor1_label.pack(anchor="w")

        self.dc_resistance_motor2_label = tk.Label(
            self.frame, text="DC Resistance Motor 2: N/A"
        )
        self.dc_resistance_motor2_label.pack(anchor="w")

        self.sweep_resonance_frequency_label = tk.Label(
            self.frame, text="Sweep Resonance Frequency: N/A"
        )
        self.sweep_resonance_frequency_label.pack(anchor="w")

    def read_input_registers(self, modbus_client):
        try:
            time.sleep(time_between_frame)
            dc_response = modbus_client.read_input_registers(4, 1, unit=1)
            time.sleep(time_between_frame)
            radiator_response = modbus_client.read_input_registers(10, 1, unit=1)

            if not radiator_response.isError():
                raw_radiator_value = radiator_response.registers[0] / 10
                self.radiator_temp_label.config(
                    text=f"Radiator Temperature: {raw_radiator_value} °C"
                )
            else:
                self.radiator_temp_label.config(
                    text=f"Error reading Radiator Temperature"
                )

            time.sleep(time_between_frame)
            live_frequency_motor1_response = modbus_client.read_input_registers(
                3, 1, unit=1
            )
            if not live_frequency_motor1_response.isError():
                raw_live_frequency_motor1_value = (
                    live_frequency_motor1_response.registers[0]
                )
                live_frequency_motor1 = raw_live_frequency_motor1_value / 10
                self.live_frequency_motor1_label.config(
                    text=f"Live Frequency Motor 1: {live_frequency_motor1} Hz"
                )
            else:
                self.live_frequency_motor1_label.config(
                    text=f"Error reading Live Frequency Motor 1"
                )

            time.sleep(time_between_frame)
            live_frequency_motor2_response = modbus_client.read_input_registers(
                18, 1, unit=1
            )
            if not live_frequency_motor2_response.isError():
                raw_live_frequency_motor2_value = (
                    live_frequency_motor2_response.registers[0]
                )
                live_frequency_motor2 = raw_live_frequency_motor2_value / 10
                self.live_frequency_motor2_label.config(
                    text=f"Live Frequency Motor 2: {live_frequency_motor2} Hz"
                )
            else:
                self.live_frequency_motor2_label.config(
                    text=f"Error reading Live Frequency Motor 2"
                )

            time.sleep(time_between_frame)
            dc_bus_voltage_response = modbus_client.read_input_registers(4, 1, unit=1)
            if not dc_bus_voltage_response.isError():
                raw_dc_bus_voltage_value = dc_bus_voltage_response.registers[0]
                dc_bus_voltage = raw_dc_bus_voltage_value / 10
                self.dc_bus_voltage_label.config(
                    text=f"DC Bus Voltage: {dc_bus_voltage} V"
                )
            else:
                self.dc_bus_voltage_label.config(text=f"Error reading DC Bus Voltage")

            time.sleep(time_between_frame)
            ac_voltage_motor1_response = modbus_client.read_input_registers(
                5, 1, unit=1
            )
            if not ac_voltage_motor1_response.isError():
                raw_ac_voltage_motor1_value = ac_voltage_motor1_response.registers[0]
                ac_voltage_motor1 = raw_ac_voltage_motor1_value / 10
                self.ac_voltage_motor1_label.config(
                    text=f"Voltage Motor 1 RMS: {ac_voltage_motor1} V"
                )
            else:
                self.ac_voltage_motor1_label.config(
                    text=f"Error reading AC Voltage Motor 1"
                )

            time.sleep(time_between_frame)
            ac_voltage_motor2_response = modbus_client.read_input_registers(
                6, 1, unit=1
            )
            if not ac_voltage_motor2_response.isError():
                raw_ac_voltage_motor2_value = ac_voltage_motor2_response.registers[0]
                ac_voltage_motor2 = raw_ac_voltage_motor2_value / 10
                self.ac_voltage_motor2_label.config(
                    text=f"Voltage Motor 2 RMS: {ac_voltage_motor2} V"
                )
            else:
                self.ac_voltage_motor2_label.config(
                    text=f"Error reading AC Voltage Motor 2"
                )

            time.sleep(time_between_frame)
            RMS_current_motor1_response = modbus_client.read_input_registers(
                7, 1, unit=1
            )
            if not RMS_current_motor1_response.isError():
                raw_ac_current_motor1_value = RMS_current_motor1_response.registers[0]
                ac_current_motor1 = raw_ac_current_motor1_value / 10
                self.input_RMS_current_motor1_label.config(
                    text=f"Current Motor 1 RMS: {ac_current_motor1} A"
                )
            else:
                self.input_RMS_current_motor1_label.config(
                    text=f"Error reading AC Current Motor 1"
                )

            time.sleep(time_between_frame)
            RMS_current_motor2_response = modbus_client.read_input_registers(
                8, 1, unit=1
            )
            if not RMS_current_motor2_response.isError():
                raw_ac_current_motor2_value = RMS_current_motor2_response.registers[0]
                ac_current_motor2 = raw_ac_current_motor2_value / 10
                self.input_RMS_current_motor2_label.config(
                    text=f"Current Motor 2 RMS: {ac_current_motor2} A"
                )
            else:
                self.input_RMS_current_motor2_label.config(
                    text=f"Error reading AC Current Motor 2"
                )

            time.sleep(time_between_frame)
            mcu_temperature_response = modbus_client.read_input_registers(9, 1, unit=1)
            if not mcu_temperature_response.isError():
                raw_mcu_temperature_value = mcu_temperature_response.registers[0]
                mcu_temperature = raw_mcu_temperature_value / 10
                self.mcu_temperature_label.config(
                    text=f"MCU Temperature: {mcu_temperature} °C"
                )
            else:
                self.mcu_temperature_label.config(text=f"Error reading MCU Temperature")

            time.sleep(time_between_frame)
            mcu_temperature_min_response = modbus_client.read_input_registers(
                17, 1, unit=1
            )
            if not mcu_temperature_min_response.isError():
                raw_mcu_temperature_min_value = mcu_temperature_min_response.registers[
                    0
                ]
                mcu_temperature_min = raw_mcu_temperature_min_value / 10
                self.mcu_temperature_min_label.config(
                    text=f"MCU Temperature Min (live): {mcu_temperature_min} °C"
                )
            else:
                self.mcu_temperature_min_label.config(
                    text=f"Error reading MCU Temperature Min (live)"
                )

            time.sleep(time_between_frame)
            mcu_temperature_max_response = modbus_client.read_input_registers(
                18, 1, unit=1
            )
            if not mcu_temperature_max_response.isError():
                raw_mcu_temperature_max_value = mcu_temperature_max_response.registers[
                    0
                ]
                mcu_temperature_max = raw_mcu_temperature_max_value / 10
                self.mcu_temperature_max_label.config(
                    text=f"MCU Temperature Max (live): {mcu_temperature_max} °C"
                )
            else:
                self.mcu_temperature_max_label.config(
                    text=f"Error reading MCU Temperature Max (live)"
                )

            time.sleep(time_between_frame)
            radiator_temperature_min_response = modbus_client.read_input_registers(
                19, 1, unit=1
            )
            if not radiator_temperature_min_response.isError():
                raw_radiator_temperature_min_value = (
                    radiator_temperature_min_response.registers[0]
                )
                radiator_temperature_min = raw_radiator_temperature_min_value / 10
                self.radiator_temperature_min_label.config(
                    text=f"Radiator Temperature Min (live): {radiator_temperature_min} °C"
                )
            else:
                self.radiator_temperature_min_label.config(
                    text=f"Error reading Radiator Temperature Min (live)"
                )

            time.sleep(time_between_frame)
            radiator_temperature_max_response = modbus_client.read_input_registers(
                20, 1, unit=1
            )
            if not radiator_temperature_max_response.isError():
                raw_radiator_temperature_max_value = (
                    radiator_temperature_max_response.registers[0]
                )
                radiator_temperature_max = raw_radiator_temperature_max_value / 10
                self.radiator_temperature_max_label.config(
                    text=f"Radiator Temperature Max (live): {radiator_temperature_max} °C"
                )
            else:
                self.radiator_temperature_max_label.config(
                    text=f"Error reading Radiator Temperature Max (live)"
                )

            time.sleep(time_between_frame)
            motor1_position_average_response = modbus_client.read_input_registers(
                11, 1, unit=1
            )
            if not motor1_position_average_response.isError():
                raw_motor1_position_average_value = (
                    motor1_position_average_response.registers[0]
                )
                motor1_position_average = raw_motor1_position_average_value / 10
                self.motor1_position_average_label.config(
                    text=f"Motor 1 Position Average: {motor1_position_average} mm"
                )
            else:
                self.motor1_position_average_label.config(
                    text=f"Error reading Motor 1 Position Average"
                )

            time.sleep(time_between_frame)
            motor1_position_max_response = modbus_client.read_input_registers(
                12, 1, unit=1
            )
            if not motor1_position_max_response.isError():
                raw_motor1_position_max_value = motor1_position_max_response.registers[
                    0
                ]
                motor1_position_max = raw_motor1_position_max_value / 10
                self.motor1_position_max_label.config(
                    text=f"Motor 1 Position Max: {motor1_position_max} mm"
                )
            else:
                self.motor1_position_max_label.config(
                    text=f"Error reading Motor 1 Position Max"
                )

            time.sleep(time_between_frame)
            motor1_position_min_response = modbus_client.read_input_registers(
                13, 1, unit=1
            )
            if not motor1_position_min_response.isError():
                raw_motor1_position_min_value = motor1_position_min_response.registers[
                    0
                ]
                motor1_position_min = raw_motor1_position_min_value / 10
                self.motor1_position_min_label.config(
                    text=f"Motor 1 Position Min: {motor1_position_min} mm"
                )
            else:
                self.motor1_position_min_label.config(
                    text=f"Error reading Motor 1 Position Min"
                )

            time.sleep(time_between_frame)
            motor2_position_average_response = modbus_client.read_input_registers(
                14, 1, unit=1
            )
            if not motor2_position_average_response.isError():
                raw_motor2_position_average_value = (
                    motor2_position_average_response.registers[0]
                )
                motor2_position_average = raw_motor2_position_average_value / 10
                self.motor2_position_average_label.config(
                    text=f"Motor 2 Position Average: {motor2_position_average} mm"
                )
            else:
                self.motor2_position_average_label.config(
                    text=f"Error reading Motor 2 Position Average"
                )

            time.sleep(time_between_frame)
            motor2_position_max_response = modbus_client.read_input_registers(
                15, 1, unit=1
            )
            if not motor2_position_max_response.isError():
                raw_motor2_position_max_value = motor2_position_max_response.registers[
                    0
                ]
                motor2_position_max = raw_motor2_position_max_value / 10
                self.motor2_position_max_label.config(
                    text=f"Motor 2 Position Max: {motor2_position_max} mm"
                )
            else:
                self.motor2_position_max_label.config(
                    text=f"Error reading Motor 2 Position Max"
                )

            time.sleep(time_between_frame)
            motor2_position_min_response = modbus_client.read_input_registers(
                16, 1, unit=1
            )
            if not motor2_position_min_response.isError():
                raw_motor2_position_min_value = motor2_position_min_response.registers[
                    0
                ]
                motor2_position_min = raw_motor2_position_min_value / 10
                self.motor2_position_min_label.config(
                    text=f"Motor 2 Position Min: {motor2_position_min} mm"
                )
            else:
                self.motor2_position_min_label.config(
                    text=f"Error reading Motor 2 Position Min"
                )

            time.sleep(time_between_frame)
            network_frequency_response = modbus_client.read_input_registers(
                20, 1, unit=1
            )
            if not network_frequency_response.isError():
                raw_network_frequency_value = network_frequency_response.registers[0]
                network_frequency = raw_network_frequency_value / 10
                self.network_frequency_label.config(
                    text=f"Network Frequency: {network_frequency} Hz"
                )
            else:
                self.network_frequency_label.config(
                    text=f"Error reading Network Frequency"
                )

            time.sleep(time_between_frame)
            apparent_power_response = modbus_client.read_input_registers(21, 1, unit=1)
            if not apparent_power_response.isError():
                raw_apparent_power_value = apparent_power_response.registers[0]
                apparent_power = raw_apparent_power_value / 10
                self.apparent_power_label.config(
                    text=f"Apparent Power: {apparent_power} VA"
                )
            else:
                self.apparent_power_label.config(text=f"Error reading Apparent Power")

            time.sleep(time_between_frame)
            active_power_response = modbus_client.read_input_registers(22, 1, unit=1)
            if not active_power_response.isError():
                raw_active_power_value = active_power_response.registers[0]
                active_power = raw_active_power_value / 10
                self.active_power_label.config(text=f"Active Power: {active_power} W")
            else:
                self.active_power_label.config(text=f"Error reading Active Power")

            time.sleep(time_between_frame)
            dc_resistance_motor1_response = modbus_client.read_input_registers(
                26, 1, unit=1
            )
            if not dc_resistance_motor1_response.isError():
                raw_dc_resistance_motor1_value = (
                    dc_resistance_motor1_response.registers[0]
                )
                dc_resistance_motor1 = raw_dc_resistance_motor1_value / 100
                self.dc_resistance_motor1_label.config(
                    text=f"DC Resistance Motor 1: {dc_resistance_motor1} mOhm"
                )
            else:
                self.dc_resistance_motor1_label.config(
                    text=f"Error reading DC Resistance Motor 1"
                )

            time.sleep(time_between_frame)
            dc_resistance_motor2_response = modbus_client.read_input_registers(
                27, 1, unit=1
            )
            if not dc_resistance_motor2_response.isError():
                raw_dc_resistance_motor2_value = (
                    dc_resistance_motor2_response.registers[0]
                )
                dc_resistance_motor2 = raw_dc_resistance_motor2_value / 100
                self.dc_resistance_motor2_label.config(
                    text=f"DC Resistance Motor 2: {dc_resistance_motor2} mOhm"
                )
            else:
                self.dc_resistance_motor2_label.config(
                    text=f"Error reading DC Resistance Motor 2"
                )

            time.sleep(time_between_frame)
            sweep_resonance_frequency_response = modbus_client.read_input_registers(
                28, 1, unit=1
            )
            if not sweep_resonance_frequency_response.isError():
                raw_sweep_resonance_frequency_value = (
                    sweep_resonance_frequency_response.registers[0]
                )
                sweep_resonance_frequency = raw_sweep_resonance_frequency_value / 10
                self.sweep_resonance_frequency_label.config(
                    text=f"Sweep Resonance Frequency: {sweep_resonance_frequency} Hz"
                )
            else:
                self.sweep_resonance_frequency_label.config(
                    text=f"Error reading Sweep Resonance Frequency"
                )

            time.sleep(time_between_frame)
            motor_status_response = modbus_client.read_input_registers(0, 1, unit=1)
            if not motor_status_response.isError():
                motor_status_value = motor_status_response.registers[0]
                motor_status_text = self.convert_motor_status(motor_status_value)
                self.motor_status_label.config(
                    text=f"Motor Status: {motor_status_text}"
                )
            else:
                self.motor_status_label.config(text=f"Error reading Motor Status")

        except ModbusException as e:
            self.status_label.config(text=f"Modbus Exception: {e}")
        except Exception as e:
            self.status_label.config(text=f"Failed to read input registers: {e}")

    def convert_motor_status(self, status_code):
        status_mapping = {
            0: "null",
            1: "idle",
            2: "starting",
            3: "execute",
            4: "holding",
            5: "held",
            6: "unholding",
            7: "suspending",
            8: "suspended",
            9: "unsuspended",
            10: "aborting",
            11: "aborted",
            12: "clearing",
            13: "stopping",
            14: "stopped",
            15: "resetting",
            16: "completing",
            17: "complete",
        }
        return status_mapping.get(status_code, "Unknown Status")
