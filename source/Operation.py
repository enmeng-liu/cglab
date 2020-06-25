from MyCanvas import MyCanvas
from MyItem import MyItem


class Operation:
    def __init__(self, item: MyItem, canvas: MyCanvas):
        self.item = item
        self.canvas = canvas

    def mouse_move(self):
        pass

    def mouse_press(self):
        pass

    def mouse_release(self):
        pass

    def finish(self):
        pass

    def restore(self):
        """
        撤销该步操作
        """
        pass


class DrawItem(Operation):
    def restore(self):
        item_to_delete = self.item
        del self.canvas.item_dict[item_to_delete.id]
        if self.canvas.selected_id == item_to_delete.id:
            self.canvas.selected_id = ''
            self.canvas.main_window.list_widget.setCurrentItem(None)
        if self.canvas.temp_item == item_to_delete:
            self.canvas.temp_item = None
        self.canvas.scene().removeItem(item_to_delete)
        self.canvas.updateScene([self.canvas.sceneRect()])
        self.canvas.main_window.list_widget.takeItem(self.canvas.main_window.list_widget.row(item_to_delete.list_item))
        self.canvas.status = 'deleted'