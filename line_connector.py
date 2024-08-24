from diagram_connector import DiagramConnector


class LineConnector(DiagramConnector):
    def __init__(self, start_item, end_item, parent=None):
        super().__init__(start_item, end_item, parent)

    def update_position(self):
        super().update_position()
        # No additional features needed for a simple line connector
