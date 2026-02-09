import win32com.client
import time
import random
from datetime import datetime
import os
import pywintypes
from win32com.client import constants


def real_time_dashboard_optimized(file_path, duration=60):
    """
    优化版：禁用屏幕更新和事件，减少冲突
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
        header_range.Interior.Color = 0x4472C4
        header_range.Font.Color = 0xFFFFFF

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

            try:
                # 临时禁用屏幕更新和事件（提高性能，减少冲突）
                excel.ScreenUpdating = False
                excel.EnableEvents = False
                
                # 更新单元格
                worksheet.Cells(row, 1).Value = current_time
                worksheet.Cells(row, 2).Value = temperature
                worksheet.Cells(row, 3).Value = humidity
                worksheet.Cells(row, 4).Value = status

                # 如果温度过高，标红
                if temperature >= 28:
                    worksheet.Cells(row, 2).Interior.Color = 0x0000FF

                print(f"行 {row}: {current_time} - 温度: {temperature}°C, 湿度: {humidity}%")
                
            except pywintypes.com_error as e:
                if 1 or e.args[0] == -2147418111:
                    print(f"  Excel正忙，跳过行 {row}")
                else:
                    print(f"  错误: {e}")
            finally:
                # 恢复屏幕更新和事件
                excel.ScreenUpdating = True
                excel.EnableEvents = True

            row += 1
            time.sleep(2)

        # 最后调整列宽
        try:
            worksheet.Columns.AutoFit()
        except:
            pass

        # 保存工作簿
        try:
            workbook.Save()
            print("更新完成并已保存！")
        except:
            print("保存失败，请手动保存")

    except Exception as e:
        print(f"错误: {e}")


# 使用示例
real_time_dashboard_optimized("example.xlsx", duration=30)
