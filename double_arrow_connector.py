from PyQt5.QtWidgets import QGraphicsPolygonItem
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtCore import QPointF, QLineF
from diagram_connector import DiagramConnector


class DoubleArrowConnector(DiagramConnector):
    def __init__(self, start_pos=None, end_pos=None, parent=None):
        super().__init__(start_pos, end_pos, parent)

    def add_double_arrowheads(self):
        """Add arrowheads at both ends of the connector."""
        self.add_arrowhead(self.line().p1(), self.line().p2())
        self.add_arrowhead(self.line().p2(), self.line().p1())

    def finalize(self, end_pos):
        super().finalize(end_pos)
        self.add_double_arrowheads()

    def add_arrowhead(self, start_pos, end_pos):
        """Helper method to add an arrowhead."""
        arrow_size = 10
        angle = QLineF(start_pos, end_pos).angle()

        p1 = end_pos + QPointF(arrow_size * -1, arrow_size / 2)
        p2 = end_pos + QPointF(arrow_size * -1, arrow_size / -2)

        arrow_head = QPolygonF([p1, p2, end_pos])

        arrow_item = QGraphicsPolygonItem(arrow_head)
        arrow_item.setPen(self.pen())
        arrow_item.setBrush(self.pen().color())

        self.scene().addItem(arrow_item)
