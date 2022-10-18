from datetime import datetime
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import * 
import sys
from data_handler import DataHandler

from main_window import MainWindow

class Program(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        DataHandler.import_data_from_csv("data/20200118/310/summary.csv")

        self.window = MainWindow()
        self.window.show()
        self.exec()

if __name__ == "__main__":
    Program()

