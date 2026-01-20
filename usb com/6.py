#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports
import threading
import sys
import time

class SerialTerminal:
    """交互式串口终端"""
    
    def __init__(self):
        self.ser: Optional[serial.Serial] = None
        self.running = False
    
    def select_port(self):
        """选择串口"""
        ports = serial.tools.list_ports.comports()
        
        if not ports:
            print("未检测到串口设备")
            return None
        
        print("\n可用串口:")
        for idx, port in enumerate(ports, 1):
            chip = self.identify_chip(port.vid, port.pid)
            print(f"{idx}. {port.device} - {port.description} [{chip}]")
        
        while True:
            try:
                choice = input("\n选择串口 (输入序号): ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(ports):
                    return ports[idx].device
                print("无效选择")
            except (ValueError, KeyboardInterrupt):
                return None
    
    def identify_chip(self, vid, pid):
        """识别芯片"""
        chips = {
            (0x1A86, 0x7523): "CH340",
            (0x10C4, 0xEA60): "CP210x",
            (0x0403, 0x6001): "FTDI",
        }
        return chips.get((vid, pid), "Unknown")
    
    def configure_port(self):
        """配置串口参数"""
        print("\n串口配置:")
        
        baudrate = input("波特率 [115200]: ").strip() or "115200"
        bytesize = input("数据位 [8]: ").strip() or "8"
        parity = input("校验位 (N/E/O) [N]: ").strip().upper() or "N"
        stopbits = input("停止位 [1]: ").strip() or "1"
        
        parity_map = {'N': serial.PARITY_NONE, 'E': serial.PARITY_EVEN, 'O': serial.PARITY_ODD}
        
        return {
            'baudrate': int(baudrate),
            'bytesize': int(bytesize),
            'parity': parity_map.get(parity, serial.PARITY_NONE),
            'stopbits': float(stopbits),
            'timeout': 0.1,
        }
    
    def read_thread(self):
        """后台读取线程"""
        while self.running and self.ser and self.ser.is_open:
            try:
                if self.ser.in_waiting > 0:
                    data = self.ser.read(self.ser.in_waiting)
                    try:
                        text = data.decode('utf-8', errors='ignore')
                        print(f"\r[RX] {text}", end='', flush=True)
                    except:
                        print(f"\r[RX HEX] {data.hex()}", flush=True)
                time.sleep(0.01)
            except:
                break
    
    def run(self):
        """运行终端"""
        print("="*60)
        print("串口终端工具")
        print("="*60)
        
        port = self.select_port()
        if not port:
            return
        
        config = self.configure_port()
        
        try:
            self.ser = serial.Serial(port, **config)
            print(f"\n✓ 已连接到 {port}")
            print(f"配置: {config['baudrate']}bps, {config['bytesize']}N{config['stopbits']}")
            print("\n输入文本发送，输入 ':q' 退出，':h' 查看帮助\n")
            
            self.running = True
            thread = threading.Thread(target=self.read_thread, daemon=True)
            thread.start()
            
            while self.running:
                try:
                    text = input()
                    
                    if text == ':q':
                        break
                    elif text == ':h':
                        self.show_help()
                    elif text.startswith(':hex '):
                        hex_str = text[5:].replace(' ', '')
                        data = bytes.fromhex(hex_str)
                        self.ser.write(data)
                        print(f"[TX HEX] {data.hex()}")
                    else:
                        self.ser.write((text + '\n').encode('utf-8'))
                        print(f"[TX] {text}")
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"错误: {e}")
            
        except serial.SerialException as e:
            print(f"串口错误: {e}")
        finally:
            self.running = False
            if self.ser and self.ser.is_open:
                self.ser.close()
            print("\n已断开连接")
    
    def show_help(self):
        """显示帮助"""
        print("""
命令:
  :q          - 退出
  :h          - 帮助
  :hex XX XX  - 发送十六进制数据
  其他        - 发送文本 (自动添加换行)
""")


if __name__ == "__main__":
    terminal = SerialTerminal()
    terminal.run()
