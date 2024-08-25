from PyQt5.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsTextItem,
)
from PyQt5.QtGui import QCursor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF, QLineF

from rectangle_table import RectItem
from oval_attribute import OvalItem
from triangle_special_generalization import TriangleItem
from diamond_relationship import DiamondItem
from er_diagram import ErDiagramItem
from diagram_connector import (
    DiagramConnector,
)  # Make sure this is the correct import path
from arrow_connector import ArrowConnector
from line_connector import LineConnector
from double_arrow_connector import DoubleArrowConnector


class DiagramCanvas(QGraphicsView):
    def __init__(self, scene=None, parent=None):
        if scene is None:
            scene = QGraphicsScene()
        scene.setSceneRect(0, 0, 800, 600)  # Adjust dimensions as needed
        super().__init__(scene, parent)

        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.current_tool = None
        self.current_item = None
        self.selection_box = None  # To hold the temporary selection box
        self.selection_start = None  # Start point for selection box

        self.connector_start_item = None  # Start item for connectors
        self.connector_preview = None  # Preview line for connectors

        self.setScene(scene)  # Ensure the scene is set correctly
        self.scene().selectionChanged.connect(self.handle_selection_change)

    def set_tool(self, tool):
        if self.current_tool == "select":
            self.exit_text_editing()  # Exit text editing mode for the previous item
        self.current_tool = tool
        self.update_cursor()

    def update_cursor(self):
        if self.current_tool in {
            "rect",
            "oval",
            "triangle",
            "diamond",
            "arrow_connector",
            "line_connector",
            "double_arrow_connector",
        }:
            self.setCursor(QCursor(Qt.CrossCursor))
        elif self.current_tool == "select":
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.current_tool in {"arrow_connector", "line_connector"}:
            self.setCursor(QCursor(Qt.CrossCursor))

    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())

        if event.button() == Qt.LeftButton:
            if self.current_tool in {"rect", "oval", "triangle", "diamond"}:
                # Handle item creation or text editing
                self.exit_text_editing()
                self.scene().clearSelection()

                item = self.itemAt(event.pos())
                if item and isinstance(item, ErDiagramItem):
                    # Clicked on an existing item: Select and enter text edit mode
                    if self.current_tool == "select":
                        if not item.isSelected():
                            self.scene().clearSelection()
                            item.setSelected(True)
                        item.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
                        item.text_item.setFocus()
                else:
                    # Create a new item
                    if self.current_tool == "rect":
                        self.current_item = RectItem(pos.x(), pos.y(), 0, 0)
                    elif self.current_tool == "oval":
                        self.current_item = OvalItem(pos.x(), pos.y(), 0, 0)
                    elif self.current_tool == "triangle":
                        self.current_item = TriangleItem(pos.x(), pos.y(), 50, 50)
                    elif self.current_tool == "diamond":
                        self.current_item = DiamondItem(pos.x(), pos.y(), 50, 50)

                    if self.current_item:
                        self.scene().addItem(self.current_item)
                        self.current_item = None

            elif self.current_tool in {
                "arrow_connector",
                "line_connector",
                "double_arrow_connector",
            }:
                # Handle connector creation
                item = self.itemAt(event.pos())
                if isinstance(item, ErDiagramItem):
                    # Start a connector from an existing item
                    self.connector_start_item = item
                    self.connector_preview = self.create_connector_preview(pos, pos)
                    self.scene().addItem(self.connector_preview)
                else:
                    # Start a connector in empty space
                    self.connector_start_item = None
                    self.connector_preview = self.create_connector_preview(pos, pos)
                    self.scene().addItem(self.connector_preview)

            elif self.current_tool == "select":
                # Handle selection and text editing
                item = self.itemAt(event.pos())
                if item and isinstance(item, ErDiagramItem):
                    if not item.isSelected():
                        self.scene().clearSelection()
                        item.setSelected(True)
                    item.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
                    item.text_item.setFocus()
                else:
                    # Start the selection box for multi-selection
                    self.selection_start = pos
                    self.selection_box = QGraphicsRectItem(
                        QRectF(self.selection_start, QSizeF(0, 0))
                    )
                    self.selection_box.setPen(QPen(Qt.blue, 2, Qt.DashLine))
                    self.selection_box.setBrush(QBrush(Qt.NoBrush))
                    self.scene().addItem(self.selection_box)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.current_tool == "select" and self.selection_start:
            if self.selection_box:
                # Update the selection box as the mouse moves
                selection_end = self.mapToScene(event.pos())
                rect = QRectF(self.selection_start, selection_end).normalized()
                self.selection_box.setRect(rect)

        if self.current_tool in {
            "line_connector",
            "arrow_connector",
            "double_arrow_connector",
        }:
            if self.connector_preview:
                start_pos = self.connector_preview.line().p1()
                end_pos = self.mapToScene(event.pos())

                # Ensure both start_pos and end_pos are QPointF
                if isinstance(start_pos, QPointF) and isinstance(end_pos, QPointF):
                    # Create a QLineF with these points
                    new_line = QLineF(start_pos, end_pos)
                    self.connector_preview.setLine(new_line)
                else:
                    # Handle conversion or error
                    print("Error: start_pos or end_pos is not of type QPointF")

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        pos = self.mapToScene(event.pos())

        if self.current_tool == "select" and self.selection_box:
            # Select items within the selection box
            rect = self.selection_box.rect()
            items = self.scene().items(rect)
            self.scene().clearSelection()
            for item in items:
                if isinstance(item, ErDiagramItem):
                    item.setSelected(True)
            self.scene().removeItem(self.selection_box)
            self.selection_box = None

        elif self.current_tool in {
            "arrow_connector",
            "line_connector",
            "double_arrow_connector",
        }:
            if self.connector_preview:
                # Finalize the connector creation
                start_pos = self.connector_preview.line().p1()
                end_pos = pos
                end_item = self.itemAt(event.pos())

                if isinstance(end_item, ErDiagramItem):
                    connector = self.create_connector(start_pos, end_pos, end_item)
                    self.scene().addItem(connector)
                    if self.connector_start_item:
                        connector.set_start_item(self.connector_start_item)
                    connector.set_end_item(end_item)
                else:
                    # Just a visual line, no connections
                    connector = self.create_connector(start_pos, end_pos)
                    self.scene().addItem(connector)

                # Apply styles based on the type of connector
                if self.current_tool == "line_connector":
                    pen = QPen(Qt.black, 2, Qt.SolidLine)
                    connector.setPen(pen)
                elif self.current_tool == "arrow_connector":
                    pen = QPen(Qt.black, 2, Qt.SolidLine)
                    connector.setPen(pen)
                    self.add_arrowhead(start_pos, end_pos, connector)
                elif self.current_tool == "double_arrow_connector":
                    pen = QPen(Qt.black, 2, Qt.SolidLine)
                    connector.setPen(pen)
                    self.add_arrowhead(start_pos, end_pos, connector)
                    self.add_arrowhead(end_pos, start_pos, connector)

                # Clean up the preview and exit drawing mode
                self.scene().removeItem(self.connector_preview)
                self.connector_preview = None
                self.connector_start_item = None
                self.current_tool = None  # Exit drawing mode

        # Call the base class implementation to ensure default behavior
        super().mouseReleaseEvent(event)

    def add_arrowhead(self, start_pos, end_pos, line_item):
        arrow_size = 10
        line = QLineF(start_pos, end_pos)

        angle = line.angle()

        p1 = end_pos + QPointF(arrow_size * -1, arrow_size / 2)
        p2 = end_pos + QPointF(arrow_size * -1, arrow_size / -2)

        arrow_head = QPolygonF([p1, p2, end_pos])

        arrow_item = QGraphicsPolygonItem(arrow_head)
        arrow_item.setPen(line_item.pen())
        arrow_item.setBrush(line_item.pen().color())

        self.scene().addItem(arrow_item)


    def create_connector(self, start_pos, end_pos, end_item=None):
        if self.current_tool == "arrow_connector":
            return ArrowConnector(start_pos, end_pos, end_item)
        elif self.current_tool == "line_connector":
            return LineConnector(start_pos, end_pos, end_item)
        elif self.current_tool == "double_arrow_connector":
            return DoubleArrowConnector(start_pos, end_pos, end_item)

    def create_connector_preview(self, start_pos, end_pos):
        # Create a preview line item to show the user where the connector will be drawn
        pen = QPen(Qt.black, 2, Qt.DashLine)
        preview_line = self.scene().addLine(
            start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y(), pen
        )
        return preview_line

    def handle_selection_change(self):
        selected_items = self.scene().selectedItems()
        if not selected_items:
            print("No items selected.")
            return

        for item in selected_items:
            print(f"Selected item: {item}")

            # Ensure no brush for selection
            if hasattr(item, "setBrush"):
                item.setBrush(QBrush(Qt.NoBrush))

    def exit_text_editing(self):
        # Exit text editing for all items in the scene
        for item in self.scene().items():
            if isinstance(item, ErDiagramItem):
                item.clear_text_editing()

    def mouseDoubleClickEvent(self, event):
        pos = self.mapToScene(event.pos())
        item = self.itemAt(event.pos())

        if item and isinstance(item, ErDiagramItem):
            # Exit text editing mode for all other items
            self.exit_text_editing()

            # Enable text editing for the double-clicked item
            item.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
            item.text_item.setFlag(QGraphicsItem.ItemIsFocusable)
            item.text_item.setFocus()

            # Switch to selection tool
            self.set_tool("select")
            self.update_cursor()
        else:
            super().mouseDoubleClickEvent(event)
