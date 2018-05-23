#coding=gb18030

import threading
import time
import serial


class ComThread:
    def __init__(self, Port='COM3'):
        self.l_serial = None
        self.alive = False
        self.waitEnd = None
        self.port = Port
        self.data = ''


    def waiting(self):
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def SetStopEvent(self):
        if not self.waitEnd is None:
            self.waitEnd.set()
        self.alive = False
        self.stop()

    def start(self):
        global temperature
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = 115200
        self.l_serial.timeout = 2
        self.l_serial.open()
        if self.l_serial.isOpen():
            self.waitEnd = threading.Event()
            self.alive = True
            self.thread_read = None
            self.thread_read = threading.Thread(target=self.FirstReader)
            self.thread_read.setDaemon(1)
            self.thread_read.start()
            return True
        else:
            return False

    def FirstReader(self):
        global temperature
        while self.alive:
            time.sleep(0.1)
            tempdata=''
            tempdata = tempdata.encode('utf-8')

            n = self.l_serial.inWaiting()
            if n:
                #输出串口接收到的数值
                 print(self.get_result())
                 fd = open("mydata.txt", "w+")  # 读取方式打开，清除文件原来内容
                 fd.write(self.get_result())
                 fd.close()
                 tempdata = tempdata + self.l_serial.read(n)
                #输出串口未编码之前的数值
                 #print('get data from serial port:', tempdata)
                 #print(type(tempdata))
                 self.data=tempdata.decode('gb18030')
            n = self.l_serial.inWaiting()
            #if len(data)>0 and n==0:
            #    try:
            #        temp = data.decode('gb18030')
            #        print(type(temp))
            #        print(temp)
            #    except:
            #        print("读卡错误，请重试！\n")

        self.waitEnd.set()
        self.alive = False

    def get_result(self):
        return self.data

    def stop(self):
        self.alive = False
        self.thread_read.join()
        if self.l_serial.isOpen():
            self.l_serial.close()





'''if __name__ == '__main__':

   # 调用串口，测试串口
    db.drop_all()
    db.create_all()
    temperature= Temperature('Mytemperature')
    db.session.add(temperature)
    db.session.commit()
    rt = ComThread()
    try:
        if rt.start():
            print(rt.l_serial.name)
            rt.waiting()
            rt.stop()
        else:
            pass
    except Exception as se:
        print(str(se))

    if rt.alive:
        rt.stop()
    del rt

'''