import win32com.client
import pythoncom
import time
import random
import os


class ExcelUpdater:
    """
    方法3: Excel更新器类 - 更灵活的控制
    """

    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
        self.excel = None
        self.workbook = None
        self.worksheet = None

    def connect(self):
        """连接到Excel"""
        try:
            # 初始化COM
            pythoncom.CoInitialize()

            # 获取或创建Excel实例
            try:
                self.excel = win32com.client.GetActiveObject("Excel.Application")
            except:
                self.excel = win32com.client.Dispatch("Excel.Application")

            self.excel.Visible = True

            print(f"{self.excel}")
            # 打开工作簿
            workbook_found = False
            for wb in self.excel.Workbooks:
                print(f"1")
                print(wb.FullName.lower())
                if wb.FullName.lower() == self.file_path.lower():
                    print(f"2")
                    self.workbook = wb
                    print(f"3")
                    workbook_found = True
                    print(f"4")
                    break

            if not workbook_found:
                print(f"5")
                if os.path.exists(self.file_path):
                    print(f"6")
                    self.workbook = self.excel.Workbooks.Open(self.file_path)
                else:
                    print(f"7")
                    self.workbook = self.excel.Workbooks.Add()
                    self.workbook.SaveAs(self.file_path)

            self.worksheet = self.workbook.Worksheets(1)
            print("已连接到Excel")
            return True

        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def update_cell(self, row, col, value):
        """更新单个单元格"""
        try:
            self.worksheet.Cells(row, col).Value = value
            return True
        except Exception as e:
            print(f"更新单元格失败: {e}")
            return False

    def update_range(self, start_row, start_col, data):
        """更新一个范围的数据"""
        try:
            for i, row_data in enumerate(data):
                for j, value in enumerate(row_data):
                    self.worksheet.Cells(start_row + i, start_col + j).Value = value
            return True
        except Exception as e:
            print(f"更新范围失败: {e}")
            return False

    def format_cell(self, row, col, **kwargs):
        """格式化单元格"""
        try:
            cell = self.worksheet.Cells(row, col)

            if "bold" in kwargs:
                cell.Font.Bold = kwargs["bold"]
            if "color" in kwargs:
                cell.Font.Color = kwargs["color"]
            if "bg_color" in kwargs:
                cell.Interior.Color = kwargs["bg_color"]
            if "size" in kwargs:
                cell.Font.Size = kwargs["size"]

            return True
        except Exception as e:
            print(f"格式化失败: {e}")
            return False

    def save(self):
        """保存工作簿"""
        try:
            self.workbook.Save()
            print("已保存")
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False

    def close(self):
        """关闭连接"""
        try:
            pythoncom.CoUninitialize()
            print("已断开连接")
        except:
            pass


# 使用示例
def demo_updater():
    updater = ExcelUpdater("example.xlsx")

    if updater.connect():
        # 设置表头
        headers = ["序号", "时间", "数值", "状态"]
        updater.update_range(1, 1, [headers])

        # 格式化表头
        for col in range(1, 5):
            updater.format_cell(1, col, bold=True, bg_color=0x4472C4, color=0xFFFFFF)

        # 动态更新数据
        for i in range(10):
            row_data = [
                i + 1,
                time.strftime("%H:%M:%S"),
                random.randint(1, 100),
                "运行中",
            ]
            updater.update_range(i + 2, 1, [row_data])
            print(f"更新第 {i + 1} 行")
            time.sleep(1)

        updater.save()
        updater.close()


demo_updater()
