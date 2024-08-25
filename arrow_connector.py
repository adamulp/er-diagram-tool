from PyQt5.QtWidgets import QGraphicsPolygonItem
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtCore import QPointF, QLineF
from diagram_connector import DiagramConnector


class ArrowConnector(DiagramConnector):
    def __init__(self, start_pos=None, end_pos=None, parent=None):
        super().__init__(start_pos, end_pos, parent)

    def add_arrowhead(self):
        arrow_size = 10
        angle = self.line().angle()

        p1 = self.line().p2() + QPointF(arrow_size * -1, arrow_size / 2)
        p2 = self.line().p2() + QPointF(arrow_size * -1, arrow_size / -2)

        arrow_head = QPolygonF([p1, p2, self.line().p2()])

        arrow_item = QGraphicsPolygonItem(arrow_head)
        arrow_item.setPen(self.pen())
        arrow_item.setBrush(self.pen().color())

        self.scene().addItem(arrow_item)

    def finalize(self, end_pos):
        super().finalize(end_pos)
        self.add_arrowhead()
