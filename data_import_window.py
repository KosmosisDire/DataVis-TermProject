import asyncio
from time import sleep
import time
from PyQt6.QtWidgets import QWidget
from data_handler import DataHandler
from plot_handler import PlotHandler
from styles import Styles
from widgets.new_widgets.tag_selector import TagSelector
from widgets.themed_widgets.colored_text import ColoredText
from widgets.utility_widgets.panel import Panel
from widgets.utility_widgets.seperator import HorizontalSeperator
from widgets.utility_widgets.vertical_group import VerticalGroup
from widgets.utility_widgets.horizontal_group import HorizontalGroup
from widgets.themed_widgets.themed_textbox import ThemedTextbox
from widgets.themed_widgets.themed_button import ThemedButton
from PyQt6.QtCore import Qt # AlignmentFlag
from PyQt6.QtGui import QCloseEvent, QIcon, QColor

import main_window

class ImportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import Data")
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setMinimumSize(500, 600)
        self.resize(500, 600)

        self.csv_path: str = None
        self.data_handler: DataHandler = None
        self.csv_path_textbox: ThemedTextbox = None
        self.column_selector: TagSelector = None
        self.is_path_valid = False
        self.error_message_text: ColoredText = None

        self.create_UI()
    
    def create_UI(self):
        self.setStyleSheet(f"background-color: {Styles.theme.dark_background_color_hex};")

        vertical_layout = VerticalGroup(spacing=0)
        vertical_layout.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        header: Panel = vertical_layout.addWidget(Panel(Styles.theme.header_bar_color_hex, True))
        header.setFixedHeight(50)

        header.addWidget(ColoredText("Import Data", Styles.theme.header_text_color, Styles.theme.header_font_size, margins=(Styles.theme.medium_spacing, 0, 0, 0)))

        vertical_controls_layout = vertical_layout.addWidget(VerticalGroup(spacing=0, margins=(Styles.theme.medium_spacing, Styles.theme.medium_spacing, Styles.theme.medium_spacing, Styles.theme.medium_spacing)))
        vertical_controls_layout.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        vertical_controls_layout.addWidget(ColoredText("Path:", Styles.theme.label_color, Styles.theme.label_font_size))
        path_browse_horizontal = vertical_controls_layout.addWidget(HorizontalGroup(spacing=Styles.theme.medium_spacing, margins=(0, 0, 0, 0)))
        self.csv_path_textbox = path_browse_horizontal.addWidget(ThemedTextbox(placeholder="/path to .csv file/", textChanged=self.set_manual_path))
        browse_button = path_browse_horizontal.addWidget(ThemedButton("Browse", clicked=self.browse_for_csv))
        browse_button.setFixedWidth(100)

        vertical_controls_layout.addWidget(HorizontalSeperator(Styles.theme.huge_spacing, 1))

        vertical_controls_layout.addWidget(ColoredText("Columns To Import:", Styles.theme.header_text_color, Styles.theme.header_font_size))
        self.column_selector = vertical_controls_layout.addWidget(TagSelector([]))

        vertical_controls_layout.addWidget(HorizontalSeperator(Styles.theme.medium_spacing, 1))

        import_button:ThemedButton = vertical_controls_layout.addWidget(ThemedButton("Import"))
        import_button.clicked.connect(self.import_data, Qt.ConnectionType.QueuedConnection)

        self.error_message_text: ColoredText = vertical_controls_layout.addWidget(ColoredText("", QColor(223, 69, 58), 14, margins=(0, Styles.theme.medium_spacing, 0, Styles.theme.medium_spacing)))


        self.setLayout(vertical_layout.layout())

    def browse_for_csv(self) -> str:
        if main_window.MainWindow.instance.file_dialog.exec():
            files = main_window.MainWindow.instance.file_dialog.selectedFiles()
            self.csv_path = files[0]
            self.csv_path_textbox.setText(self.csv_path)

            self.process_path()

    def set_manual_path(self, path: str):
        self.csv_path = path
        self.process_path()

    def process_path(self):
        tags = DataHandler.get_column_names_from_file(self.csv_path)

        if not tags:
            self.is_path_valid = False
            return
        
        self.is_path_valid = True

        # filter out columns with the word "time" in them
        tags = [tag for tag in tags if "time" not in tag.lower()]
        self.column_selector.update_tags(tags)


    def import_data(self):
        if not self.is_path_valid or self.csv_path is None or self.csv_path == "":
            self.error_message_text.setText("Error importing data: \nThe selected .csv file is invalid.")
            return

        if len(self.column_selector.get_selected_tags()) == 0:
            self.error_message_text.setText("Error importing data: \nNo columns selected to import!")
            return

        PlotHandler.clear_plots()
        main_window.MainWindow.instance.graph_columns = self.column_selector.get_selected_tags()
        main_window.MainWindow.instance.create_graphs()

        if not DataHandler.import_data_from_csv(self.csv_path):
            self.error_message_text.setText("Error importing data: \nMake sure the .csv has a column named 'Unix Timestamp (UTC)'")
            PlotHandler.clear_plots()
            return

        self.error_message_text.setText("")

        main_window.MainWindow.instance.populate_graphs()