from collections.abc import Sequence
from datetime import datetime
from time import sleep, time
from typing import Any, Callable

from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
                             QDateTimeEdit, QDial, QDoubleSpinBox,
                             QFontComboBox, QHBoxLayout, QLabel, QLCDNumber,
                             QLineEdit, QMainWindow, QProgressBar, QPushButton,
                             QRadioButton, QSlider, QSpinBox, QTimeEdit,
                             QVBoxLayout, QWidget, QScrollArea)
from global_settings import GlobalSettings

from styles import Styles
from data_handler import DataHandler
from widgets.blank_widget import BlankWidget
from widgets.colored_text import ColoredText
from widgets.horizontal_group import HorizonalGroup
from widgets.labeled_control import LabeledWidget
from widgets.seperator import HorizontalSeperator
from widgets.sidebar_widget import Sidebar
from widgets.themed_button import ThemedButton
from widgets.themed_dropdown import ThemedDropdown
from widgets.themed_radiobutton import ThemedRadioButton
from widgets.themed_scroll_area import ThemedScrollArea
from widgets.time_range_picker import TimeRangePicker
from widgets.themed_plot import ThemedPlot


class ProjectWindow(QMainWindow):
    def __init__(self):
         super().__init__()
         self.resizeCallacks: list[Callable[[QResizeEvent]], Any] = []

    def resizeEvent(self, event: QResizeEvent):
        for callback in self.resizeCallacks:
            callback(event)
        QMainWindow.resizeEvent(self, event)

    def register_resize_callback(self, callback: Callable[[QResizeEvent], Any]):
        self.resizeCallacks.append(callback)


class MainWindow(ProjectWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Data Visualizer")
        self.setMinimumSize(int(1920/2), int(1080/2))
        self.resize(1280, 720)

        background = BlankWidget(Styles.theme.light_background_color)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = Sidebar()
        self.populate_sidebar(sidebar)
        layout.addWidget(sidebar)

        right_area = BlankWidget()
        right_area.setLayout(QVBoxLayout())
        layout.addWidget(right_area)

        graph_header = BlankWidget(Styles.theme.mid_background_color_hex)
        graph_header.setLayout(QVBoxLayout())
        right_area.addWidget(graph_header)

        time_range = DataHandler.get_time_range()
        print(time_range)
        time_picker = TimeRangePicker(75, datetime.fromtimestamp(time_range[0]), datetime.fromtimestamp(time_range[1]), GlobalSettings.time_range_changed_callback)
        time_picker.set_plot_data(DataHandler.get_all("Temp avg"))
        graph_header.layout().addWidget(time_picker)

        scroll_area = ThemedScrollArea()
        scroll_area.setLayout(QVBoxLayout(), Styles.theme.close_spacing, (Styles.theme.close_spacing, Styles.theme.close_spacing, Styles.theme.close_spacing, Styles.theme.close_spacing))
        right_area.addWidget(scroll_area)

        graph1 = ThemedPlot("Temperature", "Temp avg")

        scroll_area.addWidget(graph1)

        background.setLayout(layout)
        self.setCentralWidget(background)
        self.register_resize_callback(sidebar.on_resize)

    def populate_sidebar(self, sidebar: Sidebar):

        #File heading
        sidebar.setLayout(QVBoxLayout())
        sidebar.getLayout().setSpacing(Styles.theme.close_spacing)

        sidebar.addWidget(ColoredText("File: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        file_widgets = [ThemedButton("Import Data", DataHandler.open_import_window), ThemedButton("Clear Data", DataHandler.clear_table)]
        sidebar.addWidget(HorizonalGroup(file_widgets, Styles.theme.medium_spacing))
        
        sidebar.addWidget(HorizontalSeperator(Styles.theme.medium_spacing))

        # View heading
        sidebar.addWidget(ColoredText("View: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        interval_dropdown = ThemedDropdown(["30 Seconds", "1 Minute", "5 Minutes", "30 Minutes", "1 Hour", "6 Hours", "12 Hours", "1 Day"], GlobalSettings.aggregation_changed_callback)
        sidebar.addWidget(LabeledWidget("Time Interval:", interval_dropdown))
        sidebar.addWidget(LabeledWidget("Local Time:", ThemedRadioButton(GlobalSettings.local_time_changed_callback)))

        sidebar.addWidget(HorizontalSeperator(Styles.theme.medium_spacing))

        



   
