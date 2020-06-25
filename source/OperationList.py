import collections
from MyItem import MyItem


class OperationList:
    """
    备忘录类
    """
    def __init__(self):
        self.op_list = collections.deque()

    def add_memo(self):
        pass

    def add_draw_memo(self, item: MyItem):
        pass

    def add_translate_memo(self, item_id, deltax, deltay):
        pass

    def add_rotate_memo(self, item_id, radian):
        pass

    def add_scale_memo(self, s):
        pass

    def restore(self):
        pass