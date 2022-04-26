# -*- coding: utf-8 -*-


from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from src.gui.Ui_miniGui import Ui_MainWindow
import socket


class Thread(QThread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super(Thread, self).__init__()
        if kwargs is None:
            kwargs = {}
        self._target = target
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs


class UdpLogic(Ui_MainWindow):

    signal_write_msg = QtCore.pyqtSignal(bytes)

    def __init__(self, *args, **kwargs):
        super(UdpLogic, self).__init__(*args, **kwargs)

        self.udp_server_socket = None
        self.udp_client_socket = None
        self.sever_thread = None  # 初始化 udp server 的线程
        self.client_thread = None  # 初始化 udp client 的线程

        self.net_recv_msg = bytes
        self.address = None
        self.link = False  # 网络有没有连接的标志位

    def __del__(self):
        print(' UDP Logic 运行析构函数,释放资源')
        self.udp_close()

    def udp_server_start(self):
        """
        开启UDP服务端方法
        :return:
        """
        self.udp_server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)

        try:
            port = int(self.lineEdit_local_port.text())
            address = ('', port)
            self.udp_server_socket.bind(address)
            msg = 'UDP服务端正在开启...'
            print(msg)
            self.textBrowser_net_info.append(msg)
        except Exception as ret:  # 捕捉到的异常放入ret中,并执行下面的代码
            msg = '请检查端口号'
            print(msg)
            self.textBrowser_net_info.append(msg)
        else:
            self.sever_thread = Thread(target=self.udp_server_concurrency)
            self.sever_thread.start()
            msg = 'UDP服务端正在监听端口:{}'.format(port)
            print(msg)
            self.textBrowser_net_info.append(msg)

    def udp_server_concurrency(self):
        """
        持续监听UDP通信的线程
        :return:
        """
        while True:
            recv_msg, recv_addr = self.udp_server_socket.recvfrom(1024)
            # print('net_recv_msg type: ', type(self.net_recv_msg))
            # print('net_recv_msg: ', self.net_recv_msg)
            self.signal_write_msg.emit(recv_msg)

    def udp_client_start(self):
        """
        确认UDP客户端的ip及地址
        :return:
        """
        self.udp_client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.address = (str(self.lineEdit_target_ip.text()),
                            int(self.lineEdit_target_port.text()))
        except Exception as ret:
            msg = '请检查目标IP,目标端口\n'
            self.textBrowser_net_info.append(msg)
        else:
            msg = 'UDP客户端已启动\n'
            self.textBrowser_net_info.append(msg)

    def udp_close(self):
        """
        功能函数,关闭网络连接的方法
        :return:
        """
        try:
            self.sever_thread.terminate()
            self.sever_thread.wait()
        except Exception:
            pass
        try:
            self.udp_server_socket.close()
            self.udp_client_socket.close()
            if self.link is True:
                msg = '已断开网络\n'
                self.textBrowser_net_info.append(msg)
        except Exception as ret:
            pass
