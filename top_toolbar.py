from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import QSize
from file_toolbar import FileToolbar
from text_toolbar import TextToolbar


class TopToolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the file and text toolbars
        self.file_toolbar = FileToolbar(self)
        self.text_toolbar = TextToolbar(self)

        # Adjust toolbar button sizes
        icon_size = QSize(22, 22)  # Set a smaller icon size
        self.file_toolbar.setIconSize(icon_size)
        self.text_toolbar.setIconSize(icon_size)

        # Remove padding/margins from the toolbar layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)  # Remove spacing between toolbars
        layout.addWidget(self.file_toolbar)
        layout.addWidget(self.text_toolbar)

        # Set the layout for the widget
        self.setLayout(layout)
