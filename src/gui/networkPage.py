# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from src.gui.Ui_miniGui import Ui_MainWindow
from src.gui.networkUdp import UdpLogic
import socket

""" 
    网络界面的函数
"""
class NetworkPage(UdpLogic, Ui_MainWindow):

    def setupNetPage(self):
        self.is_network_available = False
        self.is_fullscreen = False

    @pyqtSlot()
    def on_pushButton_get_ip_clicked(self):
        # 获取本机ip
        self.lineEdit_local_ip.clear()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            my_addr = s.getsockname()[0]
            my_port = 2223
            target_addr = "192.168.4.1"
            target_port = 2222
            msg = '本机地址:{}'.format((my_addr,my_port))
            print(msg)
            self.textBrowser_net_info.append(msg)
            msg = '目标地址:{}'.format((target_addr,target_port))
            print(msg)
            self.textBrowser_net_info.append(msg)
            self.lineEdit_local_ip.setText(str(my_addr))
            self.lineEdit_local_port.setText(str(my_port))
            self.lineEdit_target_ip.setText(str(target_addr))
            self.lineEdit_target_port.setText(str(target_port))
        except Exception as ret:
            # 若无法连接互联网使用，会调用以下方法
            try:
                my_addr = socket.gethostbyname(socket.gethostname())
            except Exception as ret_e:
                self.signal_write_msg.emit("无法获取ip，请连接网络！\n")
        else:
            print('获取成功')
            s.close()

    @pyqtSlot()
    def on_pushButton_net_link_clicked(self):
        # 启动连接
        self.udp_server_start()
        self.udp_client_start()
        self.link = True
        self.is_network_available = True
        self.pushButton_net_unlink.setEnabled(True)
        self.pushButton_net_link.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_net_unlink_clicked(self):
        # 关闭连接
        self.udp_close()
        self.link = False
        self.is_network_available = False
        self.pushButton_net_unlink.setEnabled(False)
        self.pushButton_net_link.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_fullscreen_clicked(self):
        #全屏
        if self.is_fullscreen == False:
            self.showFullScreen()
            self.is_fullscreen = True
            print('全屏')
        elif self.is_fullscreen == True:
            self.showNormal()
            self.is_fullscreen = False
            print('退出全屏')
            
    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        #关闭程序
        self.close()
        
