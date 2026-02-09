"""
Excel Worksheet 对象参考
文档: https://docs.microsoft.com/en-us/office/vba/api/excel.worksheet
"""

WORKSHEET_REFERENCE = {
    "属性": {
        # 基本信息
        "Name": "String - 工作表名称",
        "Index": "Long - 工作表索引位置",
        "Visible": "XlSheetVisibility - 可见性 (-1可见, 0隐藏, 2很隐藏)",
        
        # 范围和单元格
        "Cells": "Range - 所有单元格",
        "Range(Cell1, Cell2)": "Range - 指定范围",
        "UsedRange": "Range - 已使用的范围",
        "Rows": "Range - 所有行",
        "Columns": "Range - 所有列",
        
        # 集合
        "Shapes": "Shapes - 形状集合",
        "Comments": "Comments - 批注集合",
        "Hyperlinks": "Hyperlinks - 超链接集合",
        "PivotTables": "PivotTables - 数据透视表集合",
        
        # 其他
        "StandardWidth": "Double - 标准列宽",
        "StandardHeight": "Double - 标准行高",
        "Tab": "Tab - 工作表标签",
    },
    
    "方法": {
        # 基本操作
        "Activate()": "激活工作表",
        "Select()": "选择工作表",
        "Delete()": "删除工作表",
        "Copy(Before, After)": "复制工作表",
        "Move(Before, After)": "移动工作表",
        
        # 保护
        "Protect(Password)": "保护工作表",
        "Unprotect(Password)": "取消保护",
        
        # 数据操作
        "Calculate()": "计算工作表",
        "Paste()": "粘贴",
        "PasteSpecial()": "选择性粘贴",
        
        # 其他
        "PrintOut()": "打印",
        "PrintPreview()": "打印预览",
        "ChartObjects()": "返回图表对象集合",
    }
}

# 示例代码
def demo_worksheet():
    import win32com.client
    
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    
    workbook = excel.Workbooks.Add()
    worksheet = workbook.Worksheets(1)
    
    # 设置名称
    worksheet.Name = "数据表"
    
    # 添加数据
    worksheet.Cells(1, 1).Value = "姓名"
    worksheet.Cells(1, 2).Value = "年龄"
    worksheet.Cells(2, 1).Value = "张三"
    worksheet.Cells(2, 2).Value = 25
    
    # 获取已使用范围
    used_range = worksheet.UsedRange
    print(f"已使用范围: {used_range.Address}")
    print(f"行数: {used_range.Rows.Count}")
    print(f"列数: {used_range.Columns.Count}")
    
    # 复制工作表
    worksheet.Copy(After=worksheet)
    new_sheet = workbook.Worksheets(2)
    new_sheet.Name = "副本"
    
    # 清理
    workbook.Close(SaveChanges=False)
    excel.Quit()

# 打印参考
def print_reference():
    print("=" * 80)
    print("Excel Worksheet 对象参考")
    print("文档: https://docs.microsoft.com/en-us/office/vba/api/excel.worksheet")
    print("=" * 80)
    
    for category, items in WORKSHEET_REFERENCE.items():
        print(f"\n{category}:")
        print("-" * 80)
        for name, description in items.items():
            print(f"  {name:40} {description}")

if __name__ == "__main__":
    print_reference()
