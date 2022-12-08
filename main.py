from PyQt6.QtWidgets import QApplication
import sys

from main_window import MainWindow

class Program(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        self.window = MainWindow()
        self.window.show()
        self.exec()

if __name__ == "__main__":
    Program()