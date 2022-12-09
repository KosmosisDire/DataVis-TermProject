from PyQt6.QtWidgets import QMainWindow
from data_handler import DataHandler


class ImportWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import Data")
        self.setMinimumSize(500, 667)
        self.resize(500, 667)

        self.csv_path: str = None
        self.data_handler: DataHandler = None

        self.create_UI()
    
    def create_UI(self):
        pass