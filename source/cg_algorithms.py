#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math
import logging
import collections


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    # logging.debug('draw line for {} with {}'.format(p_list, algorithm))
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if x1 == x0:
        result = [[x0, y] for y in range(min(y0, y1), max(y0, y1) + 1)]
        return result
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, round(y0 + k * (x - x0))))
    #-----------------------------------------------
    elif algorithm == 'DDA':
        dx, dy = x1 - x0, y1 - y0
        step = max(abs(dx), abs(dy))
        dx, dy = dx / step, dy / step
        for i in range(0, step + 1):
            result.append((round(x0 + dx * i), round(y0 + dy * i)))
    #-----------------------------------------------
    elif algorithm == 'Bresenham':
        if y1 == y0:
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
            step = round(dy / (y1 - y0))
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
            dx, dy = abs(x1 - x0), y1 - y0
            p = dx * 2 - dy
            x = x0
            step = round(dx / (x1 - x0))
            dx = abs(dx)
            for k in range(0, dy):
                if p < 0:
                    result.append([x, y0 + k +1])
                    p += (dx * 2)
                else:
                    x += step
                    result.append([x, y0 + k + 1])
                    p += (dx * 2 - dy * 2)
        # logging.debug('Bresenham ends at {}'.format(result[-1]))
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    # logging.debug('alg: draw polygon with p_list={}'.format(p_list))
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result

def draw_rect(p_list, algorithm):
    """绘制矩形（GUI中使用）
    ：param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 矩形的左上角和右下角顶点坐标
    ：return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    return draw_polygon([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], 'Bresenham')

def draw_ellipse(p_list, algorithm):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    if p_list[0] == p_list[1]:
        return [p_list[0],]
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    quarter = []
    rx, ry = (round(abs(x1 - x0) / 2), round(abs(y1 - y0) / 2))
    rx2, ry2 = rx * rx, ry * ry
    xc, yc = round((x1 + x0) / 2), round((y1 + y0) / 2)
    # logging.debug('draw ellipse at ({},{}), with rx={}, ry={}'.format(xc, yc, rx, ry))
    quarter.append([0, ry])
    p = ry2- rx2 * ry + rx2 / 4
    x, y, k = 0, ry, 0
    # 区域1
    while 2 * ry2 * x < 2 * rx2 * y:
        if p < 0:
            quarter.append([k + 1, y])
            p += 2 * ry2 * (k + 1) + ry2
        else:
            y -= 1
            quarter.append([k + 1, y])
            p += 2 * ry2 * (k + 1) - 2 * rx2 * y + ry2
        k += 1
        x = k
    # 区域2
    k = 0
    p = ry2 * (x + 1/2) * (x + 1/2) + rx2 * (y - 1) * (y - 1) - rx2 * ry2
    for k in range(0, y):
        if p > 0:
            quarter.append([x, y - k - 1])
            p += rx2 - 2 * rx2 * (y-k-1)
        else:
            x += 1
            quarter.append([x, y - k - 1])
            p += 2 * ry2 * x - 2 * rx2 * (y-k-1) + rx2
    # 对称
    full = []
    for [x, y] in quarter:
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
    # logging.debug('Start to draw curve with {}'.format(p_list))
    result, points = [], []
    n = len(p_list) # 控制点个数
    if algorithm == 'Bezier':
        # 计算n-1为底的二项式系数
        comb = []
        comb.append(1)
        for i in range(0, n):
            comb.append(comb[i] / (i + 1) * (n - 1 - i))
        # 计算Bezier曲线公式
        step = 0.01
        u = 0
        while u <= 1:
            x, y = 0.0, 0.0
            for i in range(0, n):
                x += comb[i] * math.pow(u, i) * math.pow(1-u, n-1-i) * p_list[i][0]
                y += comb[i] * math.pow(u, i) * math.pow(1-u, n-1-i) * p_list[i][1]
            points.append([round(x), round(y)])
            u = u + step
    elif algorithm == 'B-spline':
        k = 4 #阶数
        if n < k:
            # print('Not enough control points.')
            return []
        # 计算节点矢量
        U = []
        for i in range(0, n+k+1):
            U.append(i*100/(n+k))
        #子函数
        def de_Boor_Cox(r, i, u):
            """de Boor Cox公式递归计算x,y坐标
            """
            if r == 0:
                return p_list[i]
            tmp = 0
            if u - U[i] == 0 and U[i+k-r] - U[i]  == 0:
                tmp = 1
            else:
                tmp = (u - U[i]) / (U[i+k-r]-U[i])
            x1, y1 = de_Boor_Cox(r-1, i, u)
            x2, y2 = de_Boor_Cox(r-1, i-1, u)
            x = tmp * x1 + (1-tmp) * x2
            y = tmp * y1 + (1-tmp) * y2
            return x,y
        # 只在[t_{k-1}, t_n]上有定义，故只需在这个范围枚举j
        step = 0.01
        for j in range(k-1, n):
            u = U[j]
            while u < U[j + 1]:
                p = de_Boor_Cox(k-1, j, u)
                points.append([round(p[0]), round(p[1])])
                u = u + step
    else:
        print('No such algorithm.')
    # 生成的点间用直线相连
    for i in range(0, len(points)-1):
        result = result + draw_line(points[i:i+2], 'Bresenham')
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    # logging.debug('translate (%d, %d)' % (dx, dy))
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
    return rotate_by_radian(p_list, x, y, r*math.pi/180)

def rotate_by_radian(p_list, x, y ,r):
    """弧度制旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转弧度
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    sinr = math.sin(r)
    cosr = math.cos(r)
    for [xx,yy] in p_list:
        newx = x + (xx - x) * cosr - (yy - y) * sinr
        newy = y + (xx - x) * sinr + (yy - y) * cosr
        result.append([round(newx), round(newy)])
        # logging.debug('rotate {} to {}'.format([xx, yy], result[-1]))
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
        newx, newy =  round(xx * s + cx), round(yy * s + cy)
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

def clipt(d, q, tl, tu):
    """确定裁剪后线段上参数的最大值或最小值
    """
    t = q / d
    visible = True
    if d == 0 and q < 0:
        # line is outside and parallel to the edge
        visible = False
    elif d < 0: 
        # looking for upper limit
        if t > tu:
            # check for trivially invisible
            visible = False
        elif t > tl:
            tl = t # find the minimum of the maximum
    elif d > 0:
        # looking for lower limit
        if t < tl:
            visible = False
        elif t < tu:
            tu = t
    return visible, tl, tu


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
    # logging.debug('Start to clip {} with ({},{}) to ({},{})'.format(p_list, x_min, y_min, x_max, y_max))
    if x_min > x_max or y_min > y_max:
        return p_list
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
                # logging.debug('clip to ({}, {})-({}, {})'.format(x0, y0, x1, y1))
        if accept:
            result = [[round(x0), round(y0)], [round(x1), round(y1)]]
        # logging.debug('C-S clip get {}'.format(result))
        return result
    elif algorithm == 'Liang-Barsky':
        tl, tu = 0, 1
        dx, dy = x1 - x0, y1 - y0
        visible, tl, tu = clipt(-dx, x0-x_min, tl, tu)
        if visible == False:
            return []
        visible, tl, tu = clipt(dx, x_max-x0, tl, tu)
        if visible == False:
            return []
        visible, tl, tu = clipt(-dy, y0-y_min, tl, tu) 
        if visible == False:
            return []
        visible, tl, tu = clipt(dy, y_max-y0, tl, tu)
        if visible == False:
            return []
        # logging.debug('visible=%d, tl=%f, tu=%f' % (visible, tl, tu))
        if tu < 1:
            x1, y1 = x0+tu*dx, y0+tu*dy
        if tl > 0:
            x0, y0 = x0+tl*dx, y0+tl*dy
        if visible:
            result = [[round(x0), round(y0)], [round(x1), round(y1)]]
        return result
    else:
        print('Invalid algorithm: ' + algorithm)
    return result

