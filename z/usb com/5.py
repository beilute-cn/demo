
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports
import time
import threading
from typing import Optional, Callable

class SerialCommunication:
    """串口通信类"""
    
    def __init__(self, port: str, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser: Optional[serial.Serial] = None
        self.running = False
        self.receive_callback: Optional[Callable] = None
    
    def open(self):
        """打开串口"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            print(f"✓ 串口 {self.port} 已打开 (波特率: {self.baudrate})")
            return True
        except serial.SerialException as e:
            print(f"✗ 打开串口失败: {e}")
            return False
    
    def close(self):
        """关闭串口"""
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"✓ 串口已关闭")
    
    def write(self, data: bytes):
        """写入数据"""
        if self.ser and self.ser.is_open:
            written = self.ser.write(data)
            print(f"✓ 发送 {written} 字节: {data.hex()}")
            return written
        return 0
    
    def write_string(self, text: str, encoding='utf-8'):
        """写入字符串"""
        data = text.encode(encoding)
        return self.write(data)
    
    def read(self, size=1) -> bytes:
        """读取指定字节数"""
        if self.ser and self.ser.is_open:
            data = self.ser.read(size)
            if data:
                print(f"✓ 接收 {len(data)} 字节: {data.hex()}")
            return data
        return b''
    
    def read_line(self, encoding='utf-8') -> str:
        """读取一行（以\n结尾）"""
        if self.ser and self.ser.is_open:
            line = self.ser.readline()
            if line:
                text = line.decode(encoding, errors='ignore').strip()
                print(f"✓ 接收行: {text}")
                return text
        return ''
    
    def read_all(self) -> bytes:
        """读取所有可用数据"""
        if self.ser and self.ser.is_open:
            data = self.ser.read(self.ser.in_waiting or 1)
            if data:
                print(f"✓ 接收 {len(data)} 字节: {data.hex()}")
            return data
        return b''
    
    def read_until(self, expected=b'\n', size=None) -> bytes:
        """读取直到遇到指定字符"""
        if self.ser and self.ser.is_open:
            data = self.ser.read_until(expected, size)
            if data:
                print(f"✓ 接收: {data.hex()}")
            return data
        return b''
    
    def start_reading_thread(self, callback: Callable[[bytes], None]):
        """启动后台读取线程"""
        self.receive_callback = callback
        self.running = True
        thread = threading.Thread(target=self._read_loop, daemon=True)
        thread.start()
        print("✓ 后台读取线程已启动")
    
    def _read_loop(self):
        """后台读取循环"""
        while self.running and self.ser and self.ser.is_open:
            if self.ser.in_waiting > 0:
                data = self.ser.read(self.ser.in_waiting)
                if data and self.receive_callback:
                    self.receive_callback(data)
            time.sleep(0.01)
    
    def get_status(self):
        """获取串口状态"""
        if not self.ser or not self.ser.is_open:
            return "串口未打开"
        
        return f"""
串口状态:
  端口: {self.ser.port}
  波特率: {self.ser.baudrate}
  已打开: {self.ser.is_open}
  接收缓冲: {self.ser.in_waiting} 字节
  发送缓冲: {self.ser.out_waiting} 字节
  CTS: {self.ser.cts}
  DSR: {self.ser.dsr}
  RI: {self.ser.ri}
  CD: {self.ser.cd}
"""


def demo_basic_rw():
    """基本读写演示"""
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("未检测到串口")
        return
    
    port = ports[0].device
    print(f"使用串口: {port}\n")
    
    comm = SerialCommunication(port, baudrate=115200)
    
    if comm.open():
        # 发送字符串
        comm.write_string("Hello Serial!\n")
        
        # 发送十六进制数据
        comm.write(b'\x01\x02\x03\x04')
        
        # 读取数据
        time.sleep(0.1)
        if comm.ser.in_waiting > 0:
            data = comm.read_all()
            print(f"收到数据: {data}")
        
        # 显示状态
        print(comm.get_status())
        
        comm.close()


def demo_continuous_read():
    """持续读取演示"""
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("未检测到串口")
        return
    
    port = ports[0].device
    print(f"使用串口: {port}\n")
    
    comm = SerialCommunication(port, baudrate=115200)
    
    def on_receive(data: bytes):
        """接收回调函数"""
        try:
            text = data.decode('utf-8', errors='ignore')
            print(f"[接收] {text.strip()} (HEX: {data.hex()})")
        except:
            print(f"[接收] HEX: {data.hex()}")
    
    if comm.open():
        # 启动后台读取
        comm.start_reading_thread(on_receive)
        
        # 持续发送数据
        try:
            for i in range(5):
                comm.write_string(f"Message {i}\n")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n中断")
        
        comm.close()


if __name__ == "__main__":
    print("="*60)
    print("串口读写演示")
    print("="*60)
    
    print("\n1. 基本读写演示")
    demo_basic_rw()
    
    print("\n2. 持续读取演示")
    # demo_continuous_read()  # 取消注释以运行
