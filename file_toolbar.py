from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class FileToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("File", parent)
        self.setOrientation(Qt.Horizontal)
        icon_size = QSize(22, 22)
        self.setIconSize(icon_size)
        # self.setFixedHeight(30)

        # Create the Open Diagram button
        open_action = QAction(QIcon("icons/open-document.svg"), "Open Diagram", self)
        self.addAction(open_action)

        # Create the Save button
        save_action = QAction(QIcon("icons/save-icon.svg"), "Save", self)
        self.addAction(save_action)

        # Set toolbar properties
        self.setMovable(True)  # Optional: Make the toolbar non-movable
