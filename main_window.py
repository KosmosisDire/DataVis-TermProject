import asyncio
from datetime import datetime
import PyQt6

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import * 
from PyQt6.QtCore import *
from colorama import Style 

from data_handler import DataHandler
from plot_handler import PlotHandler
from styles import Styles
from widgets.colored_text import ColoredText
from widgets.horizontal_group import HorizontalGroup
from widgets.labeled_widget import LabeledWidget
from widgets.panel import Panel
from widgets.seperator import HorizontalSeperator
from widgets.sidebar import Sidebar
from widgets.themed_button import ThemedButton
from widgets.themed_dropdown import ThemedDropdown
from widgets.themed_plot import ThemedPlot
from widgets.themed_radiobutton import ThemedRadioButton
from widgets.themed_scroll_area import ThemedScrollArea
from widgets.time_range_picker import TimeRangePicker
from widgets.vertical_group import VerticalGroup

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg


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

        self.plot_height = 120
        self.ctrl_down = False

        self.create_UI()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Control:
            self.ctrl_down = True
            self.scroll_area.lock()

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Control:
            self.ctrl_down = False
            self.scroll_area.unlock()

        super().keyReleaseEvent(event)

    def wheelEvent(self, a0: QWheelEvent):
        if self.ctrl_down:
            self.plot_height += 5 * a0.angleDelta().y() / 120
            self.plot_height = max(Styles.theme.medium_spacing * 2, self.plot_height)
            PlotHandler.set_plot_height(int(self.plot_height))

    def create_UI(self):
        background = Panel(Styles.theme.light_background_color_hex)
        self.base = background.addWidget(HorizontalGroup())

        self.sidebar : Sidebar = self.base.addWidget(self.create_sidebar())
        self.sidebar.widthAnimation.finished.connect(PlotHandler.regenerate_plots)
        right_area = self.base.addWidget(VerticalGroup())
        right_area.stackUnder(self.sidebar)

        graph_header: Panel = right_area.addWidget(Panel(Styles.theme.light_background_color_hex))
        graph_header.setShadow(xOffset=4)

        time_range = DataHandler.get_time_range()
        self.time_picker = TimeRangePicker(75, datetime.fromtimestamp(time_range[0]), datetime.fromtimestamp(time_range[1]), PlotHandler.set_time_range)
        self.time_picker.set_plot_data(DataHandler.get_all("Steps count"))
        graph_header.addWidget(self.time_picker)

        self.scroll_area: ThemedScrollArea = right_area.addWidget(ThemedScrollArea())
        self.scroll_area.setContentsMargins((0, Styles.theme.medium_spacing, 0, Styles.theme.medium_spacing))
        self.scroll_area.verticalScrollBar().valueChanged.connect(PlotHandler.regenerate_plots) #update the graphs when scrolling

        self.create_graphs()

        self.setCentralWidget(background)

    def create_graphs(self):
        graph1 = ThemedPlot()
        graph1.plot(DataHandler.get_all("Rest"))
        graph2 = ThemedPlot()
        graph2.plot(DataHandler.get_all("Steps count"))
        graph3 = ThemedPlot()
        graph3.plot(DataHandler.get_all("Movement intensity"))
        graph4 = ThemedPlot()
        graph4.plot(DataHandler.get_all("Temp avg"))
        graph5 = ThemedPlot()
        graph5.plot(DataHandler.get_all("Eda avg"))
        graph6 = ThemedPlot()
        graph6.plot(DataHandler.get_all("Acc magnitude avg"))
        graph7 = ThemedPlot()
        graph7.plot(DataHandler.get_all("Rest"))
        graph8 = ThemedPlot()
        graph8.plot(DataHandler.get_all("Steps count"))
        graph9 = ThemedPlot()
        graph9.plot(DataHandler.get_all("Movement intensity"))
        graph10 = ThemedPlot()
        graph10.plot(DataHandler.get_all("Temp avg"))
        graph11 = ThemedPlot()
        graph11.plot(DataHandler.get_all("Eda avg"))
        graph12 = ThemedPlot()
        graph12.plot(DataHandler.get_all("Acc magnitude avg"))

        graphs = [graph1, graph2, graph3, graph4, graph5, graph6, graph7, graph8, graph9, graph10, graph11, graph12]
        self.scroll_area.addWidgets(graphs)
        
        PlotHandler.set_plot_height(self.plot_height)
        PlotHandler.add_plots(graphs)
        PlotHandler.set_time_range(DataHandler.get_time_range())
        

    def create_sidebar(self) -> Sidebar:
        #File heading
        sidebar = Sidebar()
        sidebar.setShadow(xOffset=4)
        sidebar.getLayout().setSpacing(Styles.theme.close_spacing)

        sidebar.addWidget(ColoredText("File: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        file_widgets = [ThemedButton("Import Data", DataHandler.open_import_window), ThemedButton("Clear Data", DataHandler.clear_table)]
        sidebar.addWidget(HorizontalGroup(file_widgets, Styles.theme.medium_spacing))
        
        sidebar.addWidget(HorizontalSeperator(Styles.theme.medium_spacing))

        # View heading
        sidebar.addWidget(ColoredText("View: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        moving_avg_dropdown = ThemedDropdown({"None" : 0, "2 Minutes" : 120,"4 Minutes" : 240, "8 Minutes" : 480,"16 Minutes" : 960,"32 Minutes" : 1920, "1 Hour": 3600, "4 Hours": 14400}, PlotHandler.set_moving_average)
        moving_avg_dropdown.setCurrentIndex(2)
        sidebar.addWidget(LabeledWidget("Moving Average:", moving_avg_dropdown))
        interval_dropdown = ThemedDropdown({"None" : 0, "2 Minutes" : 120,"4 Minutes" : 240, "8 Minutes" : 480,"16 Minutes" : 960,"32 Minutes" : 1920, "1 Hour": 3600}, PlotHandler.set_aggregation_interval)
        interval_dropdown.setCurrentIndex(3)
        sidebar.addWidget(LabeledWidget("Time Interval:", interval_dropdown))
        #sidebar.addWidget(LabeledWidget("Local Time:", ThemedRadioButton(GlobalSettings.local_time_changed_callback)))
        sidebar.addWidget(HorizontalSeperator(Styles.theme.medium_spacing))
        sidebar.addWidget(ColoredText("Controls: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        sidebar.addWidget(ColoredText("Hold Ctrl and Scroll to zoom in/out", Styles.theme.label_color, Styles.theme.label_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))

        return sidebar

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.sidebar.on_resize(event)
        QMainWindow.resizeEvent(self, event)

        



   
