import logging
from copy import deepcopy

from MyItem import MyItem


class Operation:
    def __init__(self, item: MyItem):
        self.item = item

    def mouse_move(self):
        pass

    def mouse_press(self):
        pass

    def mouse_release(self):
        pass

    def finish(self):
        pass

    def undo(self):
        """
        撤销该步操作
        """
        pass


class DrawItem(Operation):
    def __str__(self):
        return 'DrawItem: %s' % self.item

    def undo(self):
        logging.debug('Undo and delete %s' % self.item)
        return 'delete', self.item


class EditItem(Operation):
    def __init__(self, item: MyItem):
        super().__init__(item)
        self.old_p_list = deepcopy(item.p_list)

    def __str__(self):
        return 'EditItem old_p_list={}'.format(self.old_p_list)

    def undo(self):
        logging.debug('Undo {} to old p_list={}'.format(self.item, self.old_p_list))
        self.item.p_list = self.old_p_list
        return 'undo', self.item


class MoveCenter(Operation):
    def __init__(self, item):
        super().__init__(item)
        self.old_center = self.item.center

    def __str__(self):
        return 'MoveCenter old center={}'.format(self.old_center)

    def undo(self):
        logging.debug('Undo {} to old center={}'.format(self.item, self.old_center))
        self.item.center = self.old_center
        return 'undo', self.item


class DeleteItem(Operation):
    def __str__(self):
        return 'DeleteItem %s' % self.item

    def undo(self):
        logging.debug('Undo and restore {}'.format(self.item))
        return 'restore', self.item


class DrawingPolygon(Operation):
    def __str__(self):
        return 'DrawingPolygon: %s' % self.item

    def undo(self):
        logging.debug('Undo drawing polygon line {}'.format(self.item))
        return 'drawing_polygon', self.item


class DrawingCurve(Operation):
    def __str__(self):
        return 'DrawingCurve: %s' % self.item

    def undo(self):
        self.item.p_list.pop()
        logging.debug('Undo drawing curve.')
        return 'undo', self.item