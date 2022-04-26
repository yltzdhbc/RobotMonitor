# -*- coding: utf-8 -*-

import struct
from PyQt5.QtCore import pyqtSlot
from src.gui.Ui_miniGui import Ui_MainWindow
from src.gui.networkPage import NetworkPage
import pyqtgraph as pg

HEADER = bytes([0xff])
ENDER = bytes([0xdd])

def GetCRC(data, length):
    crc = 0
    for i in range(0, length):
        crc = crc ^ data[i]
        for x in range(0, 8):
            if crc & 0x01:
                crc = (crc >> 1) ^ 0x8C
            else:
                crc = crc >> 1
    return crc

# 箭头类
class CenteredArrowItem(pg.ArrowItem):
    def setData(self, x, y, angle):
        self.opts['angle'] = angle
        opt = dict([(k, self.opts[k]) for k in ['headLen',
                   'tipAngle', 'baseAngle', 'tailLen', 'tailWidth']])
        path = pg.functions.makeArrowPath(**opt)
        b = path.boundingRect()
        tr = pg.QtGui.QTransform()
        tr.rotate(-angle + 90)
        tr.translate(-b.x() - b.width() / 2, -b.y() - b.height() / 2)
        self.path = tr.map(path)
        self.setPath(self.path)
        self.setPos(x, y)


class ControlPage(NetworkPage, Ui_MainWindow):

    def setupControlPage(self):

        # 参数设置区域
        ##########################################
        self.vxset_inc = 0.2
        self.vyset_inc = 0.2
        self.wzset_inc = 0.3

        # 变量定义区域
        ##########################################
        self.vx_set = 0.0
        self.vy_set = 0.0
        self.wz_set = 0.0

        self.is_serial_available = 0

        self.position_x_1 = [1]
        self.position_y_1 = [1]
        self.time = []
        self.showtime = 0.0

        # 信号槽
        ##########################################
        self.signal_write_msg.connect(self.protocol_handler)

        # 实例初始化
        ##########################################
        # 初始化pyqtgraph
        self.pg_pos.clear()
        # self.plot10 = self.pg_pos.addPlot(title="监控")
        self.plot11 = self.pg_pos.addPlot()

        # self.pyqtgraph11.clear()
        # self.plot11 = self.pyqtgraph11.addPlot(title="监控")
        # self.plot11 = self.pyqtgraph11.addPlot()

        self.plot11.addLegend(size=(100, 50), offset=(0, 0))  # 设置图形的图例

        # 设置图形网格的形式，我们设置显示横线和竖线，并且透明度惟0.5：
        self.plot11.showGrid(x=True, y=True, alpha=0.5)
        # self.plot11.setLabel(axis='left', text=u'Y')
        # self.plot11.setLabel(axis='bottom', text=u'X')
        self.plot11.setXRange(min=-18.4, max=18.4, padding=0)
        self.plot11.setYRange(min=-10, max=10, padding=0)
        # self.curve11_1 = self.plot11.plot(pen=pg.mkPen(color='b', width=5), name="全局坐标", symbol='o',
        #                                   symbolSize=4, symbolPen=(0, 0, 0), symbolBrush=(0, 0, 0))
        self.arrow = CenteredArrowItem(headLen=40, tipAngle=45, baseAngle=30)
        self.plot11.addItem(self.arrow)
        self.arrow.setData(0, 0, 0)

    def protocol_handler(self , received_data):
        # [头  ][命令] [长] [ 数据内容长度不定 ] [CRC] [  尾 ]
        # 01 23 45 67  89  1011 1213‘’‘’‘’   1415  1617 1819
        # 55 aa 5a 5a  2                      cb   0d  0a
        # print('received_data type: ', type(received_data))
        # print('received ', received_data.hex())
        # 获得消息头
        header = received_data[0:1]
        if header == HEADER:  # 消息头正确
            # 获得指令
            command = received_data[1:2] # 获得命令指令
            length = int.from_bytes(received_data[2:3], byteorder='little', signed=False) # 获得数据长度
            ender = received_data[(3 + length + 1):(3 + length + 2)]  # 获得尾部帧
            if ender == ENDER:  # 消息尾正确
                # 进行CRC校验
                temp = []
                for i in range(0, length + 3, 1):
                    temp += [int.from_bytes(received_data[i:i+1], byteorder='little', signed=False)]
                crc_calc = bytes([GetCRC(temp, len(temp))])
                crc_recv = received_data[(3 + length): (3 + length + 1)]
                if crc_calc == crc_recv:    # CRC校验通过
                    #数据解析 将数据转换为16位的int
                    data_raw = {}
                    data = {}
                    for i in range(0, int(length / 2)  , 1):
                        data_raw[i] = int.from_bytes(received_data[3+i*2:5+i*2], byteorder='little', signed=True)
                        data[i] = round(data_raw[i]/100,2)
                    #得到此次数据的个数
                    data_num = len(data)

                    # print('DATA------------------')
                    # print('len data:', data_num)
                    # for i in range(0, data_num  , 1):
                    #     print('data_raw:', data_raw[i])
                    #     print('data:', data[i])

                    vx_act = data[0]
                    vy_act = data[1]
                    wz_act = data[2]

                    x_act = data[3]
                    y_act = data[4]
                    a_act = data[5]

                    batt_vol = data[6]

                    s0 = data[7]
                    s1 = data[8]
                    s2 = data[9]
                    s3 = data[10]

                   
                    self.lineEdit_vx_act.setText(str(vx_act))
                    self.lineEdit_vy_act.setText(str(vy_act))
                    self.lineEdit_wz_act.setText(str(wz_act))

                    self.lineEdit_pos_x_act.setText(str(x_act))
                    self.lineEdit_pos_y_act.setText(str(y_act))
                    self.lineEdit_ang_z_act.setText(str(a_act))
                    self.arrow.setData(-y_act, x_act, a_act)
                    # self.arrow.setData(x_act, y_act, a_act)


                    self.lineEdit_voltage.setText(str(batt_vol))
                    battery_percent = int(batt_vol / 26 * 100)
                    self.lineEdit_battery_precent.setText(
                        str(battery_percent))
                    self.precentbar1.Value = battery_percent
                    self.precentbar1_2.Value = battery_percent
                    self.lineEdit_vehicle_state.setText(str(0))

                    self.lineEdit_s0.setText(str(s0))
                    self.lineEdit_s1.setText(str(s1))
                    self.lineEdit_s2.setText(str(s2))
                    self.lineEdit_s3.setText(str(s3))
                else:
                    print('crc is not correct, calc:%s recv:%s' % (crc_calc.hex() , crc_recv.hex()))
            else:
                print('ender is not correct:', ender.hex())
        else:
            print('header is not correct:', header.hex())



    def protocol_speedset_send(self, vx_set, vy_set, wz_set):
        yaw_set = 0
        head = struct.pack("B", 0xff)
        command = struct.pack("B", 0x00)
        length = (struct.pack("B", 16))
        x_set = (struct.pack("f", vx_set))
        y_set = (struct.pack("f", vy_set))
        w_set = (struct.pack("f", wz_set))
        yaw_set = (struct.pack("f", yaw_set))
        temp_crc = head + command + length + x_set + y_set+w_set+yaw_set
        crc = (struct.pack("B", GetCRC(temp_crc, len(temp_crc))))
        end = struct.pack("B", 0xdd)
        data = head+command+length+x_set+y_set + w_set+yaw_set+crc+end
        print('send data type: ', type(data))
        print('send data: ', data)
        self.udp_client_socket.sendto(data, self.address)

    def protocol_ctrl_send(self, btn, val):
        head = struct.pack("B", 0xff)
        command = struct.pack("B", 0x01) 
        length = (struct.pack("B", 1))  # 数据域的长度 [字节]
        btn = (struct.pack("B", btn))  # 按键值
        val = (struct.pack("B", val))  # 按键值
        temp_crc = head + command + length + btn + val
        crc = (struct.pack("B", GetCRC(temp_crc, len(temp_crc))))
        end = struct.pack("B", 0x0dd)
        data = head+command+length+btn+val+crc+end
        print('send data type: ', type(data))
        print('send data: ', data.hex())
        self.udp_client_socket.sendto(data, self.address)

    def constrain(self, x, min, max):
        if x < min:
            return min
        elif x > max:
            return max
        return round(x, 3)

    # 控制按键 回调区域
    ##################################################

    @pyqtSlot()
    def on_pushButton_ctrl0_clicked(self):
        self.protocol_ctrl_send(0, 1)

    @pyqtSlot()
    def on_pushButton_ctrl1_clicked(self):
        self.protocol_ctrl_send(1, 1)

    @pyqtSlot()
    def on_pushButton_ctrl2_clicked(self):
        self.protocol_ctrl_send(2, 1)

    @pyqtSlot()
    def on_pushButton_ctrl3_clicked(self):
        self.protocol_ctrl_send(3, 1)

    @pyqtSlot()
    def on_pushButton_ctrl4_clicked(self):
        self.protocol_ctrl_send(4, 1)

    @pyqtSlot()
    def on_pushButton_ctrl5_clicked(self):
        self.protocol_ctrl_send(5, 1)

    @pyqtSlot()
    def on_pushButton_poszreo_clicked(self):
        self.protocol_ctrl_send(6, 1)

    # 速度控制 回调区域
    ##################################################
    def update_setvel_display(self):
        self.lineEdit_setvx.setText(str(self.vx_set))
        self.lineEdit_setvy.setText(str(self.vy_set))
        self.lineEdit_setwz.setText(str(self.wz_set))

    @pyqtSlot()
    def on_pushButton_front_set_clicked(self):
        self.vx_set += self.vxset_inc
        self.vx_set = self.constrain(self.vx_set, -10, 10)
        self.update_setvel_display()
        print('liner_vel_x_set: ', self.vx_set)
        self.protocol_speedset_send(self.vx_set, self.vy_set, self.wz_set)

    @pyqtSlot()
    def on_pushButton_back_set_clicked(self):
        self.vx_set -= self.vxset_inc
        self.vx_set = self.constrain(self.vx_set, -10, 10)
        self.update_setvel_display()
        print('liner_vel_x_set: ', self.vx_set)
        self.protocol_speedset_send(self.vx_set, self.vy_set, self.wz_set)

    @pyqtSlot()
    def on_pushButton_left_set_clicked(self):
        self.vy_set += self.vyset_inc
        self.vy_set = self.constrain(self.vy_set, -10, 10)
        self.update_setvel_display()
        print('liner_vel_y_set: ', self.vy_set)
        self.protocol_speedset_send(self.vx_set, self.vy_set, self.wz_set)

    @pyqtSlot()
    def on_pushButton_right_set_clicked(self):
        self.vy_set -= self.vyset_inc
        self.vy_set = self.constrain(self.vy_set, -10, 10)
        self.update_setvel_display()
        print('liner_vel_y_set: ', self.vy_set)
        self.protocol_speedset_send(self.vx_set, self.vy_set, self.wz_set)

    @pyqtSlot()
    def on_pushButton_turn_left_set_clicked(self):
        self.wz_set += self.wzset_inc
        self.wz_set = self.constrain(self.wz_set, -5, 5)
        self.update_setvel_display()
        print('angular_vel_w_set: ', self.wz_set)
        self.protocol_speedset_send(self.vx_set, self.vy_set, self.wz_set)

    @pyqtSlot()
    def on_pushButton_turn_right_set_clicked(self):
        self.wz_set -= self.wzset_inc
        self.wz_set = self.constrain(self.wz_set, -5, 5)
        self.update_setvel_display()
        print('angular_vel_w_set: ', self.wz_set)
        self.protocol_speedset_send(self.vx_set, self.vy_set, self.wz_set)

    @pyqtSlot()
    def on_pushButton_stop_set_clicked(self):
        self.vx_set = 0.0
        self.vy_set = 0.0
        self.wz_set = 0.0
        self.update_setvel_display()
        print('on_pushButton_stop_set_clicked')
        self.protocol_speedset_send(self.vx_set, self.vy_set, self.wz_set)