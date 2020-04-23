import os
import sys
import threading
import time
import requests

import pymysql
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

class Device():
    def __init__(self,idx,module_idx,type=None,term=4):
        self.flag_run = False
        self.idx = idx
        self.module_idx = module_idx
        self.type = type
        self.term = term
        self.ppm = [0, 0, 0, 0, 0, 0];

class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = loadUi("generator_.ui", self)

        self.module_idx = ['202001','202002','202003','202004','202005']
        self.gas_type = ['Normal','H2S','NH3','CH3SH','CO','CO2','CH4']
        self.dev1_type.clear()
        self.dev2_type.clear()
        self.dev3_type.clear()
        self.dev4_type.clear()
        self.dev5_type.clear()
        self.dev1_type.addItems(self.gas_type)
        self.dev2_type.addItems(self.gas_type)
        self.dev3_type.addItems(self.gas_type)
        self.dev4_type.addItems(self.gas_type)
        self.dev5_type.addItems(self.gas_type)

        self.dev=[]
        for i in range(5):
            self.dev.append(Device(idx = i+1,module_idx=self.module_idx[i]))

        self.dev1_start.clicked.connect(lambda: self.Start_Signal(self.dev[0]))
        self.dev1_stop.clicked.connect(lambda:self.Stop_Signal(self.dev[0]))

        self.dev2_start.clicked.connect(lambda: self.Start_Signal(self.dev[1]))
        self.dev2_stop.clicked.connect(lambda: self.Stop_Signal(self.dev[1]))

        self.dev3_start.clicked.connect(lambda: self.Start_Signal(self.dev[2]))
        self.dev3_stop.clicked.connect(lambda: self.Stop_Signal(self.dev[2]))

        self.dev4_start.clicked.connect(lambda: self.Start_Signal(self.dev[3]))
        self.dev4_stop.clicked.connect(lambda: self.Stop_Signal(self.dev[3]))

        self.dev5_start.clicked.connect(lambda: self.Start_Signal(self.dev[4]))
        self.dev5_stop.clicked.connect(lambda: self.Stop_Signal(self.dev[4]))

        self.dev1_stop.setEnabled(False)
        self.dev2_stop.setEnabled(False)
        self.dev3_stop.setEnabled(False)
        self.dev4_stop.setEnabled(False)
        self.dev5_stop.setEnabled(False)

        self.create_thread=[]
        for i in range(5):
            self.create_thread.append(threading.Thread(target=self.Create_Data, args=(self.dev[i],)))
            self.create_thread[i].daemon = True
            self.create_thread[i].start()

    def Start_Signal(self,dev):

        if dev.module_idx == self.module_idx[0]:
            dev.type = str(self.dev1_type.currentText())
            tmp = self.line_ppm.text()
            if ((dev.type == 'Normal') or (dev.type != 'Normal' and tmp != '')):
                self.dev1_start.setEnabled(False)
                self.dev1_stop.setEnabled(True)
                self.dev1_type.setEnabled(False)
                self.line_ppm.setDisabled(True)
                dev.flag_run = True
        elif dev.module_idx == self.module_idx[1]:
            dev.type = str(self.dev2_type.currentText())
            tmp = self.line_ppm2.text()
            if ((dev.type == 'Normal') or (dev.type != 'Normal' and tmp != '')):
                self.dev2_start.setEnabled(False)
                self.dev2_stop.setEnabled(True)
                self.dev2_type.setEnabled(False)
                self.line_ppm2.setDisabled(True)
                dev.flag_run = True
        elif dev.module_idx == self.module_idx[2]:
            dev.type = str(self.dev3_type.currentText())
            tmp = self.line_ppm3.text()
            if ((dev.type == 'Normal') or (dev.type != 'Normal' and tmp != '')):
                self.dev3_start.setEnabled(False)
                self.dev3_stop.setEnabled(True)
                self.dev3_type.setEnabled(False)
                self.line_ppm3.setDisabled(True)
                dev.flag_run = True
        elif dev.module_idx == self.module_idx[3]:
            dev.type = str(self.dev4_type.currentText())
            tmp = self.line_ppm4.text()
            if ((dev.type == 'Normal') or (dev.type != 'Normal' and tmp != '')):
                self.dev4_start.setEnabled(False)
                self.dev4_stop.setEnabled(True)
                self.dev4_type.setEnabled(False)
                self.line_ppm4.setDisabled(True)
                dev.flag_run = True
        elif dev.module_idx == self.module_idx[4]:
            dev.type = str(self.dev5_type.currentText())
            tmp = self.line_ppm5.text()
            if ((dev.type == 'Normal') or (dev.type != 'Normal' and tmp != '')):
                self.dev5_start.setEnabled(False)
                self.dev5_stop.setEnabled(True)
                self.dev5_type.setEnabled(False)
                self.line_ppm5.setDisabled(True)
                dev.flag_run = True
        if dev.flag_run:
            txt = "Device" + str(dev.idx) + " : " + dev.type + " - Data Create Start"
            self.Log_Write(txt)

    def Stop_Signal(self,dev):
        dev.flag_run = False
        if dev.module_idx == self.module_idx[0]:
            self.dev1_start.setEnabled(True)
            self.dev1_stop.setEnabled(False)
            self.dev1_type.setEnabled(True)
            self.line_ppm.setEnabled(True)
        elif dev.module_idx == self.module_idx[1]:
            self.dev2_start.setEnabled(True)
            self.dev2_stop.setEnabled(False)
            self.dev2_type.setEnabled(True)
            self.line_ppm2.setEnabled(True)
        elif dev.module_idx == self.module_idx[2]:
            self.dev3_start.setEnabled(True)
            self.dev3_stop.setEnabled(False)
            self.dev3_type.setEnabled(True)
            self.line_ppm3.setEnabled(True)
        elif dev.module_idx == self.module_idx[3]:
            self.dev4_start.setEnabled(True)
            self.dev4_stop.setEnabled(False)
            self.dev4_type.setEnabled(True)
            self.line_ppm4.setEnabled(True)
        elif dev.module_idx == self.module_idx[4]:
            self.dev5_start.setEnabled(True)
            self.dev5_stop.setEnabled(False)
            self.dev5_type.setEnabled(True)
            self.line_ppm5.setEnabled(True)
        txt = "Device" + str(dev.idx) + " : " + dev.type + " - Data Create Stop"
        self.Log_Write(txt)

    def Create_Data(self,dev):
        while(1):
            if dev.flag_run:
                if dev.idx == 1:
                    text = self.line_ppm.text()
                elif dev.idx == 2:
                    text = self.line_ppm2.text()
                elif dev.idx == 3:
                    text = self.line_ppm3.text()
                elif dev.idx == 4:
                    text = self.line_ppm4.text()
                elif dev.idx == 5:
                    text = self.line_ppm5.text()

                if dev.type == 'Normal':
                    sen = [44, 44, 44, 44, 44, 44]
                    dev.ppm = [0,0,0,0,0,0]
                elif dev.type == 'H2S':
                    sen = [1, 1, 1, 1, 1, 1]
                    dev.ppm = [text,0,0,0,0,0]
                elif dev.type == 'NH3':
                    sen = [2, 2, 2, 2, 2, 2]
                    dev.ppm = [0, text,0,0,0,0]
                elif dev.type == 'CH3SH':
                    sen = [3, 3, 3, 3, 3, 3]
                    dev.ppm = [0,0,text,0,0,0]
                elif dev.type == 'CO':
                    sen = [4, 4, 4, 4, 4, 4]
                    dev.ppm = [0,0,0,text,0,0]
                elif dev.type == 'CO2':
                    sen = [370, 370, 370, 370, 370, 370]
                    dev.ppm = [0,0,0,0,text,0]
                elif dev.type == 'CH4':
                    sen = [6, 6, 6, 6, 6, 6]
                    dev.ppm = [0,0,0,0,0,text]
                # try:
                self.DB_Insert(dev)
                print(dev.idx,"inserted")
                # except Exception as e:
                #     print("insert Error")
                    # self.Log_Write("Network disconnected")
                time.sleep(dev.term)
            else:
                time.sleep(1)

    def DB_Insert(self,dev):
        # conn = pymysql.connect(host='192.168.0.157', port=3306, database='gas', user='root', password='ubimicro')
        # conn = pymysql.connect(host='192.168.2.2', port=3306, database='gas', user='root', password='ubimicro')
        # conn = pymysql.connect(host='203.250.78.169', port=3307, database='gas', user='root', password='offset01')
        # conn = pymysql.connect(host='106.252.240.216', port=23306, database='gas', user='root', password='ubimicro')
        conn = pymysql.connect(host='127.0.0.1', port=3307, database='gas_v2', user='root', password='offset01')
        with conn.cursor() as cursor:
            sql = 'INSERT INTO gas_log (gas_module_idx,tgs2600,tgs2602,tgs2603,tgs2610,tgs2620,tgs826) VALUES(%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (dev.module_idx,1,1,1,1,1,1))
            sql = 'INSERT INTO result_info (log_idx , ppm, ppm2, ppm3, ppm4, ppm5, ppm6) VALUES(LAST_INSERT_ID(),%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (dev.ppm[0], dev.ppm[1], dev.ppm[2], dev.ppm[3], dev.ppm[4], dev.ppm[5]))
        # with conn.cursor() as cursor:
        #     sql = 'INSERT INTO gas.gas_log (gas_module_idx,H2,VOC,Methyl,LP,Solvent,NH3) VALUES(%s,%s,%s,%s,%s,%s,%s);'
        #     cursor.execute(sql, (module_idx,sen[0],sen[1],sen[2],sen[3],sen[4],sen[5]))
        conn.commit()
        conn.close()

    def Log_Write(self,string):
        now = QtCore.QDateTime.currentDateTime().toString('yyyy.MM.dd - hh:mm:ss')
        self.lw_log.addItem(string+" ----------- "+now)
        self.lw_log.scrollToBottom()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    # window.showFullScreen()

    app.exec_()