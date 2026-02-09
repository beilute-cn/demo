"""
Excel Range 对象参考
文档: https://docs.microsoft.com/en-us/office/vba/api/excel.range(object)
"""

RANGE_REFERENCE = {
    "属性": {
        # 值和内容
        "Value": "Variant - 单元格值",
        "Value2": "Variant - 单元格值（不含格式）",
        "Text": "String - 显示的文本",
        "Formula": "String - 公式（A1样式）",
        "FormulaR1C1": "String - 公式（R1C1样式）",
        
        # 位置信息
        "Address": "String - 单元格地址",
        "Row": "Long - 行号",
        "Column": "Long - 列号",
        "Rows": "Range - 行集合",
        "Columns": "Range - 列集合",
        "Count": "Long - 单元格数量",
        
        # 格式对象
        "Font": "Font - 字体对象",
        "Interior": "Interior - 内部对象（背景）",
        "Borders": "Borders - 边框对象",
        "NumberFormat": "String - 数字格式",
        
        # 对齐
        "HorizontalAlignment": "XlHAlign - 水平对齐",
        "VerticalAlignment": "XlVAlign - 垂直对齐",
        "WrapText": "Boolean - 自动换行",
        "Orientation": "Variant - 文本方向",
        
        # 其他
        "Comment": "Comment - 批注对象",
        "Hyperlinks": "Hyperlinks - 超链接集合",
        "Validation": "Validation - 数据验证",
        "MergeCells": "Boolean - 是否为合并单元格",
    },
    
    "方法": {
        # 清除
        "Clear()": "清除内容和格式",
        "ClearContents()": "清除内容",
        "ClearFormats()": "清除格式",
        "ClearComments()": "清除批注",
        
        # 复制粘贴
        "Copy(Destination)": "复制",
        "Cut(Destination)": "剪切",
        "Paste()": "粘贴",
        "PasteSpecial()": "选择性粘贴",
        
        # 选择和激活
        "Select()": "选择范围",
        "Activate()": "激活单元格",
        
        # 查找和替换
        "Find(What)": "查找",
        "FindNext(After)": "查找下一个",
        "Replace(What, Replacement)": "替换",
        
        # 合并
        "Merge()": "合并单元格",
        "UnMerge()": "取消合并",
        
        # 插入删除
        "Insert(Shift)": "插入单元格",
        "Delete(Shift)": "删除单元格",
        
        # 排序筛选
        "Sort()": "排序",
        "AutoFilter()": "自动筛选",
        
        # 其他
        "AutoFit()": "自动调整大小",
        "AddComment(Text)": "添加批注",
    }
}

# 示例代码
def demo_range():
    import win32com.client
    
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    
    workbook = excel.Workbooks.Add()
    worksheet = workbook.Worksheets(1)
    
    # 设置值
    worksheet.Range("A1").Value = "标题"
    worksheet.Cells(2, 1).Value = "数据1"
    
    # 设置公式
    worksheet.Range("B1").Formula = "=SUM(A1:A10)"
    
    # 格式化
    cell = worksheet.Range("A1")
    cell.Font.Bold = True
    cell.Font.Size = 14
    cell.Font.Color = 0xFF0000
    cell.Interior.Color = 0xFFFF00
    cell.HorizontalAlignment = -4108  # xlCenter
    
    # 合并单元格
    worksheet.Range("A3:C3").Merge()
    worksheet.Range("A3").Value = "合并单元格"
    
    # 添加边框
    range_obj = worksheet.Range("A1:C5")
    range_obj.Borders.LineStyle = 1
    
    # 获取信息
    print(f"地址: {cell.Address}")
    print(f"行号: {cell.Row}")
    print(f"列号: {cell.Column}")
    print(f"值: {cell.Value}")
    
    # 清理
    workbook.Close(SaveChanges=False)
    excel.Quit()

# 打印参考
def print_reference():
    print("=" * 80)
    print("Excel Range 对象参考")
    print("文档: https://docs.microsoft.com/en-us/office/vba/api/excel.range")
    print("=" * 80)
    
    for category, items in RANGE_REFERENCE.items():
        print(f"\n{category}:")
        print("-" * 80)
        for name, description in items.items():
            print(f"  {name:40} {description}")

if __name__ == "__main__":
    print_reference()
