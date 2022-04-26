#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow
from src.gui.networkPage import NetworkPage
from src.gui.controlPage import ControlPage
from src.gui.Ui_miniGui import Ui_MainWindow


class UserInteractionMiniWindow(ControlPage, NetworkPage, QMainWindow, Ui_MainWindow):

    def setupMainWindows(self):
        # 白色背景
        pg.setConfigOption('background', '#FFFFFF')  # 设置背景
        pg.setConfigOption('foreground', '#232629')  # 设置前景（包括坐标轴，线条，文本等等）
        # 黑色背景
        # pg.setConfigOption('background', '#232629')  # 设置背景
        # pg.setConfigOption('foreground', '#FFFFFF')  # 设置前景（包括坐标轴，线条，文本等等）
        pg.setConfigOptions(antialias=True)  # 使曲线看起来更光滑，而不是锯齿状

        self.setupUi(self)  # 创建UI中的所有控件

        # 每个页面需要初始化的内容
        self.setupNetPage()
        self.setupControlPage()

        self.on_pushButton_get_ip_clicked()  # 先获取本机IP和端口

        # self.on_pushButton_fullscreen_clicked() #最大化窗口

        self.tabWidget.setStyleSheet(
        '''
                QTabBar::tab {
                    height:30px;
                    width:80px;
                }
        ''')