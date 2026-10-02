"""串口通信类：封装连接设备、发送命令、读取成绩和关闭连接。

目前 main.py 直接处理串口，并未使用此类。它可以作为后续重构的练习。
不要同时创建此类实例并运行 main.py 的串口连接，两者会使用同一个端口。
"""

import serial
import time


class ArduinoSerial:
    def __init__(self, port="COM5", baudrate=9600):
        # __init__ 在创建实例时调用；self 保存当前实例的数据。
        self.arduino = serial.Serial(port, baudrate)
        # 部分 Arduino 打开串口后会复位，等待两秒让它完成初始化。
        time.sleep(2)

    def start_test(self):
        """发送开始命令，换行符用于标记命令结束。"""
        self.arduino.write(b"START\n")

    def read_result(self):
        """等待 TIME:数字 格式的响应，返回整数毫秒数。"""
        while True:
            # 未设置串口超时：设备不返回数据时，这里会持续等待。
            data = self.arduino.readline()
            text = data.decode().strip()
            if text.startswith("TIME:"):
                result = text.split(":")[1]
                return int(result)

    def close(self):
        """释放串口，让其他程序也能连接这个设备。"""
        if self.arduino.is_open:
            self.arduino.close()
