from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsItem
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtCore import Qt, QPointF, QLineF
from diagram_connector import DiagramConnector
import math


class ArrowConnector(DiagramConnector):
    def __init__(self, start_pos=None, end_pos=None, parent=None):
        super().__init__(start_pos, end_pos, parent)
        self.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        self.arrow_head = None
        self.update_arrow(end_pos)

    def update_arrow(self, end_pos):
        """Update the line and the arrowhead."""
        self.end_pos = end_pos
        self.setLine(QLineF(self.start_pos, self.end_pos))
        self.add_arrowhead()

    def add_arrowhead(self):
        arrow_size = 10
        if self.arrow_head is not None:
            self.scene().removeItem(self.arrow_head)

        line = self.line()
        # angle = line.angle()
        angle = math.atan2(line.dy(), line.dx())

        # Calculate the arrowhead points based on the line angle
        p1 = self.line().p2() + QPointF(
            -arrow_size * math.cos(angle - math.pi / 6),
            -arrow_size * math.sin(angle - math.pi / 6),
        )
        p2 = self.line().p2() + QPointF(
            -arrow_size * math.cos(angle + math.pi / 6),
            -arrow_size * math.sin(angle + math.pi / 6),
        )

        arrow_head = QPolygonF([p1, p2, self.line().p2()])
        arrow_head = QGraphicsPolygonItem(arrow_head)
        arrow_head.setPen(self.pen())
        arrow_head.setBrush(self.pen().color())

        # Add the arrowhead to the scene, but only if the connector is part of the scene
        if self.scene() is not None:
            self.arrow_head = arrow_head
            self.scene().addItem(self.arrow_head)

    def removeItem(self):
        if self.arrow_head:
            self.scene().removeItem(self.arrow_head)
            self.arrow_head = None
        self.scene().removeItem(self)

    def itemChange(self, change, value):
        """Override itemChange to handle removal of the connector."""
        if change == QGraphicsItem.ItemSceneHasChanged and self.scene() is None:
            # This means the item is being removed from the scene
            if self.arrow_head:
                self.scene().removeItem(self.arrow_head)
        return super().itemChange(change, value)

    def finalize(self, end_pos):
        super().finalize(end_pos)
        self.add_arrowhead()
