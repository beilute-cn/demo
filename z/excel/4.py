import win32com.client
import time
import os

def update_open_excel_com(file_path):
    """
    方法1: 使用win32com动态更新已打开的Excel
    需要安装: pip install pywin32
    """
    abs_path = os.path.abspath(file_path)
    
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
        
        # 动态更新数据
        print("开始动态更新...")
        for i in range(10):
            # 更新单元格
            worksheet.Cells(i + 2, 1).Value = f"数据 {i + 1}"
            worksheet.Cells(i + 2, 2).Value = time.strftime("%H:%M:%S")
            worksheet.Cells(i + 2, 3).Value = i * 10
            
            print(f"更新第 {i + 1} 行")
            time.sleep(1)  # 每秒更新一次
        
        # 保存（可选）
        # workbook.Save()
        
        print("更新完成！")
        
    except Exception as e:
        print(f"错误: {e}")

# 使用示例
update_open_excel_com("example.xlsx")
