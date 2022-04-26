# -*- coding: utf-8 -*-

"""
Created on 2020年7月16日
@author: Yuleitao
@email: 773673787@qq.com
@file: RobotMonitor
@description: 机器人监控端
"""

import sys
import logging
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from src.gui.miniWindow import UserInteractionMiniWindow

"""
pyinstaller -w -i .src/gui/resources/hcrt.ico robotMonitor.py
打包命令
"""

"""
qt官方文档：https://doc.qt.io/qt-5/qtwidgets-module.html
"""


if __name__ == '__main__':
    try:
        QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  #解决高分屏缩放问题
        app = QtWidgets.QApplication(sys.argv)
        ui = UserInteractionMiniWindow()
        ui.setupMainWindows()
        ui.show()
        sys.exit(app.exec_())
    except Exception as exception:\
    logging.error(exception, exc_info=True)
