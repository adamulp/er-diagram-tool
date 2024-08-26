from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtCore import Qt, QPointF, QLineF
from diagram_connector import DiagramConnector
import math


class DoubleArrowConnector(DiagramConnector):
    def __init__(self, start_pos=None, end_pos=None, parent=None):
        super().__init__(start_pos, end_pos, parent)
        self.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        self.arrow_head_start = None
        self.arrow_head_end = None
        self.update_arrows(end_pos)

    def update_arrows(self, end_pos):
        """Update the line and both arrowheads."""
        self.end_pos = end_pos
        self.setLine(QLineF(self.start_pos, self.end_pos))
        self.add_arrowheads()

    def add_arrowheads(self):
        arrow_size = 10

        # Remove existing arrowheads if they exist
        if self.arrow_head_start:
            self.scene().removeItem(self.arrow_head_start)
        if self.arrow_head_end:
            self.scene().removeItem(self.arrow_head_end)

        line = self.line()
        angle_start = math.atan2(-line.dy(), -line.dx())
        angle_end = math.atan2(line.dy(), line.dx())

        # Calculate the points for the start arrowhead
        p1_start = self.line().p1() + QPointF(
            -arrow_size * math.cos(angle_start - math.pi / 6),
            -arrow_size * math.sin(angle_start - math.pi / 6),
        )
        p2_start = self.line().p1() + QPointF(
            -arrow_size * math.cos(angle_start + math.pi / 6),
            -arrow_size * math.sin(angle_start + math.pi / 6),
        )

        arrow_head_start = QPolygonF([p1_start, p2_start, self.line().p1()])
        self.arrow_head_start = QGraphicsPolygonItem(arrow_head_start)
        self.arrow_head_start.setPen(self.pen())
        self.arrow_head_start.setBrush(self.pen().color())

        # Calculate the points for the end arrowhead
        p1_end = self.line().p2() + QPointF(
            -arrow_size * math.cos(angle_end - math.pi / 6),
            -arrow_size * math.sin(angle_end - math.pi / 6),
        )
        p2_end = self.line().p2() + QPointF(
            -arrow_size * math.cos(angle_end + math.pi / 6),
            -arrow_size * math.sin(angle_end + math.pi / 6),
        )

        arrow_head_end = QPolygonF([p1_end, p2_end, self.line().p2()])
        self.arrow_head_end = QGraphicsPolygonItem(arrow_head_end)
        self.arrow_head_end.setPen(self.pen())
        self.arrow_head_end.setBrush(self.pen().color())

        # Add the arrowheads to the scene, but only if the connector is part of the scene
        if self.scene() is not None:
            self.scene().addItem(self.arrow_head_start)
            self.scene().addItem(self.arrow_head_end)

    def removeItem(self):
        """Ensure both the connector and its arrowheads are removed."""
        if self.arrow_head_start:
            self.scene().removeItem(self.arrow_head_start)
        if self.arrow_head_end:
            self.scene().removeItem(self.arrow_head_end)
        self.scene().removeItem(self)

    def finalize(self, end_pos):
        super().finalize(end_pos)
        self.add_arrowheads()
