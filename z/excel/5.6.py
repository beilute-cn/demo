import win32com.client
import time
import random
from datetime import datetime
import os
import pywintypes


def safe_excel_update(worksheet, row, col, value, max_retries=3):
    """安全的Excel单元格更新函数"""
    for attempt in range(max_retries):
        try:
            worksheet.Cells(row, col).Value = value
            return True
        except pywintypes.com_error as e:
            if e.args[0] == -2147418111:  # Call was rejected
                if attempt < max_retries - 1:
                    time.sleep(0.3)
                else:
                    return False
            else:
                raise
    return False


def real_time_dashboard(file_path, duration=60):
    """
    推荐方案：结合重试机制和性能优化
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
            safe_excel_update(worksheet, 1, col, header)

        header_range = worksheet.Range("A1:D1")
        header_range.Font.Bold = True
        header_range.Interior.Color = 0x4472C4
        header_range.Font.Color = 0xFFFFFF

        start_time = time.time()
        row = 2
        failed_updates = 0

        print(f"开始实时更新，持续 {duration} 秒...")
        print("提示: 更新期间可以查看Excel，但避免长时间编辑单元格\n")

        while time.time() - start_time < duration:
            current_time = datetime.now().strftime("%H:%M:%S")
            temperature = round(random.uniform(20, 30), 1)
            humidity = round(random.uniform(40, 60), 1)
            status = "正常" if temperature < 28 else "警告"

            # 使用安全更新函数
            success = True
            success &= safe_excel_update(worksheet, row, 1, current_time)
            success &= safe_excel_update(worksheet, row, 2, temperature)
            success &= safe_excel_update(worksheet, row, 3, humidity)
            success &= safe_excel_update(worksheet, row, 4, status)

            if success:
                if temperature >= 28:
                    try:
                        worksheet.Cells(row, 2).Interior.Color = 0x0000FF
                    except:
                        pass
                print(f"✓ 行 {row}: {current_time} - 温度: {temperature}°C, 湿度: {humidity}%")
            else:
                failed_updates += 1
                print(f"✗ 行 {row}: 更新失败（Excel正忙）")

            row += 1
            time.sleep(2)

        # 最终处理
        try:
            worksheet.Columns.AutoFit()
            workbook.Save()
            print(f"\n更新完成并已保存！")
            print(f"成功: {row - 2 - failed_updates} 行, 失败: {failed_updates} 行")
        except:
            print("保存失败，请手动保存")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


# 使用示例
real_time_dashboard("example.xlsx", duration=30)
