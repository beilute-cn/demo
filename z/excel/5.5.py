import win32com.client
import time
import random
from datetime import datetime
import os
import pythoncom


def real_time_dashboard_with_message_filter(file_path, duration=60):
    """
    使用消息过滤器处理COM调用
    """
    try:
        # 初始化COM
        pythoncom.CoInitialize()
        
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True

        try:
            workbook = excel.Workbooks.Open(os.path.abspath(file_path))
        except:
            workbook = excel.Workbooks.Add()
            workbook.SaveAs(os.path.abspath(file_path))

        worksheet = workbook.Worksheets(1)

        # 设置表头
        worksheet.Cells(1, 1).Value = "时间"
        worksheet.Cells(1, 2).Value = "温度(°C)"
        worksheet.Cells(1, 3).Value = "湿度(%)"
        worksheet.Cells(1, 4).Value = "状态"

        header_range = worksheet.Range("A1:D1")
        header_range.Font.Bold = True
        header_range.Interior.Color = 0x4472C4
        header_range.Font.Color = 0xFFFFFF

        start_time = time.time()
        row = 2

        print(f"开始实时更新，持续 {duration} 秒...")

        while time.time() - start_time < duration:
            current_time = datetime.now().strftime("%H:%M:%S")
            temperature = round(random.uniform(20, 30), 1)
            humidity = round(random.uniform(40, 60), 1)
            status = "正常" if temperature < 28 else "警告"

            retry_count = 0
            max_retries = 5
            
            while retry_count < max_retries:
                try:
                    # 处理待处理的消息
                    pythoncom.PumpWaitingMessages()
                    
                    worksheet.Cells(row, 1).Value = current_time
                    worksheet.Cells(row, 2).Value = temperature
                    worksheet.Cells(row, 3).Value = humidity
                    worksheet.Cells(row, 4).Value = status

                    if temperature >= 28:
                        worksheet.Cells(row, 2).Interior.Color = 0x0000FF

                    print(f"行 {row}: {current_time} - 温度: {temperature}°C, 湿度: {humidity}%")
                    break
                    
                except pythoncom.com_error as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.2)
                    else:
                        print(f"  跳过行 {row}（重试失败）")

            row += 1
            time.sleep(2)

        try:
            worksheet.Columns.AutoFit()
            workbook.Save()
            print("更新完成并已保存！")
        except:
            print("保存失败")

        pythoncom.CoUninitialize()

    except Exception as e:
        print(f"错误: {e}")


# 使用示例
real_time_dashboard_with_message_filter("example.xlsx", duration=30)
