import sys
from PySide6.QtWidgets import QApplication
from front.main_window import MainWindow  # Import your main window class


def main():
    app = QApplication(sys.argv)  # Create the application
    window = MainWindow()  # Initialize the main window
    window.main_window.show()  # Show the main window
    sys.exit(app.exec())  # Execute the event loop


if __name__ == "__main__":
    main()  # Run the application
