#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, logging
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QColorDialog,
    QInputDialog,
    QDialog,
    QDialogButtonBox,
    QComboBox,
    QFileDialog,
    QStyleOptionGraphicsItem)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QImage
from PyQt5.QtCore import QRectF


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.temp_pen_color = QColor(0, 0, 0)
        self.polygon_cnt = 0

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        # logging.debug('draw line with color: {}'.format(self.temp_pen_color))
    
    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        # self.polygon_cnt = 0
        self.item_dict[self.temp_id] = []
        logging.debug('start draw polygon.')

    def finish_draw(self):
        self.temp_id = self.main_window.new_id()

    def clear_selection(self):
        if self.selected_id != '':
            # self.main_window.list_widget.clearSelection()
            self.main_window.list_widget.setCurrentItem(None)
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed_from_list(self, selected):
        if selected == '':
            return
        logging.debug('select ' + selected)
        i = 0
        while selected[i].isdigit():
            i += 1
        selected_id = selected[0:i]
        logging.debug('selected id = ' + selected_id)
        self.selection_changed_by_id(selected_id)

    def selection_changed_by_id(self, selected_id):
        if selected_id == '':
            return
        # logging.debug('select ' + selected_id)
        self.main_window.statusBar().showMessage('图元选择： %s' % selected_id)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected_id
        self.item_dict[selected_id].selected = True
        self.item_dict[selected_id].update()
        self.status = ''
        self.updateScene([self.sceneRect()])    

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            # 绘制直线
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.temp_pen_color)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon':
            # 绘制多边形
            if not self.item_dict[self.temp_id]:
                self.temp_item = MyItem(self.temp_id, 'line', [[x, y], [x, y]], self.temp_algorithm, self.temp_pen_color)
            else:
                last_point = self.item_dict[self.temp_id][-1].p_list[1]
                self.temp_item = MyItem(self.temp_id, 'line', [last_point, [x, y]], self.temp_algorithm, self.temp_pen_color)
            self.scene().addItem(self.temp_item)
            self.item_dict[self.temp_id].append(self.temp_item)
            logging.debug('add point {}'.format([x,y]))
        elif self.status == '':
            # 选择图元
            selected_items = self.items(x,y)
            if len(selected_items) > 0:
                selected_id = getattr(selected_items[0], 'id')
                self.selection_changed_by_id(selected_id)
            else:
                self.main_window.statusBar().showMessage('空闲：(%d, %d)' % (x, y))
                self.clear_selection()
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == '':
            self.main_window.statusBar().showMessage('空闲：(%d, %d)' % (x,y))
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id +' 线段')
            self.finish_draw()
            self.status = ''
        elif self.status == 'polygon':
            pass
        super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self.status == 'polygon':
            # 多边形双击闭合
            if not self.item_dict[self.temp_id]:
                return
            p_list = [self.item_dict[self.temp_id][0].p_list[0],]
            for line_item in self.item_dict[self.temp_id]:
                p_list.append(line_item.p_list[1])
                self.scene().removeItem(line_item)
            self.temp_item = MyItem(self.temp_id, 'polygon', p_list, self.temp_algorithm, self.temp_pen_color)
            self.scene().addItem(self.temp_item)
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id +' fuck you')
            self.finish_draw()
            self.status = ''
        self.updateScene([self.sceneRect()])
        super().mouseDoubleClickEvent(event)

    def get_pos(self, event: QMouseEvent) -> [int, int]:
        pos = self.mapToScene(event.localPos().toPoint())
        return [int(pos.x()), int(pos.y())]


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', color = QColor(0,0,0), parent: QGraphicsItem = None):
        """
        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.color = color
        logging.debug('create MyItem {} with p_list={}'.format(item_type, p_list))

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        draw_dict = {
            'line': alg.draw_line,
            'polygon': alg.draw_polygon,
            'ellipse': alg.draw_ellipse,
            'curve': alg.draw_curve
        }
        if self.item_type == 'polygon':
            logging.debug('fucking polygon')
        item_pixels = draw_dict[self.item_type](self.p_list, self.algorithm)
        for p in item_pixels:
            painter.setPen(self.color)
            painter.drawPoint(*p)
        if self.selected:
            painter.setPen(QColor(255, 0 ,0))
            painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        min_x, min_y, max_x, max_y = 1001, 1001, -1, -1
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            min_x = min(x0, x1)
            min_y = min(y0, y1)
            max_x = max(x0, x1)
            max_y = max(y0, y1)
        elif self.item_type == 'polygon':
            for [xx, yy] in self.p_list:
                min_x, min_y, max_x, max_y = min(xx, min_x), min(yy, min_y), max(xx, max_x), max(yy, max_y)
        elif self.item_type == 'ellipse':
            pass
        elif self.item_type == 'curve':
            pass
        return QRectF(min_x-1,  min_y-1, max_x-min_x+2, max_y-min_y+2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0
        self.pen_color = QColor(0,0,0)

        self.height = self.width = 600
        self.set_canvas_action()

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        clear_canvas_act = file_menu.addAction('清空画布')
        save_canvas_act = file_menu.addAction('保存画布')
        save_canvas_act.setShortcut('Ctrl+S')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        #-------------------文件--------------------
        exit_act.triggered.connect(qApp.quit)
        clear_canvas_act.triggered.connect(self.clear_canvas_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        set_pen_act.triggered.connect(self.set_pen_action)
        # -------------------绘制--------------------
        save_canvas_act.triggered.connect(self.save_canvas_action)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed_from_list)

    def get_id(self):
        return str(self.item_cnt)

    def new_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id
    
    def set_pen_action(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas_widget.temp_pen_color = color
            # logging.debug('set pen color to {}'.format(color))git

    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        # self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.canvas_widget.clear_selection()
    
    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.canvas_widget.clear_selection()

    def clear_canvas_action(self):
        """清空画布
        """
        self.canvas_widget.resetCachedContent()
        for item_id in range(0, self.item_cnt-1):
            del self.canvas_widget.item_dict[str(item_id)]
            logging.debug('delete item %d' % item_id)
        self.item_cnt = 0
    
    def reset_canvas_action(self):
        self.clear_canvas_action()
        while True:
            width, ok = QInputDialog.getInt(self, '重置画布', '请输入画布宽度：（单位：像素）')
            if ok and width <= 1000 and width >= 100:
                self.width = width
                logging.debug('set width to {}'.format(self.width))
                break
            elif not ok: 
                break
        while True:
            height, ok = QInputDialog.getInt(self, '重置画布', '请输入画布高度：（单位：像素）')
            if ok and height <= 1000 and height >= 100:
                self.height = height
                logging.debug('set height to {}'.format(self.height))
                break
            elif not ok: 
                break
        del self.scene
        del self.canvas_widget
        del self.hbox_layout
        del self.list_widget
        self.item_cnt = 0
        self.set_canvas_action()
    
    def save_canvas_action(self):
        path = QFileDialog.getSaveFileName(parent=self, caption='保存画布',filter='Images(*.bmp)')
        # path = file_dialog.getSaveFileName()
        logging.debug('Save canvas to {}'.format(path))
        image = self.canvas_widget.grab(self.canvas_widget.sceneRect().toRect())
        image.save(path[0])
    
    def set_canvas_action(self):
        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, self.width, self.height)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(self.width+10, self.height+10)
        self.canvas_widget.main_window = self
        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)
        self.list_widget.setMaximumWidth(200)
        self.canvas_widget.list_widget = self.list_widget
        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('新画布：({}*{})'.format(self.height, self.width))
        self.resize(self.width, self.height)
        self.setWindowTitle('CG Demo')
        


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
