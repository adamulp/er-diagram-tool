from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsTextItem,
    QGraphicsRectItem,
    QGraphicsEllipseItem,
    QGraphicsPolygonItem,
)
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QCursor
from PyQt5.QtCore import Qt, QRectF, QPointF


class ErDiagramItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_item = QGraphicsTextItem("", self)
        self.text_item.setTextInteractionFlags(
            Qt.TextEditorInteraction
        )  # Allow text editing
        self.text_item.setDefaultTextColor(Qt.black)

        # Set flags for item interaction
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)  # Allow movement
        self.setFlag(
            QGraphicsItem.ItemSendsGeometryChanges
        )  # Notify changes in geometry

        self.text_item.setVisible(True)  # Ensure text item is visible

        # Connect the contentsChanged signal to update the size and position
        self.text_item.document().contentsChanged.connect(self.update_size)

    def mouseDoubleClickEvent(self, event):
        self.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.text_item.setFocus()
        self.text_item.setCursor(QCursor(Qt.IBeamCursor))

        # Switch to the selection tool
        self.scene().clearSelection()  # Clear any previous selections
        self.setSelected(True)  # Select the current item

        # Access the main window and select the selection tool
        main_window = self.scene().main_window
        if main_window:
            main_window.tool_selection_bar.select_tool("select")

        super().mouseDoubleClickEvent(event)

    def set_text(self, text):
        self.text_item.setPlainText(text)
        self.update_size()

    def update_size(self):
        # Centralize size update logic based on the item type
        text_rect = self.text_item.boundingRect()
        width = max(100, text_rect.width() + 10)
        height = max(60, text_rect.height() + 10)

        if isinstance(self, QGraphicsRectItem) or isinstance(
            self, QGraphicsEllipseItem
        ):
            # For rectangles and ellipses
            self.setRect(QRectF(0, 0, width, height))

        elif isinstance(self, QGraphicsPolygonItem):
            # For polygon-based items (e.g., triangles, diamonds)
            self.update_polygon_shape(width, height)

        # Adjust the text position within the shape
        self.text_item.setPos(
            width / 2 - text_rect.width() / 2, height / 2 - text_rect.height() / 2
        )

    def update_polygon_shape(self, width, height):
        # This method will handle the shape updates for polygon items
        if hasattr(self, "shape_type") and self.shape_type == "triangle":
            self.set_triangle_shape(width, height)
        elif hasattr(self, "shape_type") and self.shape_type == "diamond":
            self.set_diamond_shape(width, height)
        # Add other shape-specific logic here if needed

    def set_triangle_shape(self, width, height):
        # Define points for a triangle (equilateral triangle centered at origin)
        points = [
            QPointF(width / 2, 0),
            QPointF(0, height),
            QPointF(width, height),
        ]
        polygon = QPolygonF(points)
        self.setPolygon(polygon)

    def set_diamond_shape(self, width, height):
        # Define points for a diamond shape
        points = [
            QPointF(width / 2, 0),
            QPointF(width, height / 2),
            QPointF(width / 2, height),
            QPointF(0, height / 2),
        ]
        polygon = QPolygonF(points)
        self.setPolygon(polygon)

    def paint_selection(self, painter):
        if self.isSelected():
            pen = QPen(Qt.blue, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)  # Transparent fill
            painter.drawRect(self.boundingRect())

    def clear_text_editing(self):
        if self.text_item.hasFocus():
            self.text_item.setTextInteractionFlags(Qt.NoTextInteraction)
            self.text_item.clearFocus()
