import time
import win32com.client
import os


import random

"""
方法1: 使用win32com动态更新已打开的Excel
需要安装: pip install pywin32
"""
abs_path = os.path.abspath("example.xlsx")

try:
    # 连接到已运行的Excel应用程序
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True

    # 查找已打开的工作簿
    workbook = None
    for wb in excel.Workbooks:
        if wb.FullName.lower() == abs_path.lower():
            workbook = wb
            break

    # 如果文件未打开，则打开它
    if workbook is None:
        workbook = excel.Workbooks.Open(abs_path)
        print(f"已打开文件: {abs_path}")
    else:
        print(f"找到已打开的文件: {abs_path}")

    # 获取工作表
    worksheet = workbook.Worksheets(1)  # 第一个工作表

    # 方法1: 清除所有已使用的单元格
    worksheet.UsedRange.Clear()  # 清除内容和格式

    # 或者只清除内容，保留格式
    # worksheet.UsedRange.ClearContents()

    # 为A1到Z26整个区域添加粗黑色边框
    range_area = worksheet.Range("A1:Z26")

    # 设置外边框
    range_area.BorderAround(
        LineStyle=1,  # xlContinuous (实线)
        Weight=4,  # xlThick (粗线)
        Color=0x000000,  # 黑色
    )

    if False:
        # 或者设置所有边框（包括内部网格线）
        for border in range_area.Borders:
            border.LineStyle = 1  # 实线
            border.Weight = 4  # 粗线
            border.Color = 0x000000  # 黑色

    """
    清除方法对比
    
    方法	说明	适用场景
    UsedRange.Clear()           清除所有已使用单元格的内容和格式     完全清空表格
    UsedRange.ClearContents()	只清除内容，保留格式                保留表格样式
    UsedRange.ClearFormats()	只清除格式，保留内容	            重置格式
    Cells.Clear()               清除整个工作表	                    彻底清空
    Range("A2:Z100").Clear()	清除指定范围	                    部分清除
    Rows(2).Delete()        	删除整行	                        删除数据行
    """
    # 动态更新数据
    print("开始动态更新...")
    while True:

        # 在循环前关闭屏幕更新
        excel.ScreenUpdating = False
        excel.DisplayAlerts = False
        excel.Calculation = -4135  # xlCalculationManual 手动计算

        # 方法1: 遍历区域内所有单元格（推荐）
        range_area = worksheet.Range("A1:Z26")

        for cell in range_area:
            # cell.Value = random.randint(1, 100)
            # cell.Font.Color = 0xFF0000

            # 原始颜色
            original = int(cell.Interior.Color)

            if original == 0xFFFFFF:
                continue

            b = (original >> 16) & 0xFF >> 1
            g = (original >> 8) & 0xFF >> 1
            r = (original >> 0) & 0xFF >> 1

            cell.Interior.Color = (b << 16) | (g << 8) | (r)

            print(f"{original=}")
            print(f"{cell.Interior.Color=}")

        row = random.randint(1, 26)
        column = random.randint(1, 26)
        cell = worksheet.cells(row, column)

        cell.value = f"<{row}, {column}>"

        # 设置背景颜色
        cell.Interior.Color = random.randint(0, 0xFFFFFF)

        # 恢复设置
        excel.ScreenUpdating = True
        excel.DisplayAlerts = True
        excel.Calculation = -4105  # xlCalculationAutomatic

        time.sleep(0.5)  # 每秒更新一次

    # 保存（可选）
    workbook.Save()

    print("更新完成！")

except Exception as e:
    print(f"错误: {e}")


"""
openpyxl
    ws.cell(r, c)
    ws[""]
win32
    ws.cells(r, c)
"""
