from PyQt6.QtWidgets import QApplication
import sys
import os 


from main_window import MainWindow

class Program(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        try:
            os.chdir(sys._MEIPASS)
        except:
            pass

        self.window = MainWindow()
        self.window.show()
        self.exec()

        


if __name__ == "__main__":
    Program()