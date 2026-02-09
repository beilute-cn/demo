import win32com.client
import time
import random
from datetime import datetime
import os


def real_time_dashboard(file_path, duration=60):
    """
    方法2: 创建实时更新的仪表板
    """
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True

        # 打开或创建工作簿
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

        # 设置表头样式
        header_range = worksheet.Range("A1:D1")
        header_range.Font.Bold = True
        header_range.Interior.Color = 0x4472C4  # 蓝色背景
        header_range.Font.Color = 0xFFFFFF  # 白色字体

        # 实时更新数据
        start_time = time.time()
        row = 2

        print(f"开始实时更新，持续 {duration} 秒...")

        while time.time() - start_time < duration:
            # 生成模拟数据
            current_time = datetime.now().strftime("%H:%M:%S")
            temperature = round(random.uniform(20, 30), 1)
            humidity = round(random.uniform(40, 60), 1)
            status = "正常" if temperature < 28 else "警告"

            # 更新单元格
            worksheet.Cells(row, 1).Value = current_time
            worksheet.Cells(row, 2).Value = temperature
            worksheet.Cells(row, 3).Value = humidity
            worksheet.Cells(row, 4).Value = status

            # 如果温度过高，标红
            if temperature >= 28:
                worksheet.Cells(row, 2).Interior.Color = 0x0000FF  # 红色

            # 自动调整列宽
            worksheet.Columns.AutoFit()

            print(
                f"行 {row}: {current_time} - 温度: {temperature}°C, 湿度: {humidity}%"
            )

            row += 1
            time.sleep(2)  # 每2秒更新一次

        # 保存工作簿
        workbook.Save()
        print("更新完成并已保存！")

    except Exception as e:
        print(f"错误: {e}")


# 使用示例
real_time_dashboard("example.xlsx", duration=30)
