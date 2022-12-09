import asyncio
from datetime import datetime
import PyQt6
import pandas as pd

from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import * 
from PyQt6.QtCore import *
from colorama import Style

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

import pdb


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

        self.metadata_list = []
        self.df = []
        self.utc = 0

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

        #problem here? For displaying time???
        #Is it a constant from the shared time axis?
        #Problem, Gets data from unix timestamp, not datetime
        #Fix value, should work
        PlotHandler.set_time_range(DataHandler.get_time_range())
        for i, column in enumerate(self.graph_columns):
            PlotHandler.plots[i].plot(DataHandler.get_all(column))

    def create_sidebar(self) -> Sidebar:
        #File heading
        sidebar = Sidebar()
        sidebar.setShadow(xOffset=4)
        sidebar.getLayout().setSpacing(Styles.theme.close_spacing)

        sidebar.addWidget(ColoredText("File: ",  Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        file_widgets = [ThemedButton("Import Data", self.import_data), ThemedButton("Clear Data", self.clear_data)]
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
        sidebar.addWidget(ColoredText("Hold Ctrl and Scroll to zoom in/out",  Styles.theme.label_color, Styles.theme.label_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))

        #sidebar.addWidget(ColoredText("Timezone: ", Styles.theme.label_color, Styles.theme.label_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        #sidebar.addWidget(ColoredText("Firmware Version: ", Styles.theme.label_color, Styles.theme.label_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        #sidebar.addWidget(ColoredText("OS: ",  Styles.theme.label_color, Styles.theme.label_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))
        #sidebar.addWidget(ColoredText("GCTS Algorithm: ", Styles.theme.label_color, Styles.theme.label_font_size, margins=(Styles.theme.medium_spacing//2,0,0,0)))

        sidebar.addWidget(ThemedButton("Show Data Description", self.data_description))

        sidebar.addWidget(ThemedButton("Switch Timezone", self.switch_timezone))

        sidebar.addWidget(ThemedButton("Sum", self.aggregate_sum))
        sidebar.addWidget(ThemedButton("Min", self.aggregate_min))
        sidebar.addWidget(ThemedButton("Max", self.aggregate_max))
        #sidebar.relabel("Controls: ", 9, "AAAAA")
        
        return sidebar
        

    def switch_timezone(self):
        i=0
        #fix labels
        #print(self.metadata_list)
        #is UTC, and needs to switch to local
        #pdb.set_trace()
        
        if(self.utc == 0):
            self.utc = 1
            time_diff = self.metadata_list[0][1] * 60

        else:
            self.utc = 0
            time_diff = self.metadata_list[0][1] * 60
            time_diff -= 2 * time_diff

        self
        
        #self.df['Datetime (UTC)'] = pd.to_datetime(self.df['Datetime (UTC)'])
        #pdb.set_trace()
        #self.df['Datetime (UTC)'] = self.df['Datetime (UTC)'] + pd.Timedelta(minutes=time_diff)
        #pdb.set_trace()
        #self.df['Datetime (UTC)'] = self.df['Datetime (UTC)'].astype(str)

        self.df['Unix Timestamp (UTC)'] = self.df['Unix Timestamp (UTC)'] + time_diff

        print(self.df)
        
        self.clear_data()

        #pdb.set_trace()
        #print("Cleared Data")
        #need to be able to populate with the new values I just graphed,
        #or apply these values to the db, then clear and rebuild.

        DataHandler.load_straight_to_db(self.df)
        self.populate_graphs()

        #print("FINISHED")
        #is local, needs to switch back to utc
  

    def import_data(self):
        if self.file_dialog.exec():
            files = self.file_dialog.selectedFiles()
            print(files[0])
            #if contains summary data, store in separate value that is also cleared?
            if 'metadata.csv' in files[0]:
                df = pd.read_csv(files[0])
                self.metadata_list = df.values.tolist()
                print(self.metadata_list)

                #sidebar.relabel("Timezone: ", 9, str(self.metadata_list[0][1]))
                #Sidebar.relabel(10, "Firmware Version: " + str(self.metadata_list[0][2]))
                #Sidebar.relabel(11, "OS: " + str(self.metadata_list[0][5]))
                #Sidebar.relabel(12, "GCTS Algorithm: " + str(self.metadata_list[0][7]))
                
            else:
                DataHandler.import_data_from_csv(files[0])
                self.df = pd.read_csv(files[0])
                print(self.df)
                self.populate_graphs()

    def data_description(self):
        #array is count, mean, std, min, 25%, 50%, 75%, max
        #values for datetime, timezone, unix timestamp, acceletation, eda, temp,
        #movement, steps, rest, on wrist

        #this is ugly because i am too tired to be elegant

        arr_date = []
        arr_acc = []
        arr_eda = []
        arr_temp = []
        arr_movement = []
        arr_steps = []
        arr_rest = []
        
        data_date = self.df['Datetime (UTC)'].describe()
        data_acc = self.df['Acc magnitude avg'].describe()
        data_eda = self.df['Eda avg'].describe()
        data_temp = self.df['Temp avg'].describe()
        data_movement = self.df['Movement intensity'].describe()
        data_steps = self.df['Steps count'].describe()
        data_rest = self.df['Rest'].describe()

        for i in range(8):
            if(i < 4):
                arr_date.append(data_date[i])
            arr_acc.append(data_acc[i])
            arr_eda.append(data_eda[i])
            arr_temp.append(data_temp[i])
            arr_movement.append(data_movement[i])
            arr_steps.append(data_steps[i])
            arr_rest.append(data_rest[i])

        self.w = DescriptionWindow(arr_date,arr_acc,arr_eda,arr_temp
                                   ,arr_movement,arr_steps,arr_rest)

        self.w.show()

        

    def clear_data(self):
        #Sidebar.relabel(9, "Timezone: ")
        #Sidebar.relabel(10, "Firmware Version: ")
        #Sidebar.relabel(11, "OS: ")
        #Sidebar.relabel(12, "GCTS Algorithm: ")
        DataHandler.clear_table()
        PlotHandler.erase_plots()
        self.time_picker.clear_data()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.sidebar.on_resize(event)
        QMainWindow.resizeEvent(self, event)

    def aggregate_sum(self):
        self.aggregate(False, "sum")

    def aggregate_min(self):
        self.aggregate(False, "min")

    def aggregate_max(self):
        self.aggregate(False, "max")

    def aggregate(self, checked, aggregation):
        #if self.w is None:
        value = self.df.agg(aggregation)
        #print("CHECKED: ")
        #print(checked)
        #aggregation = "sum"
        #print(value)
        self.w = AggregationWindow(str(value[0][0:12]), str(value[1]), str(value[2]),
                               str(value[3]), str(value[4]), str(value[5]),
                               str(value[6]), str(value[7]), str(value[8]),
                               str(value[9]), aggregation
                               )
        self.w.show()

class DescriptionWindow(QWidget):
    def __init__(self, date, acc, eda, temp, move, steps, rest
                 ):
        super().__init__()
        layout = QGridLayout()

    
        #count, unique, top, freq

        self.label_date_title = QLabel('Datetime')
        layout.addWidget(self.label_date_title,0,0)

        self.label_date_count= QLabel('count:' + str( date[0]))	
        layout.addWidget(self.label_date_count,0,1)
        self.label_date_mean= QLabel('mean:' + str( date[1]))	
        layout.addWidget(self.label_date_mean,0,2)
        self.label_date_std= QLabel('std:' + str( date[2]))	
        layout.addWidget(self.label_date_std,0,3)
        self.label_date_min= QLabel('min:' + str( date[3]))	

        self.label_acc_title = QLabel('Acceleration')
        layout.addWidget(self.label_acc_title,1,0)

        self.label_acc_count= QLabel('count:' + str( acc[0]))	
        layout.addWidget(self.label_acc_count,1,1)
        self.label_acc_mean= QLabel('mean:' + str( acc[1]))	
        layout.addWidget(self.label_acc_mean,1,2)
        self.label_acc_std= QLabel('std:' + str( acc[2]))	
        layout.addWidget(self.label_acc_std,1,3)
        self.label_acc_min= QLabel('min:' + str( acc[3]))	
        layout.addWidget(self.label_acc_min,1,4)
        self.label_acc_25= QLabel('25:' + str( acc[4]))	
        layout.addWidget(self.label_acc_25,1,5)
        self.label_acc_50= QLabel('50:' + str( acc[5]))	
        layout.addWidget(self.label_acc_50,1,6)
        self.label_acc_75= QLabel('75:' + str( acc[6]))	
        layout.addWidget(self.label_acc_75,1,7)
        self.label_acc_max= QLabel('max:' + str( acc[7]))	
        layout.addWidget(self.label_acc_max,1,8)

        self.label_eda_title = QLabel('EDA')
        layout.addWidget(self.label_eda_title,2,0)

        self.label_eda_count= QLabel('count:' + str( eda[0]))	
        layout.addWidget(self.label_eda_count,2,1)
        self.label_eda_mean= QLabel('mean:' + str( eda[1]))	
        layout.addWidget(self.label_eda_mean,2,2)
        self.label_eda_std= QLabel('std:' + str( eda[2]))	
        layout.addWidget(self.label_eda_std,2,3)
        self.label_eda_min= QLabel('min:' + str( eda[3]))	
        layout.addWidget(self.label_eda_min,2,4)
        self.label_eda_25= QLabel('25:' + str( eda[4]))	
        layout.addWidget(self.label_eda_25,2,5)
        self.label_eda_50= QLabel('50:' + str( eda[5]))	
        layout.addWidget(self.label_eda_50,2,6)
        self.label_eda_75= QLabel('75:' + str( eda[6]))	
        layout.addWidget(self.label_eda_75,2,7)
        self.label_eda_max= QLabel('max:' + str( eda[7]))	
        layout.addWidget(self.label_eda_max,2,8)

        self.label_temp_title = QLabel('Temperature')
        layout.addWidget(self.label_temp_title,3,0)

        self.label_temp_count= QLabel('count:' + str( temp[0]))	
        layout.addWidget(self.label_temp_count,3,1)
        self.label_temp_mean= QLabel('mean:' + str( temp[1]))	
        layout.addWidget(self.label_temp_mean,3,2)
        self.label_temp_std= QLabel('std:' + str( temp[2]))	
        layout.addWidget(self.label_temp_std,3,3)
        self.label_temp_min= QLabel('min:' + str( temp[3]))	
        layout.addWidget(self.label_temp_min,3,4)
        self.label_temp_25= QLabel('25:' + str( temp[4]))	
        layout.addWidget(self.label_temp_25,3,5)
        self.label_temp_50= QLabel('50:' + str( temp[5]))	
        layout.addWidget(self.label_temp_50,3,6)
        self.label_temp_75= QLabel('75:' + str( temp[6]))	
        layout.addWidget(self.label_temp_75,3,7)
        self.label_temp_max= QLabel('max:' + str( temp[7]))	
        layout.addWidget(self.label_temp_max,3,8)

        self.label_move_title = QLabel('Movement Intensity')
        layout.addWidget(self.label_move_title,4,0)

        self.label_move_count= QLabel('count:' + str( move[0]))	
        layout.addWidget(self.label_move_count,4,1)
        self.label_move_mean= QLabel('mean:' + str( move[1]))	
        layout.addWidget(self.label_move_mean,4,2)
        self.label_move_std= QLabel('std:' + str( move[2]))	
        layout.addWidget(self.label_move_std,4,3)
        self.label_move_min= QLabel('min:' + str( move[3]))	
        layout.addWidget(self.label_move_min,4,4)
        self.label_move_25= QLabel('25:' + str( move[4]))	
        layout.addWidget(self.label_move_25,4,5)
        self.label_move_50= QLabel('50:' + str( move[5]))	
        layout.addWidget(self.label_move_50,4,6)
        self.label_move_75= QLabel('75:' + str( move[6]))	
        layout.addWidget(self.label_move_75,4,7)
        self.label_move_max= QLabel('max:' + str( move[7]))	
        layout.addWidget(self.label_move_max,4,8)

        self.label_steps_title = QLabel('Steps')
        layout.addWidget(self.label_steps_title,5,0)

        self.label_steps_count= QLabel('count:' + str( steps[0]))	
        layout.addWidget(self.label_steps_count,5,1)
        self.label_steps_mean= QLabel('mean:' + str( steps[1]))	
        layout.addWidget(self.label_steps_mean,5,2)
        self.label_steps_std= QLabel('std:' + str( steps[2]))	
        layout.addWidget(self.label_steps_std,5,3)
        self.label_steps_min= QLabel('min:' + str( steps[3]))	
        layout.addWidget(self.label_steps_min,5,4)
        self.label_steps_25= QLabel('25:' + str( steps[4]))	
        layout.addWidget(self.label_steps_25,5,5)
        self.label_steps_50= QLabel('50:' + str( steps[5]))	
        layout.addWidget(self.label_steps_50,5,6)
        self.label_steps_75= QLabel('75:' + str( steps[6]))	
        layout.addWidget(self.label_steps_75,5,7)
        self.label_steps_max= QLabel('max:' + str( steps[7]))	
        layout.addWidget(self.label_steps_max,5,8)

        self.label_rest_title = QLabel('Rest')
        layout.addWidget(self.label_rest_title,6,0)

        self.label_rest_count= QLabel('count:' + str( rest[0]))	
        layout.addWidget(self.label_rest_count,6,1)
        self.label_rest_mean= QLabel('mean:' + str( rest[1]))	
        layout.addWidget(self.label_rest_mean,6,2)
        self.label_rest_std= QLabel('std:' + str( rest[2]))	
        layout.addWidget(self.label_rest_std,6,3)
        self.label_rest_min= QLabel('min:' + str( rest[3]))	
        layout.addWidget(self.label_rest_min,6,4)
        self.label_rest_25= QLabel('25:' + str( rest[4]))	
        layout.addWidget(self.label_rest_25,6,5)
        self.label_rest_50= QLabel('50:' + str( rest[5]))	
        layout.addWidget(self.label_rest_50,6,6)
        self.label_rest_75= QLabel('75:' + str( rest[6]))	
        layout.addWidget(self.label_rest_75,6,7)
        self.label_rest_max= QLabel('max:' + str( rest[7]))	
        layout.addWidget(self.label_rest_max,6,8)


        self.setLayout(layout)
    

class AggregationWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, datetime, timezone, unix, acc,
                 eda, temp, movement, steps, rest, on_wrist, aggregation):
        super().__init__()
        layout = QVBoxLayout()

        self.label_aggregation = QLabel("Aggregation: " + aggregation)
        layout.addWidget(self.label_aggregation)
        
        self.label_datetime = QLabel("Datetime: " + datetime)
        layout.addWidget(self.label_datetime)

        self.label_acc = QLabel("Acc: " + acc)
        layout.addWidget(self.label_acc)

        self.label_eda = QLabel("Eda: " + eda)
        layout.addWidget(self.label_eda)

        self.label_temp = QLabel("temp: " + temp)
        layout.addWidget(self.label_temp)

        self.label_movement = QLabel("movement: " + movement)
        layout.addWidget(self.label_movement)

        self.label_steps = QLabel("steps: " + steps)
        layout.addWidget(self.label_steps)

        self.label_rest = QLabel("rest: " + rest)
        layout.addWidget(self.label_steps)

        self.label_on_wrist = QLabel("On Wrist: " + on_wrist)
        layout.addWidget(self.label_on_wrist)

        self.setLayout(layout)
