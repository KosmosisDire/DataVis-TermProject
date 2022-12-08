from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import * 
from PyQt6.QtCore import *

from data_handler import DataHandler
from plot_handler import PlotHandler
from styles import Styles
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.graph_columns = [
            "Rest",
            "Steps count",
            "Movement intensity",
            "Temp avg",
            "Eda avg",
            "Acc magnitude avg",
        ]
        
        self.setWindowTitle("Data Visualizer")
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

        self.time_picker = TimeRangePicker(75, PlotHandler.set_time_range)
        graph_header.addWidget(self.time_picker)

        self.scroll_area: ThemedScrollArea = right_area.addWidget(ThemedScrollArea())
        self.scroll_area.setContentsMargins((0, Styles.theme.medium_spacing, 0, Styles.theme.medium_spacing))
        self.scroll_area.verticalScrollBar().valueChanged.connect(PlotHandler.regenerate_plots) #update the graphs when scrolling

        self.create_graphs()

        self.setCentralWidget(background)

    def create_graphs(self):
        PlotHandler.set_plot_height(self.plot_height)
        for i in range(len(self.graph_columns)):
            graph = ThemedPlot()
            PlotHandler.add_plot(graph)
            self.scroll_area.addWidget(graph)

    def populate_graphs(self):
        self.time_picker.set_time_range(DataHandler.get_time_range())
        self.time_picker.set_plot_data(DataHandler.get_all("Steps count"))

        PlotHandler.set_time_range(DataHandler.get_time_range())
        for i, column in enumerate(self.graph_columns):
            PlotHandler.plots[i].plot(DataHandler.get_all(column))

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

        # add space
        sidebar.addWidget(HorizontalSeperator(Styles.theme.medium_spacing))

        # add local time checkbox
        sidebar.addWidget(LabeledWidget("Local Time:", ThemedRadioButton(PlotHandler.convert_local_timezone, True)))
        
        # this shows some instruction for controls, but I am removing it for now.
        # sidebar.addWidget(ColoredText("Controls: ", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        # sidebar.addWidget(ColoredText("Hold Ctrl and Scroll to zoom in/out", Styles.theme.label_color, Styles.theme.label_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))

        return sidebar

    def import_data(self):
        if self.file_dialog.exec():
            files = self.file_dialog.selectedFiles()
            DataHandler.import_data_from_csv(files[0])
            self.populate_graphs()

    def clear_data(self):
        DataHandler.clear_table()
        PlotHandler.erase_plots()
        self.time_picker.clear_data()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.sidebar.on_resize(event)
        QMainWindow.resizeEvent(self, event)
