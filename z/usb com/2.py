
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial.tools.list_ports
import time
import sys

try:
    import usb.core
    import usb.util
    USB_AVAILABLE = True
except ImportError:
    USB_AVAILABLE = False
    print("警告: pyusb未安装，部分功能受限")
    print("安装命令: pip install pyusb")

class AdvancedUSBMonitor:
    def __init__(self):
        self.current_serial_devices = {}
        self.current_usb_devices = {}
        
    def get_all_usb_devices(self):
        """获取所有USB设备（使用pyusb）"""
        if not USB_AVAILABLE:
            return {}
        
        devices = {}
        try:
            usb_devices = usb.core.find(find_all=True)
            for dev in usb_devices:
                key = f"{dev.idVendor:04x}:{dev.idProduct:04x}:{dev.bus}:{dev.address}"
                devices[key] = {
                    'vid': dev.idVendor,
                    'pid': dev.idProduct,
                    'bus': dev.bus,
                    'address': dev.address,
                    'manufacturer': usb.util.get_string(dev, dev.iManufacturer) if dev.iManufacturer else None,
                    'product': usb.util.get_string(dev, dev.iProduct) if dev.iProduct else None,
                    'serial': usb.util.get_string(dev, dev.iSerialNumber) if dev.iSerialNumber else None,
                }
        except Exception as e:
            print(f"读取USB设备时出错: {e}")
        
        return devices
    
    def get_serial_devices(self):
        """获取所有串口设备"""
        devices = {}
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
            devices[port.device] = {
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
            }
        
        return devices
    
    def display_serial_devices(self, devices):
        """显示串口设备"""
        print("\n📱 串口设备列表:")
        print("-" * 60)
        
        if not devices:
            print("  (无串口设备)")
        else:
            for idx, (key, info) in enumerate(devices.items(), 1):
                print(f"\n[串口 {idx}] {info['device']}")
                if info['description']:
                    print(f"  描述: {info['description']}")
                if info['vid'] and info['pid']:
                    print(f"  VID:PID = {info['vid']:04X}:{info['pid']:04X}")
                if info['manufacturer']:
                    print(f"  制造商: {info['manufacturer']}")
                if info['product']:
                    print(f"  产品: {info['product']}")
                if info['serial_number']:
                    print(f"  序列号: {info['serial_number']}")
    
    def monitor(self):
        """监控设备变化"""
        print("="*60)
        print("USB设备监控程序 (按 Ctrl+C 退出)")
        print("="*60)
        
        self.current_serial_devices = self.get_serial_devices()
        self.display_serial_devices(self.current_serial_devices)
        
        try:
            while True:
                time.sleep(0.5)
                new_serial = self.get_serial_devices()
                
                added = set(new_serial.keys()) - set(self.current_serial_devices.keys())
                removed = set(self.current_serial_devices.keys()) - set(new_serial.keys())
                
                if added:
                    print("\n\n✅ 设备已连接:")
                    for dev in added:
                        info = new_serial[dev]
                        print(f"  → {dev}")
                        if info['description']:
                            print(f"    {info['description']}")
                
                if removed:
                    print("\n\n❌ 设备已断开:")
                    for dev in removed:
                        print(f"  → {dev}")
                
                if added or removed:
                    self.current_serial_devices = new_serial
                    
        except KeyboardInterrupt:
            print("\n\n程序已退出")

if __name__ == "__main__":
    monitor = AdvancedUSBMonitor()
    monitor.monitor()
