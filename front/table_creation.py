from PySide6 import QtWidgets, QtCore, QtGui


def set_centered_item(table: QtWidgets.QTableWidget, row: int, col: int, text: str) -> None:
        """Helper function to set a centered item in the table."""
        item = QtWidgets.QTableWidgetItem(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(8)
        item.setFont(font)
        table.setItem(row, col, item)


def create_temp_table(table: QtWidgets.QTableWidget) -> None:
    """Create the table for the temperature"""
    # Merge header labels
    table.setSpan(0, 0, 1, 3)
    table.setSpan(0, 3, 1, 3)
    # Set headers
    set_centered_item(table, 0, 0, QtWidgets.QTableWidgetItem("Radiator Temperature [°C]"))
    set_centered_item(table, 0, 3, QtWidgets.QTableWidgetItem("MCU Temperature [°C]"))
    # Set second row labels (Min, Live, Max)
    headers = ["min", "live", "max", "min", "live", "max"]
    for col in range(6):
        set_centered_item(table, 1, col, QtWidgets.QTableWidgetItem(headers[col]))
    # Disable editing for the first three rows
    for row in range(3):
        for col in range(6):
            item = table.item(row, col)
            if item:
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)


def create_motor_table(table: QtWidgets.QTableWidget) -> None:
    """Create the table for the temperature"""
    # Merge header labels
    table.setSpan(0, 0, 2, 1)
    table.setSpan(0, 1, 1, 3)
    table.setSpan(0, 1, 1, 3)
    table.setSpan(0, 4, 1, 2)
    table.setSpan(0, 6, 1, 3)
    # Set headers
    set_centered_item(table, 0, 0, QtWidgets.QTableWidgetItem("Live freq. [Hz]"))
    set_centered_item(table, 0, 1, QtWidgets.QTableWidgetItem("Position [mm]"))
    set_centered_item(table, 0, 4, QtWidgets.QTableWidgetItem("AC rms"))
    set_centered_item(table, 0, 6, QtWidgets.QTableWidgetItem("DC"))
    # Set second row labels (Min, Live, Max)
    headers = ["min", "avg.", "max", "voltage [V]", "current [A]", "resistance [Ω]", "current [A]", "position [mm]"]
    for col in range(1, len(headers)+1):
        set_centered_item(table, 1, col, QtWidgets.QTableWidgetItem(headers[col-1]))
    # Disable editing for the first three rows
    for row in range(3):
        for col in range(7):
            item = table.item(row, col)
            if item:
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)


def create_pow_table(table: QtWidgets.QTableWidget) -> None:
    """Create the table for the temperature"""
    table.setSpan(0, 0, 2, 1)
    table.setSpan(0, 1, 2, 1)
    headers = ["Apparent [VA]", "Active [W]"]
    for col in range(2):
        set_centered_item(table, 0, col, QtWidgets.QTableWidgetItem(headers[col]))
    # Disable editing for the first three rows
    for row in range(3):
        for col in range(2):
            item = table.item(row, col)
            if item:
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)


def create_other_table(table: QtWidgets.QTableWidget) -> None:
    """Create the table for the temperature"""
    table.setSpan(0, 0, 2, 1)
    table.setSpan(0, 1, 1, 2)
    set_centered_item(table, 0, 0, QtWidgets.QTableWidgetItem("DC Bus voltage [V]"))
    set_centered_item(table, 0, 1, QtWidgets.QTableWidgetItem("Frequency [Hz]"))
    headers = ["network", "sweep resonance"]
    for col in range(1, 3):
        set_centered_item(table, 1, col, QtWidgets.QTableWidgetItem(headers[col-1]))
    # Disable editing for the first three rows
    for row in range(3):
        for col in range(6):
            item = table.item(row, col)
            if item:
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)


def create_holding_1(table: QtWidgets.QTableWidget) -> None:
    """Create the table for the temperature"""
    # Merge header labels
    table.setSpan(0, 0, 1, 4)
    table.setSpan(0, 4, 1, 2)
    # Set headers
    set_centered_item(table, 0, 0, QtWidgets.QTableWidgetItem("Voltage [V]"))
    set_centered_item(table, 0, 4, QtWidgets.QTableWidgetItem("Current [A]"))
    # Set second row labels (Min, Live, Max)
    headers = ["max DC bus", "min DC bus", "max AC motor 1", "max AC motor 2", "AC motor 1", "AC motor 2"]
    for col in range(6):
        set_centered_item(table, 1, col, QtWidgets.QTableWidgetItem(headers[col]))
    # Disable editing for the first three rows
    for row in range(3):
        for col in range(6):
            item = table.item(row, col)
            if item:
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)


def create_holding_2(table: QtWidgets.QTableWidget) -> None:
    """Create the table for the temperature"""
    # Merge header labels
    table.setSpan(0, 0, 1, 2)
    table.setSpan(0, 2, 1, 3)
    table.setSpan(0, 5, 2, 1)
    table.setSpan(0, 6, 2, 1)
    # Set headers
    set_centered_item(table, 0, 0, QtWidgets.QTableWidgetItem("Temperature [°C]"))
    set_centered_item(table, 0, 2, QtWidgets.QTableWidgetItem("Frequency [Hz]"))
    set_centered_item(table, 0, 5, QtWidgets.QTableWidgetItem("Sweep stabilisation [ms]"))
    set_centered_item(table, 0, 6, QtWidgets.QTableWidgetItem("Modulation [%]"))
    # Set second row labels (Min, Live, Max)
    headers = ["max MCU", "max radiator", "initial", "sweep min.", "sweep max"]
    for col in range(5):
        set_centered_item(table, 1, col, QtWidgets.QTableWidgetItem(headers[col]))
    # Disable editing for the first three rows
    for row in range(3):
        for col in range(7):
            item = table.item(row, col)
            if item:
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)