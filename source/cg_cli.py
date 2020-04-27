#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import cg_algorithms as alg
import numpy as np
import logging
from PIL import Image


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    item_dict = {}
    pen_color = np.zeros(3, np.uint8)
    width = 0
    height = 0
    draw_dict = {
        'line': alg.draw_line,
        'polygon': alg.draw_polygon,
        'ellipse': alg.draw_ellipse,
        'curve': alg.draw_curve
    }

    with open(input_file, 'r') as fp:
        line = fp.readline()
        while line:
            line = line.strip().split(' ')
            if line[0][0] == '#':
                pass #注释
            if line[0] == 'resetCanvas':
                item_dict.clear() #清空画布
                width = int(line[1])
                height = int(line[2])
            elif line[0] == 'saveCanvas':
                save_name = line[1]
                canvas = np.zeros([height, width, 3], np.uint8)
                canvas.fill(255)
                for item_type, p_list, algorithm, color in item_dict.values():
                    pixels = draw_dict[item_type](p_list, algorithm)
                    for x,y in pixels:
                        canvas[y, x] = color
                Image.fromarray(canvas).save(os.path.join(output_dir, save_name + '.bmp'), 'bmp')
            elif line[0] == 'setColor':
                pen_color[0] = int(line[1])
                pen_color[1] = int(line[2])
                pen_color[2] = int(line[3])
            elif line[0] == 'drawLine':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = line[6]
                item_dict[item_id] = ['line', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
            elif line[0] == 'drawPolygon':
                item_id = line[1]
                p_list = []
                for i in range(1, len(line) - 1, 2):
                    p_list.append([int(line[i]), int(line[i + 1])])
                    logging.debug('append {}'.format(p_list[-1]))
                algorithm = line[-1]
                item_dict[item_id] = ['polygon', p_list, algorithm, np.array(pen_color)]
            elif line[0] == 'drawEllipse':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                item_dict[item_id] = ['ellipse', [[x0, y0], [x1, y1]], 'midpoint', np.array(pen_color)]
            elif line[0] == 'drawCurve':
                item_id = line[1]
                p_list = []
                for i in range(2, len(line) - 1, 2):
                    p_list.append([int(line[i]), int(line[i + 1])])
                algorithm = line[-1]
                item_dict[item_id] = ['curve', p_list, algorithm, np.array(pen_color)]
            elif line[0] == 'translate':
                item_id = line[1]
                item_type, p_list, algorithm, color = item_dict[item_id]
                p_list = alg.translate(p_list, int(line[2]), int(line[3]))
                item_dict[item_id] = item_type, p_list, algorithm, color
            elif line[0] == 'rotate':
                item_id = line[1]
                item_type, p_list, algorithm, color = item_dict[item_id]
                p_list = alg.rotate(p_list, int(line[2]), int(line[3]), int(line[4]))
                item_dict[item_id] = item_type, p_list, algorithm, color
            elif line[0] == 'scale':
                item_id = line[1]
                item_type, p_list, algorithm, color = item_dict[item_id]
                p_list = alg.scale(p_list, int(line[2]), int(line[3]), int(line[4]))
                item_dict[item_id] = item_type, p_list, algorithm, color
            elif line[0] == 'clip':
                item_id = line[1]
                item_type, p_list, algorithm, color = item_dict[item_id]
                if item_type != 'line':
                    print('Cannot clip {} type'.format(item_type))
                p_list = alg.clip(p_list, int(line[2]), int(line[3]), int(line[4]), int(line[5]), line[6])
                if len(p_list):
                    item_dict[item_id] = item_type, p_list, algorithm, color
                else:
                    del item_dict[item_id]
            else:
                print('Invalid command: ' + line[0])
            line = fp.readline()

