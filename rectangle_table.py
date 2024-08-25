from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF, QLineF
from er_diagram import ErDiagramItem


class RectItem(QGraphicsRectItem, ErDiagramItem):
    def __init__(self, x, y, width, height):
        # Initialize both parent classes
        QGraphicsRectItem.__init__(self)
        ErDiagramItem.__init__(self)

        # Initialize the QGraphicsRectItem with the provided dimensions
        self.setRect(QRectF(0, 0, width, height))

        # Set additional properties
        self.setBrush(QBrush(Qt.lightGray))
        self.setPen(QPen(Qt.black))
        self.setPos(x, y)
        self.update_size()

    def update_size(self):
        ErDiagramItem().update_size()
        if hasattr(self, "text_item") and self.text_item is not None:
            text_rect = self.text_item.boundingRect()
            rect = QRectF(
                0, 0, max(100, text_rect.width() + 10), max(60, text_rect.height() + 10)
            )
            self.setRect(rect)
            self.text_item.setPos(5, 5)

    def find_intersection_with_rectangle(rect, line):
        """Find the intersection point of a line with a rectangle's perimeter."""
        edges = [
            QLineF(rect.topLeft(), rect.topRight()),  # Top edge
            QLineF(rect.topRight(), rect.bottomRight()),  # Right edge
            QLineF(rect.bottomRight(), rect.bottomLeft()),  # Bottom edge
            QLineF(rect.bottomLeft(), rect.topLeft()),  # Left edge
        ]

        intersect_point = QPointF()
        for edge in edges:
            if line.intersect(edge, intersect_point) == QLineF.BoundedIntersection:
                return intersect_point

        return line.p2()  # Default to the end point if no intersection
