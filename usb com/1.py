#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial.tools.list_ports
import time
import threading
from datetime import datetime

class USBMonitor:
    def __init__(self):
        self.current_devices = {}
        self.running = False
        
    def get_device_info(self, port):
        """获取USB串口设备的详细信息"""
        info = {
            'device': port.device,
            'name': port.name,
            'description': port.description,
            'hwid': port.hwid,
            'vid': port.vid,  # Vendor ID
            'pid': port.pid,  # Product ID
            'serial_number': port.serial_number,
            'location': port.location,
            'manufacturer': port.manufacturer,
            'product': port.product,
            'interface': port.interface,
        }
        return info
    
    def format_device_info(self, info):
        """格式化设备信息用于显示"""
        lines = [
            f"  设备路径: {info['device']}",
            f"  设备名称: {info['name']}",
            f"  描述: {info['description']}",
            f"  硬件ID: {info['hwid']}",
        ]
        
        if info['vid'] is not None:
            lines.append(f"  VID: 0x{info['vid']:04X}")
        if info['pid'] is not None:
            lines.append(f"  PID: 0x{info['pid']:04X}")
        if info['serial_number']:
            lines.append(f"  序列号: {info['serial_number']}")
        if info['manufacturer']:
            lines.append(f"  制造商: {info['manufacturer']}")
        if info['product']:
            lines.append(f"  产品名: {info['product']}")
        if info['location']:
            lines.append(f"  位置: {info['location']}")
        if info['interface']:
            lines.append(f"  接口: {info['interface']}")
            
        return '\n'.join(lines)
    
    def scan_devices(self):
        """扫描当前所有USB串口设备"""
        devices = {}
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
            # 只关注USB设备
            if 'USB' in port.hwid or port.vid is not None:
                device_key = port.device
                devices[device_key] = self.get_device_info(port)
        
        return devices
    
    def display_all_devices(self, devices):
        """显示所有设备"""
        print("\n" + "="*60)
        print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"检测到 {len(devices)} 个USB串口设备:")
        print("="*60)
        
        if not devices:
            print("  (无设备)")
        else:
            for idx, (key, info) in enumerate(devices.items(), 1):
                print(f"\n[设备 {idx}]")
                print(self.format_device_info(info))
        
        print("="*60)
    
    def monitor(self, interval=1.0):
        """监控USB设备的热插拔"""
        print("USB串口设备监控程序启动...")
        print("按 Ctrl+C 退出\n")
        
        self.running = True
        self.current_devices = self.scan_devices()
        self.display_all_devices(self.current_devices)
        
        try:
            while self.running:
                time.sleep(interval)
                new_devices = self.scan_devices()
                
                # 检测新增设备
                added = set(new_devices.keys()) - set(self.current_devices.keys())
                # 检测移除设备
                removed = set(self.current_devices.keys()) - set(new_devices.keys())
                
                if added or removed:
                    if added:
                        print("\n" + "🔌 " + "="*58)
                        print(f"检测到新设备插入 ({datetime.now().strftime('%H:%M:%S')})")
                        print("="*60)
                        for device_key in added:
                            print(f"\n[新增设备: {device_key}]")
                            print(self.format_device_info(new_devices[device_key]))
                        print("="*60)
                    
                    if removed:
                        print("\n" + "🔌 " + "="*58)
                        print(f"检测到设备移除 ({datetime.now().strftime('%H:%M:%S')})")
                        print("="*60)
                        for device_key in removed:
                            print(f"\n[移除设备: {device_key}]")
                            print(self.format_device_info(self.current_devices[device_key]))
                        print("="*60)
                    
                    self.current_devices = new_devices
                    
        except KeyboardInterrupt:
            print("\n\n程序已停止")
            self.running = False

def main():
    monitor = USBMonitor()
    monitor.monitor(interval=0.5)  # 每0.5秒检测一次

if __name__ == "__main__":
    main()
