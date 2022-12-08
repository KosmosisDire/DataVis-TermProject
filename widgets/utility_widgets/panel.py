from widgets.utility_widgets.custom_widget import CustomWidget

class Panel(CustomWidget):
    def __init__(self, color: str = "transparent"):
        super(Panel, self).__init__()

        self.fill(color)
