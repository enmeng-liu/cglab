#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys, logging
from PyQt5.QtWidgets import (QApplication,)
import MainWindow


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    app = QApplication(sys.argv)
    mw = MainWindow.MainWindow()
    mw.show()
    sys.exit(app.exec_())
