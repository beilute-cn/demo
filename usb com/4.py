#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports
from typing import Optional, Dict
import time

class SerialConfig:
    """串口配置管理类"""
    
    # 常用波特率
    COMMON_BAUDRATES = [
        300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 
        38400, 57600, 115200, 230400, 460800, 921600
    ]
    
    # 数据位
    BYTESIZE_OPTIONS = {
        5: serial.FIVEBITS,
        6: serial.SIXBITS,
        7: serial.SEVENBITS,
        8: serial.EIGHTBITS,
    }
    
    # 校验位
    PARITY_OPTIONS = {
        'N': serial.PARITY_NONE,    # 无校验
        'E': serial.PARITY_EVEN,    # 偶校验
        'O': serial.PARITY_ODD,     # 奇校验
        'M': serial.PARITY_MARK,    # 标记校验
        'S': serial.PARITY_SPACE,   # 空格校验
    }
    
    # 停止位
    STOPBITS_OPTIONS = {
        1: serial.STOPBITS_ONE,
        1.5: serial.STOPBITS_ONE_POINT_FIVE,
        2: serial.STOPBITS_TWO,
    }
    
    def __init__(self, port: str):
        """初始化串口配置"""
        self.port = port
        self.ser: Optional[serial.Serial] = None
    
    def open(self, baudrate=9600, bytesize=8, parity='N', stopbits=1, 
             timeout=1, xonxoff=False, rtscts=False, dsrdtr=False):
        """打开串口并设置参数"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=baudrate,
                bytesize=self.BYTESIZE_OPTIONS.get(bytesize, serial.EIGHTBITS),
                parity=self.PARITY_OPTIONS.get(parity, serial.PARITY_NONE),
                stopbits=self.STOPBITS_OPTIONS.get(stopbits, serial.STOPBITS_ONE),
                timeout=timeout,
                xonxoff=xonxoff,      # 软件流控
                rtscts=rtscts,        # 硬件流控(RTS/CTS)
                dsrdtr=dsrdtr,        # 硬件流控(DSR/DTR)
            )
            print(f"✓ 串口 {self.port} 已打开")
            return True
        except serial.SerialException as e:
            print(f"✗ 打开串口失败: {e}")
            return False
    
    def close(self):
        """关闭串口"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"✓ 串口 {self.port} 已关闭")
    
    def get_current_config(self) -> Dict:
        """获取当前串口配置"""
        if not self.ser or not self.ser.is_open:
            return {}
        
        # 反向查找
        parity_name = {v: k for k, v in self.PARITY_OPTIONS.items()}.get(
            self.ser.parity, 'Unknown'
        )
        
        stopbits_name = {v: k for k, v in self.STOPBITS_OPTIONS.items()}.get(
            self.ser.stopbits, 'Unknown'
        )
        
        config = {
            'port': self.ser.port,
            'baudrate': self.ser.baudrate,
            'bytesize': self.ser.bytesize,
            'parity': parity_name,
            'stopbits': stopbits_name,
            'timeout': self.ser.timeout,
            'write_timeout': self.ser.write_timeout,
            'inter_byte_timeout': self.ser.inter_byte_timeout,
            'xonxoff': self.ser.xonxoff,
            'rtscts': self.ser.rtscts,
            'dsrdtr': self.ser.dsrdtr,
            'is_open': self.ser.is_open,
            'in_waiting': self.ser.in_waiting,      # 接收缓冲区字节数
            'out_waiting': self.ser.out_waiting,    # 发送缓冲区字节数
        }
        
        # 获取控制线状态
        try:
            config['cts'] = self.ser.cts  # Clear To Send
            config['dsr'] = self.ser.dsr  # Data Set Ready
            config['ri'] = self.ser.ri    # Ring Indicator
            config['cd'] = self.ser.cd    # Carrier Detect
        except:
            pass
        
        return config
    
    def display_config(self):
        """显示当前配置"""
        config = self.get_current_config()
        
        if not config:
            print("串口未打开")
            return
        
        print("\n" + "="*50)
        print(f"串口配置: {config['port']}")
        print("="*50)
        print(f"  波特率: {config['baudrate']}")
        print(f"  数据位: {config['bytesize']}")
        print(f"  校验位: {config['parity']}")
        print(f"  停止位: {config['stopbits']}")
        print(f"  超时: {config['timeout']}s")
        print(f"  软件流控(XON/XOFF): {config['xonxoff']}")
        print(f"  硬件流控(RTS/CTS): {config['rtscts']}")
        print(f"  硬件流控(DSR/DTR): {config['dsrdtr']}")
        print(f"  状态: {'已打开' if config['is_open'] else '已关闭'}")
        print(f"  接收缓冲区: {config['in_waiting']} 字节")
        print(f"  发送缓冲区: {config['out_waiting']} 字节")
        
        if 'cts' in config:
            print(f"\n控制线状态:")
            print(f"  CTS: {config['cts']}")
            print(f"  DSR: {config['dsr']}")
            print(f"  RI: {config['ri']}")
            print(f"  CD: {config['cd']}")
        
        print("="*50)
    
    def set_baudrate(self, baudrate: int):
        """设置波特率"""
        if self.ser and self.ser.is_open:
            self.ser.baudrate = baudrate
            print(f"✓ 波特率已设置为: {baudrate}")
    
    def set_timeout(self, timeout: float):
        """设置超时时间"""
        if self.ser and self.ser.is_open:
            self.ser.timeout = timeout
            print(f"✓ 超时已设置为: {timeout}s")
    
    def set_dtr(self, state: bool):
        """设置DTR信号"""
        if self.ser and self.ser.is_open:
            self.ser.dtr = state
            print(f"✓ DTR已设置为: {state}")
    
    def set_rts(self, state: bool):
        """设置RTS信号"""
        if self.ser and self.ser.is_open:
            self.ser.rts = state
            print(f"✓ RTS已设置为: {state}")
    
    def reset_input_buffer(self):
        """清空接收缓冲区"""
        if self.ser and self.ser.is_open:
            self.ser.reset_input_buffer()
            print("✓ 接收缓冲区已清空")
    
    def reset_output_buffer(self):
        """清空发送缓冲区"""
        if self.ser and self.ser.is_open:
            self.ser.reset_output_buffer()
            print("✓ 发送缓冲区已清空")
    
    def send_break(self, duration=0.25):
        """发送BREAK信号"""
        if self.ser and self.ser.is_open:
            self.ser.send_break(duration)
            print(f"✓ 已发送BREAK信号 ({duration}s)")


def main():
    # 列出所有串口
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("未检测到串口设备")
        return
    
    print("可用串口:")
    for idx, port in enumerate(ports, 1):
        print(f"{idx}. {port.device} - {port.description}")
    
    # 选择第一个串口进行演示
    selected_port = ports[0].device
    print(f"\n使用串口: {selected_port}")
    
    # 创建配置对象
    config = SerialConfig(selected_port)
    
    # 打开串口
    if config.open(baudrate=115200, bytesize=8, parity='N', stopbits=1):
        # 显示配置
        config.display_config()
        
        # 修改配置
        print("\n修改配置...")
        config.set_baudrate(9600)
        config.set_timeout(2.0)
        config.set_dtr(True)
        config.set_rts(True)
        
        # 再次显示配置
        config.display_config()
        
        # 清空缓冲区
        config.reset_input_buffer()
        config.reset_output_buffer()
        
        # 关闭串口
        config.close()


if __name__ == "__main__":
    main()
