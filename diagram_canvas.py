from PyQt5.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsPolygonItem,
)
from PyQt5.QtGui import QCursor, QPainter, QBrush, QPen, QPolygonF
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF, QLineF

from rectangle_table import RectItem
from oval_attribute import OvalItem
from triangle_special_generalization import TriangleItem
from diamond_relationship import DiamondItem
from er_diagram import ErDiagramItem
from diagram_connector import (
    DiagramConnector,
)
from arrow_connector import ArrowConnector
from line_connector import LineConnector
from double_arrow_connector import DoubleArrowConnector


class DiagramCanvas(QGraphicsView):
    def __init__(self, scene=None, parent=None):
        if scene is None:
            scene = QGraphicsScene()
        scene.setSceneRect(0, 0, 800, 600)
        super().__init__(scene, parent)

        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.current_tool = None
        self.current_item = None
        self.selection_box = None
        self.selection_start = None

        self.connector_start_item = None
        self.connector_preview = None

        self.setScene(scene)
        self.scene().selectionChanged.connect(self.handle_selection_change)

    def set_tool(self, tool):
        if self.current_tool == "select":
            self.exit_text_editing()
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

    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())

        if event.button() == Qt.LeftButton:
            if self.current_tool in {"rect", "oval", "triangle", "diamond"}:
                self.exit_text_editing()
                self.scene().clearSelection()

                item = self.itemAt(event.pos())
                if item and isinstance(item, ErDiagramItem):
                    super().mousePressEvent(event)
                    if self.current_tool == "select":
                        if not item.isSelected():
                            self.scene().clearSelection()
                            item.setSelected(True)
                        item.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
                        item.text_item.setFocus()
                else:
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
                start_item = self.itemAt(event.pos())
                if isinstance(start_item, ErDiagramItem):
                    # Create the connector and set the start item and start position
                    self.connector_preview = self.create_connector(
                        start_item, start_item.pos()
                    )
                    self.connector_preview.start_item = start_item  # Set the start item
                    self.connector_preview.setZValue(
                        -1
                    )  # Lower the Z-value of the connector preview
                    self.scene().addItem(self.connector_preview)
                else:
                    # Allow starting from any point on the scene
                    self.connector_preview = self.create_connector(None, pos)
                    self.connector_preview.start_pos = pos
                    self.connector_preview.setZValue(
                        -1
                    )  # Lower the Z-value of the connector preview
                    self.scene().addItem(self.connector_preview)

            elif self.current_tool == "select":
                item = self.itemAt(event.pos())
                if item and isinstance(item, ErDiagramItem):
                    if not item.isSelected():
                        self.scene().clearSelection()
                        item.setSelected(True)
                    item.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
                    item.text_item.setFocus()
                else:
                    self.selection_start = pos
                    self.selection_box = QGraphicsRectItem(
                        QRectF(self.selection_start, QSizeF(0, 0))
                    )
                    self.selection_box.setPen(QPen(Qt.blue, 2, Qt.DashLine))
                    self.selection_box.setBrush(QBrush(Qt.NoBrush))
                    self.scene().addItem(self.selection_box)

            else:
                super().mousePressEvent(event)

    def find_item_near_pos(self, pos):
        """Find an item near the given position."""
        items = self.scene().items(QRectF(pos - QPointF(5, 5), QSizeF(10, 10)))
        for item in items:
            if isinstance(item, ErDiagramItem):
                return item
        return None

    def mouseReleaseEvent(self, event):
        pos = self.mapToScene(event.pos())

        if self.current_tool == "select" and self.selection_box:
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
                end_item = self.find_item_near_pos(pos)
                print(f"Mouse release at position: {pos}")
                print(f"Item near mouse: {end_item}")

                if isinstance(end_item, ErDiagramItem):
                    self.connector_preview.set_end_item(end_item)
                    self.connector_preview.finalize(end_item.pos())
                else:
                    self.connector_preview.set_end_pos(pos)
                    self.connector_preview.finalize(pos)

                print(f"Start item after release: {self.connector_preview.start_item}")
                print(f"End item after release: {self.connector_preview.end_item}")

                self.connector_preview = None

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.current_tool == "select" and self.selection_start:
            if self.selection_box:
                selection_end = self.mapToScene(event.pos())
                rect = QRectF(self.selection_start, selection_end).normalized()
                self.selection_box.setRect(rect)

        if self.current_tool in {
            "line_connector",
            "arrow_connector",
            "double_arrow_connector",
        }:
            if self.connector_preview:
                # Update the end position of the preview connector to follow the mouse
                end_pos = self.mapToScene(event.pos())
                self.connector_preview.set_end_pos(end_pos)

        # Prevent moving items when a connector tool is selected
        if self.current_tool not in {
            "arrow_connector",
            "line_connector",
            "double_arrow_connector",
        }:
            super().mouseMoveEvent(event)

    def create_connector(self, start_pos, end_pos):
        if self.current_tool == "arrow_connector":
            return ArrowConnector(start_pos, end_pos)
        elif self.current_tool == "line_connector":
            return LineConnector(start_pos, end_pos)
        elif self.current_tool == "double_arrow_connector":
            return DoubleArrowConnector(start_pos, end_pos)

    def handle_selection_change(self):
        selected_items = self.scene().selectedItems()
        if not selected_items:
            print("No items selected.")
            return

        for item in selected_items:
            print(f"Selected item: {item}")

            if hasattr(item, "setBrush"):
                item.setBrush(QBrush(Qt.NoBrush))

    def exit_text_editing(self):
        for item in self.scene().items():
            if isinstance(item, ErDiagramItem):
                item.clear_text_editing()

    def mouseDoubleClickEvent(self, event):
        pos = self.mapToScene(event.pos())
        item = self.itemAt(event.pos())

        if item and isinstance(item, ErDiagramItem):
            self.exit_text_editing()
            item.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
            item.text_item.setFlag(QGraphicsItem.ItemIsFocusable)
            item.text_item.setFocus()

            self.set_tool("select")
            self.update_cursor()
        else:
            super().mouseDoubleClickEvent(event)
