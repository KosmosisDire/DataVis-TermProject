from __future__ import annotations
import threading
import time
from typing import Dict, List
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import * 
from PyQt6.QtCore import *

from widgets.themed_widgets.colored_text import ColoredText
from widgets.utility_widgets.horizontal_group import HorizontalGroup
from widgets.utility_widgets.labeled_widget import LabeledWidget
from widgets.utility_widgets.panel import Panel
from widgets.utility_widgets.seperator import HorizontalSeperator
from widgets.new_widgets.sidebar import Sidebar
from widgets.themed_widgets.themed_button import ThemedButton
from widgets.themed_widgets.themed_dropdown import ThemedDropdown
from widgets.new_widgets.themed_plot import ThemedPlot
from widgets.themed_widgets.themed_radiobutton import ThemedRadioButton
from widgets.themed_widgets.themed_scroll_area import ThemedScrollArea
from widgets.new_widgets.time_range_picker import TimeRangePicker
from widgets.utility_widgets.vertical_group import VerticalGroup

from data_handler import DataHandler
from plot_handler import PlotHandler
from column_stats_window import ColumnStatsWindow
from styles import Styles
from data_import_window import ImportWindow


class MainWindow(QMainWindow):

    instance: MainWindow = None

    def __init__(self):
        super().__init__()

        MainWindow.instance = self

        self.graph_columns = []
        
        self.setWindowTitle("Natural Grapher")
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setMinimumSize(int(1920/2), int(1080/2))
        self.resize(1280, 720)

        self.scroll_area: ThemedScrollArea = None
        self.time_picker: TimeRangePicker = None
        self.sidebar: Sidebar = None
        self.base: HorizontalGroup = None

        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.file_dialog.setNameFilter("csv (*.csv)")

        self.plot_height = 120
        self.ctrl_down = False

        self.w = None

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

    def closeEvent(self, event):
        if self.w is not None:
            self.w.close()

    def create_UI(self):
        background = Panel(Styles.theme.mid_background_color)
        self.base = background.addWidget(HorizontalGroup())


        self.sidebar : Sidebar = self.base.addWidget(self.create_sidebar())
        self.sidebar.widthAnimation.finished.connect(PlotHandler.redraw_plots)
        right_area = self.base.addWidget(VerticalGroup())
        right_area.stackUnder(self.sidebar)

        graph_header: Panel = right_area.addWidget(Panel(Styles.theme.header_bar_color))
        graph_header.setShadow(xOffset=4)

        self.time_picker = TimeRangePicker(75, PlotHandler.set_time_range)
        graph_header.addWidget(self.time_picker)

        self.scroll_area: ThemedScrollArea = right_area.addWidget(ThemedScrollArea())
        self.scroll_area.setContentsMargins((0, Styles.theme.medium_spacing, 0, Styles.theme.medium_spacing))
        self.scroll_area.verticalScrollBar().valueChanged.connect(PlotHandler.redraw_plots) #update the graphs when scrolling

        self.setCentralWidget(background)

    def create_graphs(self):
        PlotHandler.clear_plots()
        PlotHandler.set_plot_height(self.plot_height)

        for i in range(len(self.graph_columns)):
            graph = ThemedPlot(self.graph_columns[i], i)
            graph.setToolTip(self.graph_columns[i])
            PlotHandler.add_plot(graph)
            self.scroll_area.addWidget(graph)

    def populate_graphs(self):
        self.time_picker.set_time_range(DataHandler.get_time_range())
        self.time_picker.set_plot_data(DataHandler.get_all(self.graph_columns[0]))

        for i, column in enumerate(self.graph_columns):
            PlotHandler.plots[i].plot(DataHandler.get_all(column))
            PlotHandler.plots[i].update()

        PlotHandler.set_time_range(DataHandler.get_time_range())

        regen_thread = threading.Thread(target=self.regen_plots_delayed)
        regen_thread.start()
    
    def regen_plots_delayed(self):
        time.sleep(0.05)
        PlotHandler.redraw_plots()

    def create_sidebar(self) -> Sidebar:
        #File heading
        sidebar = Sidebar()
        sidebar.setShadow(xOffset=4)
        sidebar.getLayout().setSpacing(Styles.theme.close_spacing)

        sidebar.addWidget(ColoredText("File: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        file_widgets = [ThemedButton("Import Data", self.import_data), ThemedButton("Clear Data", self.clear_data)]
        sidebar.addWidget(HorizontalGroup(file_widgets, Styles.theme.medium_spacing))
        
        sidebar.addWidget(HorizontalSeperator(Styles.theme.medium_spacing))

        # View heading
        sidebar.addWidget(ColoredText("View: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        
        # add moving average interal dropdown
        moving_avg_dropdown = ThemedDropdown({"None" : 0, "2 Minutes" : 120,"4 Minutes" : 240, "8 Minutes" : 480,"16 Minutes" : 960,"32 Minutes" : 1920, "1 Hour": 3600, "4 Hours": 14400}, PlotHandler.set_moving_average)
        moving_avg_dropdown.setCurrentIndex(2)
        sidebar.addWidget(LabeledWidget("Moving Average:", moving_avg_dropdown))
        
        # add aggregation interval dropdown
        interval_dropdown = ThemedDropdown({"None" : 0, "2 Minutes" : 120,"4 Minutes" : 240, "8 Minutes" : 480,"16 Minutes" : 960,"32 Minutes" : 1920, "1 Hour": 3600}, PlotHandler.set_aggregation_interval)
        interval_dropdown.setCurrentIndex(3)
        sidebar.addWidget(LabeledWidget("Time Interval:", interval_dropdown))

        # add local time checkbox
        sidebar.addWidget(LabeledWidget("Show Local Time:", ThemedRadioButton(PlotHandler.convert_local_timezone, True)))

        # add space
        sidebar.addWidget(HorizontalSeperator(Styles.theme.medium_spacing))
        sidebar.addWidget(ColoredText("Statistics: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        
        stats_button = sidebar.addWidget(HorizontalGroup([ThemedButton("Show Data Statistics", self.data_description)]))
        stats_button.layout().setContentsMargins(Styles.theme.medium_spacing,Styles.theme.close_spacing,Styles.theme.medium_spacing,Styles.theme.close_spacing)

        # position individual stats in a horizontal group
        stats_group = HorizontalGroup(spacing=Styles.theme.close_spacing)
        stats_group.layout().setContentsMargins(Styles.theme.medium_spacing,0,Styles.theme.medium_spacing,0)
        stats_group.addWidget(ThemedButton("Show Sums", self.aggregate_sum))
        stats_group.addWidget(ThemedButton("Show Mins", self.aggregate_min))
        stats_group.addWidget(ThemedButton("Show Maxes", self.aggregate_max))
        sidebar.addWidget(stats_group)

        # this shows some instruction for controls, but I am removing it for now.
        # sidebar.addWidget(ColoredText("Controls: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        # sidebar.addWidget(ColoredText("Hold Ctrl and Scroll to zoom in/out", Styles.theme.label_color, Styles.theme.label_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))



        return sidebar

    def import_data(self):
        self.w = ImportWindow()
        self.w.show()

    def clear_data(self):
        self.graph_columns.clear()
        DataHandler.clear_table()
        PlotHandler.clear_plots()
        self.time_picker.clear_data()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.sidebar.on_resize(event)
        QMainWindow.resizeEvent(self, event)

    def data_description(self):
        #description is returned as array of: count, mean, std, min, 25%, 50%, 75%, max

        if not DataHandler.is_data_imported:
            return

        descriptions_dict: Dict[str, List] = {}
        
        for column in self.graph_columns:
            descriptions_dict[column] = DataHandler.df[column].describe().to_list()

        self.w = ColumnStatsWindow(descriptions_dict, "Column Statistics", True)

        self.w.show()

    def aggregate_sum(self):
        self.aggregate("sum", "Column Sums")

    def aggregate_min(self):
        self.aggregate("min", "Column Mins")

    def aggregate_max(self):
        self.aggregate("max", "Column Maxes")

    def aggregate(self, aggregation, aggregation_display_name):
        
        if not DataHandler.is_data_imported:
            return

        aggregation_dict: Dict[str, List] = {}

        for column in self.graph_columns:
            aggregation_dict[column] = [DataHandler.df[column].agg(aggregation)]

        self.w = ColumnStatsWindow(aggregation_dict, aggregation_display_name, False)

        self.w.show()









