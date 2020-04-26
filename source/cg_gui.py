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

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        # logging.debug('draw line with color: {}'.format(self.temp_pen_color))

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.temp_pen_color)
            self.scene().addItem(self.temp_item)
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        super().mouseReleaseEvent(event)


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

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.color)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255,0,0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            pass
        elif self.item_type == 'ellipse':
            pass
        elif self.item_type == 'curve':
            pass

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            pass
        elif self.item_type == 'ellipse':
            pass
        elif self.item_type == 'curve':
            pass


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0
        self.pen_color = QColor(0,0,0)

        self.height = self.width = 600
        self.set_canvas()

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
        exit_act.triggered.connect(qApp.quit)
        clear_canvas_act.triggered.connect(self.clear_canvas_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        save_canvas_act.triggered.connect(self.save_canvas_action)
        line_naive_act.triggered.connect(self.line_naive_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
        set_pen_act.triggered.connect(self.set_pen_action)

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id
    
    def set_pen_action(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas_widget.temp_pen_color = color
            # logging.debug('set pen color to {}'.format(color))

    def line_naive_action(self):
        # self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
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
        self.set_canvas()
    
    def save_canvas_action(self):
        # file_dialog = QFileDialog(self, '保存画布', '.', '(*.bmp)')
        path = QFileDialog.getSaveFileName(parent=self, caption='保存画布',filter='Images(*.bmp)')
        # path = file_dialog.getSaveFileName()
        logging.debug('Save canvas to {}'.format(path))
        image = self.canvas_widget.grab(self.canvas_widget.sceneRect().toRect())
        image.save(path[0])
    
    def set_canvas(self):
        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, self.width, self.height)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(self.width+100, self.height+100)
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