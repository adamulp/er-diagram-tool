from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import QRectF, Qt
from er_diagram import ErDiagramItem


class OvalItem(QGraphicsEllipseItem, ErDiagramItem):
    def __init__(self, x, y, width, height):
        # Initialize the ellipse item and the ER diagram item
        QGraphicsEllipseItem.__init__(self, QRectF(x, y, width, height))
        ErDiagramItem.__init__(self)

        # Set brush and pen for the ellipse
        self.setBrush(QBrush(Qt.lightGray))
        self.setPen(QPen(Qt.black))

        # Set the position of the item
        self.setPos(x, y)

        # Initial size update to adjust text and shape
        self.update_size()

    def update_size(self):
        # Call the parent class's update_size method to get text rect and base size logic
        text_rect = self.text_item.boundingRect()

        # Expand the width more than the height to preserve the oval shape
        width = max(120, text_rect.width() + 40)  # Increased width expansion
        height = max(60, text_rect.height() + 20)  # Less height expansion

        # Set the outer bounding rectangle of the ellipse
        self.setRect(QRectF(0, 0, width, height))

        # Calculate the inner bounding rectangle by considering the oval's aspect ratio
        inner_margin_width = 20
        inner_margin_height = 10
        inner_rect = QRectF(
            inner_margin_width,
            inner_margin_height,
            width - 2 * inner_margin_width,
            height - 2 * inner_margin_height,
        )

        # Adjust the text width to fit inside the inner rectangle
        self.text_item.setTextWidth(inner_rect.width())

        # Position the text within the inner bounding rectangle, centered
        self.text_item.setPos(
            inner_rect.left() + (inner_rect.width() - text_rect.width()) / 2,
            inner_rect.top() + (inner_rect.height() - text_rect.height()) / 2,
        )
