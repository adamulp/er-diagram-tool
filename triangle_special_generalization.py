from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QPolygonF, QBrush, QPen
from PyQt5.QtCore import QRectF, QPointF, Qt
from er_diagram import ErDiagramItem


class TriangleItem(ErDiagramItem):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.setPos(x, y)

        self.pen = QPen(Qt.black)
        self.brush = QBrush(Qt.lightGray)

        self.text_item.setPos(x + 5, y + 5)
        self.update_size()

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget):
        # Inverted points for the triangle
        points = [
            QPointF(0, 0),  # Bottom-left corner
            QPointF(self.width / 2, self.height),  # Top-middle point
            QPointF(self.width, 0),  # Bottom-right corner
        ]

        triangle = QPolygonF(points)

        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPolygon(triangle)

        self.paint_selection(painter)

    def update_size(self):
        ErDiagramItem().update_size()
        text_rect = self.text_item.boundingRect()

        self.width = max(self.width, text_rect.width() + 10)
        self.height = max(self.height, text_rect.height() + 10)

        self.prepareGeometryChange()
        self.text_item.setPos(5, 5)

    def paint_selection(self, painter):
        if self.isSelected():
            pen = QPen(Qt.blue, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)  # Transparent fill
            painter.drawRect(self.boundingRect())
