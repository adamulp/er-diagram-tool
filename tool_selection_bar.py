from PyQt5.QtWidgets import QToolBar, QAction, QActionGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from diagram_canvas import DiagramCanvas  # Import DiagramCanvas
from double_arrow_connector import DoubleArrowConnector


class ToolSelectionBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOrientation(Qt.Vertical)  # Set the toolbar to be vertical

        # Rectangle Tool Action
        self.rect_action = QAction(QIcon("icons/rectangle.svg"), "Rectangle Tool", self)
        self.rect_action.setCheckable(True)
        self.rect_action.triggered.connect(lambda: self.set_tool("rect"))
        self.addAction(self.rect_action)

        # Oval Tool Action
        self.oval_action = QAction(QIcon("icons/oval.svg"), "Oval Tool", self)
        self.oval_action.setCheckable(True)
        self.oval_action.triggered.connect(lambda: self.set_tool("oval"))
        self.addAction(self.oval_action)

        # Diamond Tool Action
        self.diamond_action = QAction(QIcon("icons/diamond.svg"), "Diamond Tool", self)
        self.diamond_action.setCheckable(True)
        self.diamond_action.triggered.connect(lambda: self.set_tool("diamond"))
        self.addAction(self.diamond_action)

        # Triangle Tool Action (Use a placeholder if triangle.svg is missing)
        self.triangle_action = QAction(
            QIcon("icons/triangle.svg"), "Triangle Tool", self
        )
        self.triangle_action.setCheckable(True)
        self.triangle_action.triggered.connect(lambda: self.set_tool("triangle"))
        self.addAction(self.triangle_action)

        # Arrow Connector Tool Action
        self.arrow_action = QAction(
            QIcon("icons/arrow.svg"), "Arrow Connector Tool", self
        )
        self.arrow_action.setCheckable(True)
        self.arrow_action.triggered.connect(lambda: self.set_tool("arrow_connector"))
        self.addAction(self.arrow_action)

        # Double Arrow Connector Tool Action
        self.double_arrow_action = QAction(
            QIcon("icons/double-arrow.svg"), "Double Arrow Connector Tool", self
        )
        self.double_arrow_action.setCheckable(True)
        self.double_arrow_action.triggered.connect(
            lambda: self.set_tool("double_arrow_connector")
        )
        self.addAction(self.double_arrow_action)

        # Line Connector Tool Action
        self.line_action = QAction(QIcon("icons/line.svg"), "Line Connector Tool", self)
        self.line_action.setCheckable(True)
        self.line_action.triggered.connect(lambda: self.set_tool("line_connector"))
        self.addAction(self.line_action)

        # Text Selection Tool Action
        self.text_action = QAction(QIcon("icons/text.svg"), "Text Tool", self)
        self.text_action.setCheckable(True)
        self.text_action.triggered.connect(lambda: self.set_tool("text"))
        self.addAction(self.text_action)

        # Selection Tool Action
        self.select_action = QAction(QIcon("icons/select.svg"), "Selection Tool", self)
        self.select_action.setCheckable(True)
        self.select_action.triggered.connect(lambda: self.set_tool("select"))
        self.addAction(self.select_action)

        # Add the eraser tool button
        self.eraser_action = QAction(QIcon("icons/eraser.svg"), "Eraser Tool", self)
        self.eraser_action.setCheckable(True)
        self.eraser_action.triggered.connect(lambda: self.set_tool("eraser"))
        self.addAction(self.eraser_action)

        # Group actions so only one can be checked at a time
        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)
        self.action_group.addAction(self.rect_action)
        self.action_group.addAction(self.oval_action)
        self.action_group.addAction(self.diamond_action)
        self.action_group.addAction(self.triangle_action)
        self.action_group.addAction(self.arrow_action)
        self.action_group.addAction(self.double_arrow_action)
        self.action_group.addAction(self.line_action)
        self.action_group.addAction(self.text_action)
        self.action_group.addAction(self.select_action)
        self.action_group.addAction(self.eraser_action)

    def set_tool(self, tool_name):
        """This method will set the active tool in the diagram canvas."""
        # Retrieve DiagramCanvas from parent and set tool
        canvas = self.parent().findChild(DiagramCanvas)
        if canvas:
            canvas.set_tool(tool_name)

    def select_tool(self, tool_name):
        """Programmatically select a tool."""
        action_map = {
            "rect": self.rect_action,
            "oval": self.oval_action,
            "diamond": self.diamond_action,
            "triangle": self.triangle_action,
            "arrow_connector": self.arrow_action,
            "line_connector": self.line_action,
            "text": self.text_action,
            "select": self.select_action,
            "eraser": self.eraser_action,
        }
        action = action_map.get(tool_name)
        if action:
            action.setChecked(True)
            self.set_tool(tool_name)
