from PyQt5.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsTextItem,
)
from PyQt5.QtGui import QCursor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF

from rectangle_table import RectItem
from oval_attribute import OvalItem
from triangle_special_generalization import TriangleItem
from diamond_relationship import DiamondItem
from er_diagram import ErDiagramItem


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

        self.setScene(scene)  # Ensure the scene is set correctly
        self.scene().selectionChanged.connect(self.handle_selection_change)

    def set_tool(self, tool):
        if self.current_tool == "select":
            self.exit_text_editing()  # Exit text editing mode for the previous item
        self.current_tool = tool
        self.update_cursor()

    def update_cursor(self):
        if self.current_tool in {"rect", "oval", "triangle", "diamond"}:
            self.setCursor(QCursor(Qt.CrossCursor))
        elif self.current_tool == "select":
            self.setCursor(QCursor(Qt.ArrowCursor))

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

        # Call the base class implementation to ensure default behavior
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
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

        # Call the base class implementation to ensure default behavior
        super().mouseReleaseEvent(event)

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
        super().mouseDoubleClickEvent(event)
        pos = self.mapToScene(event.pos())
        item = self.itemAt(event.pos())

        if item and isinstance(item, ErDiagramItem):
            # Exit text editing mode for all other items
            self.exit_text_editing()

            # Enable text editing for the double-clicked item
            item.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
            item.text_item.setFlag(QGraphicsItem.ItemIsFocusable)
            item.text_item.setFocus()
