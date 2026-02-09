import win32com.client
import time
import random
from datetime import datetime
import os
import pywintypes


def real_time_dashboard_batch(file_path, duration=60, batch_size=5):
    """
    批量更新版：收集多行数据后一次性写入
    """
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True

        try:
            workbook = excel.Workbooks.Open(os.path.abspath(file_path))
        except:
            workbook = excel.Workbooks.Add()
            workbook.SaveAs(os.path.abspath(file_path))

        worksheet = workbook.Worksheets(1)

        # 设置表头
        headers = ["时间", "温度(°C)", "湿度(%)", "状态"]
        for col, header in enumerate(headers, 1):
            worksheet.Cells(1, col).Value = header

        header_range = worksheet.Range("A1:D1")
        header_range.Font.Bold = True
        header_range.Interior.Color = 0x4472C4
        header_range.Font.Color = 0xFFFFFF

        start_time = time.time()
        row = 2
        batch_data = []

        print(f"开始实时更新，持续 {duration} 秒...")
        print(f"批量大小: {batch_size} 行")

        while time.time() - start_time < duration:
            # 生成模拟数据
            current_time = datetime.now().strftime("%H:%M:%S")
            temperature = round(random.uniform(20, 30), 1)
            humidity = round(random.uniform(40, 60), 1)
            status = "正常" if temperature < 28 else "警告"

            # 收集数据
            batch_data.append({
                'row': row,
                'data': [current_time, temperature, humidity, status],
                'highlight': temperature >= 28
            })

            print(f"收集行 {row}: {current_time} - 温度: {temperature}°C, 湿度: {humidity}%")

            # 当收集够一批或时间到了，批量写入
            if len(batch_data) >= batch_size or time.time() - start_time >= duration:
                try:
                    excel.ScreenUpdating = False
                    
                    for item in batch_data:
                        for col, value in enumerate(item['data'], 1):
                            worksheet.Cells(item['row'], col).Value = value
                        
                        if item['highlight']:
                            worksheet.Cells(item['row'], 2).Interior.Color = 0x0000FF
                    
                    excel.ScreenUpdating = True
                    print(f"✓ 已写入 {len(batch_data)} 行")
                    batch_data = []
                    
                except pywintypes.com_error as e:
                    if e.args[0] == -2147418111:
                        print(f"  Excel正忙，稍后重试...")
                        time.sleep(1)
                        continue
                    else:
                        raise

            row += 1
            time.sleep(2)

        # 写入剩余数据
        if batch_data:
            try:
                for item in batch_data:
                    for col, value in enumerate(item['data'], 1):
                        worksheet.Cells(item['row'], col).Value = value
                print(f"✓ 已写入剩余 {len(batch_data)} 行")
            except:
                pass

        # 调整列宽并保存
        try:
            worksheet.Columns.AutoFit()
            workbook.Save()
            print("更新完成并已保存！")
        except:
            print("保存失败，请手动保存")

    except Exception as e:
        print(f"错误: {e}")


# 使用示例
real_time_dashboard_batch("example.xlsx", duration=30, batch_size=3)
