from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QApplication,
    QGraphicsScene,
)
from PyQt5.QtCore import Qt
from tool_selection_bar import ToolSelectionBar
from text_toolbar import TextToolbar
from diagram_canvas import DiagramCanvas  # Assuming this is where the drawing happens


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ER Diagram Editor")
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Diagram canvas
        self.scene = QGraphicsScene()
        self.view = DiagramCanvas(self.scene)
        main_layout.addWidget(self.view)

        # Toolbars
        self.tool_selection_bar = ToolSelectionBar(self)
        self.addToolBar(Qt.LeftToolBarArea, self.tool_selection_bar)  # Left side

        self.text_toolbar = TextToolbar(self)
        self.addToolBar(Qt.TopToolBarArea, self.text_toolbar)  # Top side

        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
