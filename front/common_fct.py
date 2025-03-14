from PySide6 import QtWidgets

import serial.tools.list_ports


def refresh_ports(element: QtWidgets.QComboBox) -> None:
    """Refresh the port"""
    ports = [port.device for port in serial.tools.list_ports.comports()]
    element.clear()  # Clear previous values
    element.addItems(ports)  # Add new values
    # Set the first item as the default selection if there are available ports
    if ports:
        element.setCurrentIndex(0)
