#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math
import logging


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    logging.debug('draw line for {} with {}'.format(p_list, algorithm))
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        dx, dy = x1 - x0, y1 - y0
        if abs(dx) >= abs(dy):
            # 斜率<=1
            step = abs(dx)
        else:
            # 斜率>1
            step = abs(dy)
        dx, dy = dx / step, dy / step
        for i in range(0, step + 1):
            result.append((int(x0 + dx * i), int(y0 + dy * i)))
    elif algorithm == 'Bresenham':
        if x1 == x0:
            result = [[x0, y] for y in range(min(y0, y1), max(y0, y1) + 1)]
            return result
        elif y1 == y0:
            result = [[x ,y0] for x in range(min(x0, x1), max(x0, x1) + 1)]
            return result
        dx, dy = x1 - x0, y1 - y0
        if abs(dx) >= abs(dy):
            if x0 > x1:
                # 直线生成方向与坐标轴相反时交换起始点
                x0, y0, x1, y1 = x1, y1, x0, y0
            result.append([x0, y0])
            dx, dy = x1 - x0, abs(y1 - y0)
            p = 2 * dy  - dx
            y = y0
            step = int(dy / (y1 - y0))
            for k in range(0, dx):
                if p < 0:
                    result.append([x0 + k + 1, y])
                    p += (dy * 2)
                else:
                    y += step
                    result.append([x0 + k + 1, y])
                    p += (dy * 2 - dx * 2)
        else:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            result.append([x0, y0])
            dx, dy = x1 - x0, y1 - y0
            p = dx * 2 - dy
            x = x0
            step = int(dx / abs(dx))
            dx = abs(dx)
            for k in range(0, dy):
                if p < 0:
                    result.append([x, y0 + k +1])
                    p += (dx * 2)
                else:
                    x += step
                    result.append([x, y0 + k + 1])
                    p += (dx * 2 - dy * 2)
        logging.debug('Bresenham ends at {}'.format(result[-1]))
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    quater = []
    rx, ry = (int(abs(x1 - x0) / 2), int(abs(y1 - y0) / 2))
    rx2, ry2 = rx * rx, ry * ry
    xc, yc = int((x1 + x0) / 2), int((y1 + y0) / 2)
    logging.debug('draw ellipse at ({},{}), with rx={}, ry={}'.format(xc, yc, rx, ry))
    quater.append([0, ry])
    p = ry2- rx2 * ry + ry2 / 4
    x, y, k = 0, ry, 0
    # 区域1
    while 2 * ry2 * x < 2 * rx2 * y:
        if p < 0:
            quater.append([k + 1, y])
            p += 2 * ry2 * (k + 1) + ry2
        else:
            y -= 1
            quater.append([k + 1, y])
            p += 2 * ry2 * (k + 1) - 2 * rx2 * y + ry2
        k += 1
        x = k
    # 区域2
    k = 0
    p = ry2 * (x + 1/2) * (x + 1/2) + rx2 * (y - 1) * (y - 1) - rx2 * ry2
    for k in range(0, y):
        if p > 0:
            quater.append([x, y - k - 1])
            p += rx2 - 2 * rx2 * (y-k-1)
        else:
            x += 1
            quater.append([x, y - k - 1])
            p += 2 * ry2 * x - 2 * rx2 * (y-k-1) + rx2
    # 对称
    full = []
    for [x, y] in quater:
        full.extend([[x,y], [-x, y], [x, -y], [-x, -y]])
    # 平移
    for [x, y] in full:
        result.append([x + xc, y + yc])
    return result

def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    logging.debug('Start to draw curve with {}'.format(p_list))
    result = []
    if algorithm == 'Brezier':
        n = len(p_list) - 1 
        # 计算二项式系数
        comb = []
        comb.append(1)
        for i in range(0, n):
            comb.append(comb[i] / (i + 1) * (n - i))
        # 计算Brezier曲线公式
        prec = 300 #精度（我也不知道设多少好
        for i in range(0, prec):
            x, y = 0, 0
            t = i / prec
            for j in range(0, n + 1):
                col =  comb[j] * ((1-t) **(n-j)) * (t**j)
                x += col * p_list[j][0]
                y += col * p_list[j][1]
            result.append([int(x), int(y)])
    elif algorithm == 'B-spline':
        pass
    else:
        raise ValueError('No such algorithm.')
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for a in p_list:
        result.append([a[0] + dx, a[1] + dy])
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    sinr = math.sin(r * math.pi / 180)
    cosr = math.cos(r * math.pi / 180)
    for [xx,yy] in p_list:
        newx = x + (xx - x) * cosr - (yy - y) * sinr
        newy = y + (xx - x) * sinr + (yy - y) * cosr
        result.append([int(newx), int(newy)])
        logging.debug('rotate {} to {}'.format([xx, yy], result[-1]))
    return result


def scale(p_list, x, y, s):
    """缩放变换
    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    cx, cy = x * (1 - s), y * (1 - s)
    for [xx, yy] in p_list:
        newx, newy = int(xx * s + cx), int(yy * s + cy)
        result.append([newx, newy])
    return result

def outcode(x, y, x_min, y_min, x_max, y_max):
    """输出区域码，供线段Cohen-Sutherland裁剪算法使用
    """
    left, right, down, up = 0b0001, 0b0010, 0b0100, 0b1000
    oc = 0
    if x < x_min:
        oc |= left
    elif x > x_max:
        oc |= right
    if y < y_min:
        oc |= up
    elif y > y_max:
        oc |= down
    return oc

def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪
    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    result = []
    [x0, y0], [x1, y1] = p_list
    logging.debug('Start to clip {} with ({},{}) to ({},{})'.format(p_list, x_min, y_min, x_max, y_max))
    if algorithm == 'Cohen-Sutherland':
        oc0 = outcode(x0, y0, x_min, y_min, x_max, y_max)
        oc1 = outcode(x1, y1, x_min, y_min, x_max, y_max)
        accept = False
        while True:
            if oc0 == 0 and oc1 == 0:
                # 两端点都在区域内
                accept = True
                break
            elif (oc0 & oc1) != 0:
                # 两端点都在区域外
                break
            else:
                oc = oc0
                if oc0 == 0:
                    oc = oc1
                left, right, down, up = 0b0001, 0b0010, 0b0100, 0b1000
                dx, dy = x1 - x0, y1 - y0
                if oc & left:
                    x, y = x_min, (x_min - x0) * dy / dx + y0
                elif oc & right:
                    x, y = x_max, (x_max - x0) * dy / dx + y0
                elif oc & up:
                    x, y = (y_min - y0) * dx / dy + x0, y_min
                elif oc & down:
                    x, y = (y_max - y0) * dx / dy + x0, y_max
                if oc == oc0:
                    x0, y0, oc0 = x, y, outcode(x, y, x_min, y_min, x_max, y_max)
                else:
                    x1, y1, oc1 = x, y, outcode(x, y, x_min, y_min, x_max, y_max)
                logging.debug('clip to ({}, {})-({}, {})'.format(x0, y0, x1, y1))
        if accept:
            result = [[int(x0), int(y0)], [int(x1), int(y1)]]
        logging.debug('C-S clip get {}'.format(result))
        return result
    elif algorithm == 'Liang-Barsky':
        pass
    else:
        print('Invalid algorithm: ' + algorithm)
