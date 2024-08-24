from PyQt5.QtWidgets import QGraphicsPolygonItem
from PyQt5.QtGui import QBrush, QPen, QPolygonF
from PyQt5.QtCore import QPointF, Qt
from er_diagram import ErDiagramItem


class DiamondItem(QGraphicsPolygonItem, ErDiagramItem):
    def __init__(self, x, y, width, height):
        super().__init__()
        QGraphicsPolygonItem.__init__(self)
        ErDiagramItem.__init__(self)

        self.width = width
        self.height = height

        self.update_shape(x, y)
        self.setBrush(QBrush(Qt.lightGray))
        self.setPen(QPen(Qt.black))
        self.text_item.setPos(x + 5, y + 5)
        self.update_size()

    def update_shape(self, x, y):
        points = [
            QPointF(x + self.width / 2, y),
            QPointF(x + self.width, y + self.height / 2),
            QPointF(x + self.width / 2, y + self.height),
            QPointF(x, y + self.height / 2),
        ]
        polygon = QPolygonF(points)
        self.setPolygon(polygon)

    def update_size(self):
        ErDiagramItem().update_size()
        text_rect = self.text_item.boundingRect()
        self.width = max(100, text_rect.width() + 10)
        self.height = max(60, text_rect.height() + 10)

        self.update_shape(
            self.polygon().boundingRect().x(), self.polygon().boundingRect().y()
        )
        self.text_item.setPos(
            self.polygon().boundingRect().x() + 5, self.polygon().boundingRect().y() + 5
        )
