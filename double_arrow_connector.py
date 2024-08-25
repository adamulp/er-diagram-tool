from PyQt5.QtWidgets import QGraphicsPolygonItem
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtCore import QPointF, QLineF
from diagram_connector import DiagramConnector
import math


class DoubleArrowConnector(DiagramConnector):
    def __init__(self, start_pos=None, end_pos=None, parent=None):
        super().__init__(start_pos, end_pos, parent)

    def add_double_arrowheads(self):
        """Add arrowheads at both ends of the connector."""
        self.add_arrowhead(self.line().p1(), self.line().p2())
        self.add_arrowhead(self.line().p2(), self.line().p1())

    def add_arrowhead(self, start_pos, end_pos):
        """Helper method to add an arrowhead pointing from start_pos to end_pos."""
        arrow_size = 10
        angle = math.atan2(end_pos.y() - start_pos.y(), end_pos.x() - start_pos.x())

        # Calculate the two points of the base of the arrowhead
        p1 = end_pos + QPointF(
            -arrow_size * math.cos(angle - math.pi / 6),
            -arrow_size * math.sin(angle - math.pi / 6),
        )
        p2 = end_pos + QPointF(
            -arrow_size * math.cos(angle + math.pi / 6),
            -arrow_size * math.sin(angle + math.pi / 6),
        )

        arrow_head = QPolygonF([p1, p2, end_pos])

        arrow_item = QGraphicsPolygonItem(arrow_head)
        arrow_item.setPen(self.pen())
        arrow_item.setBrush(self.pen().color())

        self.scene().addItem(arrow_item)

    def finalize(self, end_pos):
        super().finalize(end_pos)
        self.add_double_arrowheads()
