from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QApplication,
    QGraphicsScene,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from tool_selection_bar import ToolSelectionBar
from text_toolbar import TextToolbar
from file_toolbar import FileToolbar
from diagram_canvas import DiagramCanvas
from er_diagram import ErDiagramItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagramator")
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Create a horizontal layout for the top toolbars
        top_toolbar_layout = QHBoxLayout()
        top_toolbar_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        top_toolbar_layout.setSpacing(0)  # Remove spacing between toolbars

        # Initialize the file and text toolbars
        self.file_toolbar = FileToolbar(self)
        self.text_toolbar = TextToolbar(self)

        # Create a vertical line as a divider
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Sunken)

        # Add the toolbars and divider to the horizontal layout
        top_toolbar_layout.addWidget(self.file_toolbar)
        top_toolbar_layout.addWidget(divider)

        # Add a spacer between the divider and text toolbar
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        top_toolbar_layout.addSpacerItem(spacer)

        top_toolbar_layout.addWidget(self.text_toolbar)

        # Create a container widget for the top toolbar layout and add it to the main layout
        top_toolbar_widget = QWidget()
        top_toolbar_widget.setLayout(top_toolbar_layout)
        top_toolbar_widget.setFixedHeight(30)  # Set the height of the toolbar container
        main_layout.addWidget(top_toolbar_widget)

        # Diagram canvas
        self.scene = QGraphicsScene()
        self.scene.main_window = self  # Provide access to MainWindow from the scene
        self.view = DiagramCanvas(self.scene)
        main_layout.addWidget(self.view)

        # Toolbars
        self.tool_selection_bar = ToolSelectionBar(self)
        self.addToolBar(Qt.LeftToolBarArea, self.tool_selection_bar)  # Left side

        # Set the central widget
        self.setCentralWidget(central_widget)

        # Connect selection change signal to update toolbar state
        self.scene.selectionChanged.connect(self.update_toolbar_state)

    def update_toolbar_state(self):
        selected_items = self.get_selected_items()

        if not selected_items:
            # No selection: reset all buttons
            self.text_toolbar.bold_action.setChecked(False)
            self.text_toolbar.italic_action.setChecked(False)
            self.text_toolbar.underline_action.setChecked(False)
            return

        # Initialize state variables
        bold_state = None
        italic_state = None
        underline_state = None

        for item in selected_items:
            if isinstance(item, ErDiagramItem):
                font = item.text_item.font()

                # Bold state
                if bold_state is None:
                    bold_state = font.bold()
                elif bold_state != font.bold():
                    bold_state = "mixed"

                # Italic state
                if italic_state is None:
                    italic_state = font.italic()
                elif italic_state != font.italic():
                    italic_state = "mixed"

                # Underline state
                if underline_state is None:
                    underline_state = font.underline()
                elif underline_state != font.underline():
                    underline_state = "mixed"

        # Update the toolbar buttons based on the state variables
        self.update_button_state(self.text_toolbar.bold_action, bold_state)
        self.update_button_state(self.text_toolbar.italic_action, italic_state)
        self.update_button_state(self.text_toolbar.underline_action, underline_state)

    def update_button_state(self, action, state):
        if state == "mixed":
            action.setCheckable(False)  # Disable the checkable state to indicate mixed
            action.setEnabled(False)  # Optionally disable the button to indicate mixed
        else:
            action.setCheckable(True)
            action.setChecked(state)
            action.setEnabled(True)

    def get_selected_items(self):
        # Return the selected items from the scene
        return self.scene.selectedItems()

    def switch_to_selection_tool(self):
        self.tool_selection_bar.select_tool("select")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
