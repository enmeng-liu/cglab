import collections
import logging

from MyItem import MyItem
from Operation import DrawItem, EditItem, MoveCenter, DeleteItem, DrawingPolygon, DrawingCurve

status_operation_map = {
    'line': DrawItem,
    'polygon': DrawItem,
    'ellipse': DrawItem,
    'curve': DrawItem,
    'copy': DrawItem,
    'translate': EditItem,
    'scale': EditItem,
    'rotate': EditItem,
    'clip': EditItem,
    'clip_polygon': EditItem,
    'rotate_move_center': MoveCenter,
    'delete': DeleteItem,
    'drawing_polygon': DrawingPolygon,
    'drawing_curve': DrawingCurve,
}


class OperationList:
    """
    备忘录类
    """
    def __init__(self):
        self.op_list = collections.deque()

    def add_operation(self, status: str, item: MyItem):
        try:
            operation = status_operation_map[status](item)
        except KeyError:
            logging.error('No such operation.')
            return
        self.op_list.append(operation)
        logging.debug('add operation: %s' % operation)

    def undo(self):
        if len(self.op_list) == 0:
            raise ValueError('empty op_list')
        last_operation = self.op_list.pop()

        # 曲线和多边形特殊处理
        if isinstance(last_operation, DrawItem):
            while self.op_list and isinstance(self.op_list[-1], DrawingCurve):
                self.op_list.pop()
            while self.op_list and isinstance(self.op_list[-1], DrawingPolygon):
                self.op_list.pop()

        return last_operation.undo()