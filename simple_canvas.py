from PyQt5.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QApplication,
    QGraphicsTextItem,
    QGraphicsItem,
)
from PyQt5.QtGui import QCursor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF


class SimpleItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setBrush(QBrush(Qt.lightGray))

        # Add a text item inside the rectangle
        self.text_item = QGraphicsTextItem("", self)
        self.text_item.setTextInteractionFlags(Qt.NoTextInteraction)
        self.text_item.setDefaultTextColor(Qt.black)
        self.text_item.setPos(5, 5)

        # Update the item size based on the text
        self.update_size()

    def set_text(self, text):
        self.text_item.setPlainText(text)
        self.update_size()

    def update_size(self):
        text_rect = self.text_item.boundingRect()
        rect = QRectF(
            0, 0, max(100, text_rect.width() + 10), max(60, text_rect.height() + 10)
        )
        self.setRect(rect)
        self.text_item.setPos(5, 5)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.text_item.setFocus()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.text_item.setTextInteractionFlags(Qt.NoTextInteraction)


class SimpleCanvas(QGraphicsView):
    def __init__(self, scene=None, parent=None):
        if scene is None:
            scene = QGraphicsScene()
        scene.setSceneRect(0, 0, 800, 600)
        super().__init__(scene, parent)

        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setScene(scene)
        self.setup_scene()

    def setup_scene(self):
        # Add two SimpleItems for testing
        item1 = SimpleItem(100, 100, 100, 100)
        item1.set_text("Item 1")
        self.scene().addItem(item1)

        item2 = SimpleItem(300, 100, 100, 100)
        item2.set_text("Item 2")
        self.scene().addItem(item2)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print("Mouse pressed:", event.pos())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        print("Mouse moved:", event.pos())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        print("Mouse released:", event.pos())

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        print("Mouse double-clicked:", event.pos())
        pos = self.mapToScene(event.pos())
        item = self.itemAt(event.pos())
        if item and isinstance(item, SimpleItem):
            item.setFocus()
            item.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
            item.text_item.setFocus()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    view = SimpleCanvas()
    view.setWindowTitle("Simple Canvas")
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())
