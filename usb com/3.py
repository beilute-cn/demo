#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports
import time
from typing import List, Dict, Optional

class SerialIdentifier:
    """串口识别和属性管理类"""
    
    # 常见的USB转串口芯片VID:PID
    KNOWN_CHIPS = {
        (0x1A86, 0x7523): "CH340",
        (0x1A86, 0x5523): "CH341",
        (0x10C4, 0xEA60): "CP210x",
        (0x0403, 0x6001): "FTDI FT232",
        (0x0403, 0x6010): "FTDI FT2232",
        (0x0403, 0x6011): "FTDI FT4232",
        (0x0403, 0x6014): "FTDI FT232H",
        (0x067B, 0x2303): "PL2303",
        (0x2341, 0x0043): "Arduino Uno",
        (0x2341, 0x0001): "Arduino Mega",
        (0x239A, None): "Adafruit",
    }
    
    @staticmethod
    def identify_chip(vid: int, pid: int) -> str:
        """识别串口芯片类型"""
        if vid is None or pid is None:
            return "未知"
        
        # 精确匹配
        if (vid, pid) in SerialIdentifier.KNOWN_CHIPS:
            return SerialIdentifier.KNOWN_CHIPS[(vid, pid)]
        
        # VID匹配
        for (v, p), name in SerialIdentifier.KNOWN_CHIPS.items():
            if v == vid and p is None:
                return name
        
        return f"未知 (VID:PID = {vid:04X}:{pid:04X})"
    
    @staticmethod
    def list_all_ports() -> List[Dict]:
        """列出所有串口及其详细信息"""
        ports = serial.tools.list_ports.comports()
        port_list = []
        
        for port in ports:
            chip_type = SerialIdentifier.identify_chip(port.vid, port.pid)
            
            port_info = {
                'device': port.device,
                'name': port.name,
                'description': port.description,
                'hwid': port.hwid,
                'vid': port.vid,
                'pid': port.pid,
                'serial_number': port.serial_number,
                'location': port.location,
                'manufacturer': port.manufacturer,
                'product': port.product,
                'interface': port.interface,
                'chip_type': chip_type,
            }
            port_list.append(port_info)
        
        return port_list
    
    @staticmethod
    def display_ports(ports: List[Dict]):
        """显示所有串口信息"""
        print("\n" + "="*70)
        print(f"检测到 {len(ports)} 个串口设备")
        print("="*70)
        
        for idx, port in enumerate(ports, 1):
            print(f"\n[串口 {idx}]")
            print(f"  设备路径: {port['device']}")
            print(f"  芯片类型: {port['chip_type']}")
            print(f"  描述: {port['description']}")
            
            if port['vid'] and port['pid']:
                print(f"  VID:PID: {port['vid']:04X}:{port['pid']:04X}")
            
            if port['manufacturer']:
                print(f"  制造商: {port['manufacturer']}")
            if port['product']:
                print(f"  产品: {port['product']}")
            if port['serial_number']:
                print(f"  序列号: {port['serial_number']}")
            if port['location']:
                print(f"  位置: {port['location']}")
            
            print(f"  硬件ID: {port['hwid']}")
        
        print("="*70)
    
    @staticmethod
    def find_port_by_vid_pid(vid: int, pid: int) -> Optional[str]:
        """根据VID和PID查找串口"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == vid and port.pid == pid:
                return port.device
        return None
    
    @staticmethod
    def find_port_by_serial_number(serial_number: str) -> Optional[str]:
        """根据序列号查找串口"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.serial_number == serial_number:
                return port.device
        return None
    
    @staticmethod
    def find_port_by_description(keyword: str) -> List[str]:
        """根据描述关键字查找串口"""
        ports = serial.tools.list_ports.comports()
        matched = []
        for port in ports:
            if keyword.lower() in port.description.lower():
                matched.append(port.device)
        return matched


def main():
    identifier = SerialIdentifier()
    ports = identifier.list_all_ports()
    identifier.display_ports(ports)
    
    # 示例：查找特定设备
    print("\n示例查找:")
    ch340_port = identifier.find_port_by_vid_pid(0x1A86, 0x7523)
    if ch340_port:
        print(f"找到CH340设备: {ch340_port}")
    
    arduino_ports = identifier.find_port_by_description("Arduino")
    if arduino_ports:
        print(f"找到Arduino设备: {arduino_ports}")


if __name__ == "__main__":
    main()
