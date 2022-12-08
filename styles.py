from __future__ import annotations
from cProfile import label
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtWidgets import QGraphicsDropShadowEffect



class Styles:
    theme: Styles = None

    def __init__(self):
        self.header_text_color_hex: str = "#EBB66F"
        self.header_bar_color_hex: str = "#2C2621"
        self.label_color_hex: str = "#D9C5A8"
        self.button_text_color_hex: str = "#E3BF8C"
        self.light_background_color_hex: str = "#2C2621"
        self.mid_background_color_hex: str = "#342B23"
        self.dark_background_color_hex: str = "#231E1A"
        self.button_color_hex: str = "#3D3429"
        self.button_hover_color_hex: str = "#4D4239"
        self.button_pressed_color_hex: str = "#5D5239"
        self.placeholder_text_color_hex: str = "#C4C4C4C4"
        self.shroud_color_hex: str = "#000000"
        self.shroud_opacity: float = 0.4
        self.seperator_color_hex: str = "#707070"
        self.data_colors_hex: list[str] = ["#EBB66F", "#A9EB6F", "#6FBDEB", "#EB6F80", "#FFFFFF"]
        self.shadow_color_hex: str = "#000000"
        self.shadow_opacity: float = 0.4

        self.update_colors_from_hex()

        self.header_font_size: int = 25
        self.label_font_size: int = 18
        self.button_font_size: int = 11
        self.textbox_font_size: int = 10

        self.panel_radius: int = 10
        self.control_radius: int = 5
        self.panel_shadow_radius: int = 24
        self.control_shadow_radius: int = 12
    

        self.close_spacing: int = 8
        self.medium_spacing: int = 24
        self.large_spacing: int = 64
        self.huge_spacing: int = 128

        self.button_height: int = 24
        self.min_sidebar_width: int = 350

        self.slider_handle_width = 7

        self.font_family: str = "Segoe UI"

        

        Styles.theme = self

    def apply_theme(style: Styles):
        Styles.theme = style
        style.update_colors_from_hex()

    def update_colors_from_hex(self):
        self.header_text_color: QColor = QColor(self.header_text_color_hex)
        self.header_bar_color: QColor = QColor(self.header_bar_color_hex)
        self.label_color: QColor = QColor(self.label_color_hex)
        self.button_text_color: QColor = QColor(self.button_text_color_hex)
        self.light_background_color: QColor = QColor(self.light_background_color_hex)
        self.mid_background_color: QColor = QColor(self.mid_background_color_hex)
        self.dark_background_color: QColor = QColor(self.dark_background_color_hex)
        self.button_color: QColor = QColor(self.button_color_hex)
        self.button_hover_color: QColor = QColor(self.button_hover_color_hex)
        self.button_pressed_color: QColor = QColor(self.button_pressed_color_hex)
        self.placeholder_text_color: QColor = QColor(self.placeholder_text_color_hex)
        self.shroud_color: QColor = QColor(self.shroud_color_hex)
        self.seperator_color: QColor = QColor(self.seperator_color_hex)
        self.shadow_color: QColor = QColor(self.shadow_color_hex)
        self.shadow_color.setAlphaF(self.shadow_opacity)

blue_theme: Styles = Styles()
blue_theme.header_text_color_hex = "#C5D0EC"
blue_theme.header_bar_color_hex = "#21242c"
blue_theme.label_color_hex = "#909C9E"
blue_theme.button_text_color_hex = "#8CB5E3"
blue_theme.light_background_color_hex = "#21242C"
blue_theme.mid_background_color_hex = "#272940"
blue_theme.dark_background_color_hex = "#1B1A23"
blue_theme.button_color_hex = "#343754"
blue_theme.button_hover_color_hex = "#4b507a"
blue_theme.button_pressed_color_hex = "#6269a0"
blue_theme.placeholder_text_color_hex = "#C4C4C4C4"
blue_theme.shroud_color_hex = "#000000"
blue_theme.shroud_opacity = 0.4
blue_theme.seperator_color_hex = "#707070"
blue_theme.data_colors_hex = ["#EBB66F", "#A9EB6F", "#6FBDEB", "#EB6F80", "#FFFFFF"]

light_theme: Styles = Styles()
light_theme.header_text_color_hex = "#870E00"
light_theme.header_bar_color_hex = "#efe7d7"
light_theme.label_color_hex = "#870E00"
light_theme.button_text_color_hex = "#4A280A"
light_theme.light_background_color_hex = "#EFE7D7"
light_theme.mid_background_color_hex = "#CBC1B0"
light_theme.dark_background_color_hex = "#EEEAE0"
light_theme.button_color_hex = "#FFFDE8"
light_theme.button_hover_color_hex = "#cccab9"
light_theme.button_pressed_color_hex = "#99978a"
light_theme.placeholder_text_color_hex = "#8d7152"
light_theme.shroud_color_hex = "#FFFFFF"
light_theme.shroud_opacity = 0.4
light_theme.seperator_color_hex = "#32251d"
light_theme.data_colors_hex = ["#3a4f25", "#870e00", "#25404f", "#833e48", "#000000", "472a4f"]

themes = {
    "Warm": Styles(),
    "Cool": blue_theme,
}

Styles.apply_theme(themes["Warm"])