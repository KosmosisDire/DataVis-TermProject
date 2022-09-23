from collections.abc import Sequence
from datetime import datetime
from time import sleep, time
from typing import Any, Callable
from joblib import Parallel, delayed

from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
                             QDateTimeEdit, QDial, QDoubleSpinBox,
                             QFontComboBox, QHBoxLayout, QLabel, QLCDNumber,
                             QLineEdit, QMainWindow, QProgressBar, QPushButton,
                             QRadioButton, QSlider, QSpinBox, QTimeEdit,
                             QVBoxLayout, QWidget, QScrollArea)
from global_settings import GlobalSettings
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

from styles import Styles
from data_handler import DataHandler
from widgets.blank_widget import Panel
from widgets.colored_text import ColoredText
from widgets.horizontal_group import HorizontalGroup
from widgets.labeled_widget import LabeledWidget
from widgets.seperator import HorizontalSeperator
from widgets.sidebar_widget import Sidebar
from widgets.themed_button import ThemedButton
from widgets.themed_dropdown import ThemedDropdown
from widgets.themed_radiobutton import ThemedRadioButton
from widgets.themed_scroll_area import ThemedScrollArea
from widgets.time_range_picker import TimeRangePicker
from widgets.themed_plot import ThemedPlot
from widgets.vertical_group import VerticalGroup


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Data Visualizer")
        self.setMinimumSize(int(1920/2), int(1080/2))
        self.resize(1280, 720)

        self.scroll_area: ThemedScrollArea = None
        self.time_picker: TimeRangePicker = None
        self.sidebar: Sidebar = None
        self.base: HorizontalGroup = None
        self.graphs: list[ThemedPlot] = []
        

        self.create_UI()


    def create_UI(self):
        self.base = HorizontalGroup()
        self.setStyleSheet(f"background-color: {Styles.theme.light_background_color_hex};")
        self.sidebar = self.base.addWidget(self.create_sidebar())
        right_area = self.base.addWidget(VerticalGroup())
        graph_header = right_area.addWidget(VerticalGroup())

        time_range = DataHandler.get_time_range()
        self.time_picker = TimeRangePicker(75, datetime.fromtimestamp(time_range[0]), datetime.fromtimestamp(time_range[1]), GlobalSettings.time_range_changed_callback)
        self.time_picker.set_plot_data(DataHandler.get_all("Rest"))
        graph_header.addWidget(self.time_picker)

        self.scroll_area: ThemedScrollArea = right_area.addWidget(ThemedScrollArea())
        self.scroll_area.verticalScrollBar().valueChanged.connect(GlobalSettings.instance.time_range_changed.emit) #update the graphs when scrolling

        self.create_graphs()

        self.scroll_area.addWidgets(self.graphs)

        self.setCentralWidget(self.base)

    def create_graphs(self):
        graph1 = ThemedPlot("Temperature", "Temp avg")
        graph2 = ThemedPlot("Movement Intensity", "Movement intensity")
        graph3 = ThemedPlot("Rest", "Rest")
        graph4 = ThemedPlot("Activity", "Acc magnitude avg")
        graph5 = ThemedPlot("Temperature", "Temp avg")
        graph6 = ThemedPlot("Movement Intensity", "Movement intensity")
        graph7 = ThemedPlot("Rest", "Rest")
        graph8 = ThemedPlot("Activity", "Acc magnitude avg")
        graph9 = ThemedPlot("Temperature", "Temp avg")
        graph10 = ThemedPlot("Movement Intensity", "Movement intensity")
        graph11 = ThemedPlot("Rest", "Rest")
        graph12 = ThemedPlot("Activity", "Acc magnitude avg")

        self.graphs = [graph1, graph2, graph3, graph4, graph5, graph6, graph7, graph8, graph9, graph10, graph11, graph12]

    def create_sidebar(self) -> Sidebar:

        #File heading
        sidebar = Sidebar()
        sidebar.getLayout().setSpacing(Styles.theme.close_spacing)

        sidebar.addWidget(ColoredText("File: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        file_widgets = [ThemedButton("Import Data", DataHandler.open_import_window), ThemedButton("Clear Data", DataHandler.clear_table)]
        sidebar.addWidget(HorizontalGroup(file_widgets, Styles.theme.medium_spacing))
        
        sidebar.addWidget(HorizontalSeperator(Styles.theme.medium_spacing))

        # View heading
        sidebar.addWidget(ColoredText("View: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        moving_avg_dropdown = ThemedDropdown(["None", "1 Minute","2 Minutes","4 Minutes","5 Minutes","10 Minutes","15 Minutes","30 Minutes","1 Hour"], GlobalSettings.moving_average_seconds_changed_callback)
        sidebar.addWidget(LabeledWidget("Moving Average:", moving_avg_dropdown))
        interval_dropdown = ThemedDropdown(["30 Seconds","1 Minute","2 Minutes","4 Minutes","5 Minutes","10 Minutes","15 Minutes","30 Minutes","1 Hour"], GlobalSettings.aggregation_changed_callback)
        interval_dropdown.setCurrentIndex(4)
        sidebar.addWidget(LabeledWidget("Time Interval:", interval_dropdown))
        sidebar.addWidget(LabeledWidget("Local Time:", ThemedRadioButton(GlobalSettings.local_time_changed_callback)))
        sidebar.addWidget(LabeledWidget("Angle Filter:", ThemedRadioButton(GlobalSettings.use_angle_aggregation_changed_callback)))
        sidebar.addWidget(HorizontalSeperator(Styles.theme.medium_spacing))

        return sidebar

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.sidebar.on_resize(event)
        QMainWindow.resizeEvent(self, event)

        



   
