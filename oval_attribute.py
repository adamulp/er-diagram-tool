from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import QRectF, Qt
from er_diagram import ErDiagramItem


class OvalItem(QGraphicsEllipseItem, ErDiagramItem):
    def __init__(self, x, y, width, height):
        super().__init__()
        QGraphicsEllipseItem.__init__(self, x, y, width, height)
        ErDiagramItem.__init__(self)
        self.setBrush(QBrush(Qt.lightGray))
        self.setPen(QPen(Qt.black))
        self.setPos(x, y)
        self.update_size()

    def update_size(self):
        super().update_size()
        text_rect = self.text_item.boundingRect()
        self.setRect(
            self.rect().x(),
            self.rect().y(),
            max(100, text_rect.width() + 10),
            max(30, text_rect.height() + 10),
        )
        self.text_item.setPos(self.rect().x() + 5, self.rect().y() + 5)
