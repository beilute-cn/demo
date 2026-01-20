def dec_private_modes():
    """DEC 私有模式列表"""

    print("=" * 80)
    print("DEC 私有模式 (最常用)")
    print("=" * 80)

    modes = [
        {
            "编号": 1,
            "名称": "DECCKM",
            "全称": "Cursor Keys Mode",
            "启用": "\\033[?1h",
            "禁用": "\\033[?1l",
            "功能": "应用光标键模式",
            "说明": "光标键发送应用序列而非 ANSI 序列",
            "支持": "⭐⭐⭐⭐⭐",
        },
        {
            "编号": 3,
            "名称": "DECCOLM",
            "全称": "Column Mode",
            "启用": "\\033[?3h",
            "禁用": "\\033[?3l",
            "功能": "132 列模式",
            "说明": "切换 80/132 列显示",
            "支持": "⭐⭐⭐",
        },
        {
            "编号": 4,
            "名称": "DECSCLM",
            "全称": "Scrolling Mode",
            "启用": "\\033[?4h",
            "禁用": "\\033[?4l",
            "功能": "平滑滚动",
            "说明": "启用平滑滚动而非跳跃滚动",
            "支持": "⭐⭐",
        },
        {
            "编号": 5,
            "名称": "DECSCNM",
            "全称": "Screen Mode",
            "启用": "\\033[?5h",
            "禁用": "\\033[?5l",
            "功能": "反显模式",
            "说明": "反转屏幕颜色（黑底白字 ↔ 白底黑字）",
            "支持": "⭐⭐⭐⭐",
        },
        {
            "编号": 6,
            "名称": "DECOM",
            "全称": "Origin Mode",
            "启用": "\\033[?6h",
            "禁用": "\\033[?6l",
            "功能": "原点模式",
            "说明": "光标定位相对于滚动区域",
            "支持": "⭐⭐⭐",
        },
        {
            "编号": 7,
            "名称": "DECAWM",
            "全称": "Auto Wrap Mode",
            "启用": "\\033[?7h",
            "禁用": "\\033[?7l",
            "功能": "自动换行",
            "说明": "到达行尾时自动换行",
            "支持": "⭐⭐⭐⭐⭐",
        },
        {
            "编号": 12,
            "名称": "ATT610",
            "全称": "Start Blinking Cursor",
            "启用": "\\033[?12h",
            "禁用": "\\033[?12l",
            "功能": "光标闪烁",
            "说明": "启用/禁用光标闪烁",
            "支持": "⭐⭐⭐⭐",
        },
        {
            "编号": 25,
            "名称": "DECTCEM",
            "全称": "Text Cursor Enable Mode",
            "启用": "\\033[?25h",
            "禁用": "\\033[?25l",
            "功能": "显示/隐藏光标",
            "说明": "最常用的私有模式之一",
            "支持": "⭐⭐⭐⭐⭐",
        },
        {
            "编号": 47,
            "名称": "XTERM_SAVE",
            "全称": "Alternate Screen Buffer",
            "启用": "\\033[?47h",
            "禁用": "\\033[?47l",
            "功能": "备用屏幕缓冲",
            "说明": "切换到备用屏幕（旧版）",
            "支持": "⭐⭐⭐⭐",
        },
        {
            "编号": 1000,
            "名称": "MOUSE_X10",
            "全称": "X10 Mouse Reporting",
            "启用": "\\033[?1000h",
            "禁用": "\\033[?1000l",
            "功能": "鼠标报告",
            "说明": "启用基本鼠标事件报告",
            "支持": "⭐⭐⭐⭐⭐",
        },
        {
            "编号": 1002,
            "名称": "MOUSE_BTN",
            "全称": "Button Event Mouse Tracking",
            "启用": "\\033[?1002h",
            "禁用": "\\033[?1002l",
            "功能": "按钮事件跟踪",
            "说明": "报告鼠标按钮按下和释放",
            "支持": "⭐⭐⭐⭐",
        },
        {
            "编号": 1003,
            "名称": "MOUSE_ANY",
            "全称": "Any Event Mouse Tracking",
            "启用": "\\033[?1003h",
            "禁用": "\\033[?1003l",
            "功能": "任意事件跟踪",
            "说明": "报告所有鼠标移动",
            "支持": "⭐⭐⭐⭐",
        },
        {
            "编号": 1004,
            "名称": "FOCUS",
            "全称": "Focus In/Out Events",
            "启用": "\\033[?1004h",
            "禁用": "\\033[?1004l",
            "功能": "焦点事件",
            "说明": "报告终端获得/失去焦点",
            "支持": "⭐⭐⭐⭐",
        },
        {
            "编号": 1005,
            "名称": "MOUSE_UTF8",
            "全称": "UTF-8 Mouse Mode",
            "启用": "\\033[?1005h",
            "禁用": "\\033[?1005l",
            "功能": "UTF-8 鼠标模式",
            "说明": "使用 UTF-8 编码鼠标坐标",
            "支持": "⭐⭐⭐",
        },
        {
            "编号": 1006,
            "名称": "MOUSE_SGR",
            "全称": "SGR Mouse Mode",
            "启用": "\\033[?1006h",
            "禁用": "\\033[?1006l",
            "功能": "SGR 鼠标模式",
            "说明": "使用 SGR 格式报告鼠标（推荐）",
            "支持": "⭐⭐⭐⭐⭐",
        },
        {
            "编号": 1047,
            "名称": "XTERM_SAVE_ALT",
            "全称": "Alternate Screen Buffer",
            "启用": "\\033[?1047h",
            "禁用": "\\033[?1047l",
            "功能": "备用屏幕缓冲",
            "说明": "切换到备用屏幕（改进版）",
            "支持": "⭐⭐⭐⭐⭐",
        },
        {
            "编号": 1048,
            "名称": "XTERM_SAVE_CURSOR",
            "全称": "Save Cursor",
            "启用": "\\033[?1048h",
            "禁用": "\\033[?1048l",
            "功能": "保存光标",
            "说明": "保存/恢复光标位置",
            "支持": "⭐⭐⭐⭐",
        },
        {
            "编号": 1049,
            "名称": "XTERM_SAVE_FULL",
            "全称": "Save Cursor and Alternate Screen",
            "启用": "\\033[?1049h",
            "禁用": "\\033[?1049l",
            "功能": "完整备用屏幕",
            "说明": "1047 + 1048 组合（最常用）",
            "支持": "⭐⭐⭐⭐⭐",
        },
        {
            "编号": 2004,
            "名称": "BRACKETED_PASTE",
            "全称": "Bracketed Paste Mode",
            "启用": "\\033[?2004h",
            "禁用": "\\033[?2004l",
            "功能": "括号粘贴模式",
            "说明": "粘贴文本时添加特殊标记",
            "支持": "⭐⭐⭐⭐⭐",
        },
    ]

    print(f"\n{'编号':<6} {'名称':<20} {'功能':<25} {'支持度'}")
    print("-" * 80)
    for mode in modes:
        print(f"{mode['编号']:<6} {mode['名称']:<20} {mode['功能']:<25} {mode['支持']}")

    print("\n" + "=" * 80)

    return modes


modes = dec_private_modes()


exit(0)


# 下载地址：
def ecma48_info():
    """ECMA-48 标准信息"""

    print("=" * 70)
    print("ECMA-48: Control Functions for Coded Character Sets")
    print("=" * 70)

    print("\n【官方信息】")
    print("标准名称: ECMA-48")
    print("ISO 等价: ISO/IEC 6429:1992")
    print("版本: 第 5 版 (1991 年 6 月)")
    print("状态: 免费公开")

    print("\n【下载地址】")
    print("PDF 下载:")
    print(
        "https://www.ecma-international.org/wp-content/uploads/ECMA-48_5th_edition_june_1991.pdf"
    )

    print("\n【内容概要】")
    print("- 控制字符定义 (C0, C1)")
    print("- CSI 序列 (Control Sequence Introducer)")
    print("- SGR 参数 (Select Graphic Rendition) - 颜色和样式")
    print("- 光标控制")
    print("- 屏幕操作")
    print("- 模式设置")

    print("\n【重要章节】")
    chapters = [
        ("5.4", "C1 控制字符", "包括 ESC"),
        ("8.3", "控制序列", "CSI 序列格式"),
        ("8.3.117", "SGR", "颜色和文本样式"),
        ("8.3.6", "CUP", "光标定位"),
        ("8.3.39", "ED", "擦除显示"),
        ("8.3.103", "RM/SM", "模式设置"),
    ]

    print(f"\n{'章节':<10} {'名称':<20} {'内容'}")
    print("-" * 70)
    for section, name, content in chapters:
        print(f"{section:<10} {name:<20} {content}")

    print("=" * 70)


ecma48_info()


# 2. ANSI X3.64 (美国标准)
def ansi_x364_info():
    """ANSI X3.64 标准信息"""

    print("=" * 70)
    print("ANSI X3.64 标准")
    print("=" * 70)

    print("\n【基本信息】")
    print("标准名称: ANSI X3.64-1979")
    print("全称: Additional Controls for Use with")
    print("      American National Standard Code for")
    print("      Information Interchange")
    print("状态: 已被 ISO/IEC 6429 取代")

    print("\n【注意】")
    print("ANSI X3.64 是早期标准，现在应该参考:")
    print("- ECMA-48 (免费)")
    print("- ISO/IEC 6429 (等价于 ECMA-48)")

    print("\n【历史】")
    print("1979: ANSI X3.64 发布")
    print("1986: 被 ISO 6429 取代")
    print("1991: ISO 6429 更新为 ISO/IEC 6429")
    print("1991: ECMA-48 第 5 版发布")

    print("=" * 70)


ansi_x364_info()


# 在线资源
# 1. 维基百科和参考文档
def online_resources():
    """在线资源列表"""

    print("=" * 70)
    print("ANSI 转义序列在线资源")
    print("=" * 70)

    resources = [
        {
            "名称": "Wikipedia - ANSI escape code",
            "URL": "https://en.wikipedia.org/wiki/ANSI_escape_code",
            "语言": "英文",
            "质量": "⭐⭐⭐⭐⭐",
            "特点": "最全面的参考，包含所有序列",
        },
        {
            "名称": "Wikipedia - ANSI 转义序列",
            "URL": "https://zh.wikipedia.org/wiki/ANSI转义序列",
            "语言": "中文",
            "质量": "⭐⭐⭐⭐",
            "特点": "中文版本，内容较少",
        },
        {
            "名称": "XTerm Control Sequences",
            "URL": "https://invisible-island.net/xterm/ctlseqs/ctlseqs.html",
            "语言": "英文",
            "质量": "⭐⭐⭐⭐⭐",
            "特点": "XTerm 实现，非常详细",
        },
        {
            "名称": "Console Virtual Terminal Sequences",
            "URL": "https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences",
            "语言": "英文",
            "质量": "⭐⭐⭐⭐",
            "特点": "Windows 终端官方文档",
        },
        {
            "名称": "ANSI Escape Sequences Gist",
            "URL": "https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797",
            "语言": "英文",
            "质量": "⭐⭐⭐⭐⭐",
            "特点": "快速参考，格式清晰",
        },
        {
            "名称": "Build your own Command Line",
            "URL": "https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html",
            "语言": "英文",
            "质量": "⭐⭐⭐⭐",
            "特点": "实用教程，有示例",
        },
    ]

    for i, res in enumerate(resources, 1):
        print(f"\n【{i}. {res['名称']}】")
        print(f"URL: {res['URL']}")
        print(f"语言: {res['语言']}")
        print(f"质量: {res['质量']}")
        print(f"特点: {res['特点']}")

    print("\n" + "=" * 70)


online_resources()


# 　2. 交互式工具


def interactive_tools():
    """交互式工具和测试网站"""

    print("=" * 70)
    print("ANSI 转义序列交互式工具")
    print("=" * 70)

    tools = [
        {
            "名称": "ANSI Escape Tester",
            "URL": "https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#demo",
            "功能": "在线测试 ANSI 序列",
        },
        {
            "名称": "Terminal.sexy",
            "URL": "https://terminal.sexy/",
            "功能": "终端配色方案设计",
        },
        {
            "名称": "Colorize",
            "URL": "https://github.com/crazy-max/ghaction-import-gpg",
            "功能": "颜色代码生成器",
        },
        {
            "名称": "ANSI Color Code",
            "URL": "https://talyian.github.io/ansicolors/",
            "功能": "256 色和 RGB 色预览",
        },
    ]

    for tool in tools:
        print(f"\n{tool['名称']}")
        print(f"  URL: {tool['URL']}")
        print(f"  功能: {tool['功能']}")

    print("\n" + "=" * 70)


interactive_tools()


# 快速参考文档
# 1. 常用序列速查表
def quick_reference():
    """快速参考表"""

    print("=" * 70)
    print("ANSI 转义序列快速参考")
    print("=" * 70)

    print("\n【基本格式】")
    print("ESC [ <参数> <命令>")
    print("其中 ESC = \\033 或 \\x1b 或 \\e")

    print("\n【光标控制】")
    cursor_commands = [
        ("\\033[{n}A", "光标上移 n 行", "CUU"),
        ("\\033[{n}B", "光标下移 n 行", "CUD"),
        ("\\033[{n}C", "光标右移 n 列", "CUF"),
        ("\\033[{n}D", "光标左移 n 列", "CUB"),
        ("\\033[{row};{col}H", "光标移动到指定位置", "CUP"),
        ("\\033[s", "保存光标位置", "SCP"),
        ("\\033[u", "恢复光标位置", "RCP"),
    ]

    print(f"{'序列':<25} {'功能':<25} {'名称'}")
    print("-" * 70)
    for seq, func, name in cursor_commands:
        print(f"{seq:<25} {func:<25} {name}")

    print("\n【屏幕操作】")
    screen_commands = [
        ("\\033[2J", "清除整个屏幕", "ED"),
        ("\\033[0J", "清除从光标到屏幕末尾", "ED"),
        ("\\033[1J", "清除从屏幕开始到光标", "ED"),
        ("\\033[2K", "清除整行", "EL"),
        ("\\033[0K", "清除从光标到行尾", "EL"),
        ("\\033[1K", "清除从行首到光标", "EL"),
    ]

    print(f"{'序列':<25} {'功能':<25} {'名称'}")
    print("-" * 70)
    for seq, func, name in screen_commands:
        print(f"{seq:<25} {func:<25} {name}")

    print("\n【颜色和样式 (SGR)】")
    sgr_commands = [
        ("\\033[0m", "重置所有属性", "Reset"),
        ("\\033[1m", "粗体", "Bold"),
        ("\\033[2m", "暗淡", "Dim"),
        ("\\033[3m", "斜体", "Italic"),
        ("\\033[4m", "下划线", "Underline"),
        ("\\033[7m", "反显", "Reverse"),
        ("\\033[30-37m", "前景色 (8 色)", "Foreground"),
        ("\\033[40-47m", "背景色 (8 色)", "Background"),
        ("\\033[90-97m", "亮前景色", "Bright FG"),
        ("\\033[100-107m", "亮背景色", "Bright BG"),
        ("\\033[38;5;{n}m", "256 色前景", "256 FG"),
        ("\\033[48;5;{n}m", "256 色背景", "256 BG"),
        ("\\033[38;2;{r};{g};{b}m", "RGB 前景", "RGB FG"),
        ("\\033[48;2;{r};{g};{b}m", "RGB 背景", "RGB BG"),
    ]

    print(f"{'序列':<30} {'功能':<25} {'名称'}")
    print("-" * 70)
    for seq, func, name in sgr_commands:
        print(f"{seq:<30} {func:<25} {name}")

    print("\n【模式设置】")
    mode_commands = [
        ("\\033[={n}h", "设置屏幕模式", "DOS 模式"),
        ("\\033[?25h", "显示光标", "DECTCEM"),
        ("\\033[?25l", "隐藏光标", "DECTCEM"),
        ("\\033[?1049h", "启用备用屏幕缓冲", "Alt Screen"),
        ("\\033[?1049l", "禁用备用屏幕缓冲", "Alt Screen"),
    ]

    print(f"{'序列':<25} {'功能':<25} {'名称'}")
    print("-" * 70)
    for seq, func, name in mode_commands:
        print(f"{seq:<25} {func:<25} {name}")

    print("\n" + "=" * 70)


quick_reference()


# 2. 创建本地参考文档
"""
ANSI 转义序列本地参考文档生成器
"""


def generate_html_reference():
    """生成 HTML 格式的参考文档"""

    html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ANSI 转义序列参考</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 30px;
            border-left: 4px solid #4CAF50;
            padding-left: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        th {
            background: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background: #f5f5f5;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        .demo {
            background: #000;
            color: #fff;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            margin: 10px 0;
        }
        .color-demo {
            display: inline-block;
            width: 30px;
            height: 30px;
            margin: 2px;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <h1>ANSI 转义序列完整参考</h1>
    
    <h2>1. 基本格式</h2>
    <p>ANSI 转义序列的基本格式：<code>ESC [ 参数 命令</code></p>
    <p>其中 ESC 可以表示为：</p>
    <ul>
        <li><code>\\033</code> (八进制)</li>
        <li><code>\\x1b</code> (十六进制)</li>
        <li><code>\\e</code> (某些语言)</li>
    </ul>
    
    <h2>2. 光标控制</h2>
    <table>
        <tr>
            <th>序列</th>
            <th>功能</th>
            <th>示例</th>
        </tr>
        <tr>
            <td><code>\\033[{n}A</code></td>
            <td>光标上移 n 行</td>
            <td><code>\\033[5A</code> 上移 5 行</td>
        </tr>
        <tr>
            <td><code>\\033[{n}B</code></td>
            <td>光标下移 n 行</td>
            <td><code>\\033[3B</code> 下移 3 行</td>
        </tr>
        <tr>
            <td><code>\\033[{n}C</code></td>
            <td>光标右移 n 列</td>
            <td><code>\\033[10C</code> 右移 10 列</td>
        </tr>
        <tr>
            <td><code>\\033[{n}D</code></td>
            <td>光标左移 n 列</td>
            <td><code>\\033[2D</code> 左移 2 列</td>
        </tr>
        <tr>
            <td><code>\\033[{row};{col}H</code></td>
            <td>光标移动到指定位置</td>
            <td><code>\\033[10;20H</code> 移到第 10 行第 20 列</td>
        </tr>
        <tr>
            <td><code>\\033[s</code></td>
            <td>保存光标位置</td>
            <td><code>\\033[s</code></td>
        </tr>
        <tr>
            <td><code>\\033[u</code></td>
            <td>恢复光标位置</td>
            <td><code>\\033[u</code></td>
        </tr>
    </table>
    
    <h2>3. 屏幕操作</h2>
    <table>
        <tr>
            <th>序列</th>
            <th>功能</th>
            <th>说明</th>
        </tr>
        <tr>
            <td><code>\\033[2J</code></td>
            <td>清除整个屏幕</td>
            <td>最常用的清屏命令</td>
        </tr>
        <tr>
            <td><code>\\033[0J</code></td>
            <td>清除从光标到屏幕末尾</td>
            <td>保留光标之前的内容</td>
        </tr>
        <tr>
            <td><code>\\033[1J</code></td>
            <td>清除从屏幕开始到光标</td>
            <td>保留光标之后的内容</td>
        </tr>
        <tr>
            <td><code>\\033[2K</code></td>
            <td>清除整行</td>
            <td>光标位置不变</td>
        </tr>
        <tr>
            <td><code>\\033[0K</code></td>
            <td>清除从光标到行尾</td>
            <td>保留行首内容</td>
        </tr>
        <tr>
            <td><code>\\033[1K</code></td>
            <td>清除从行首到光标</td>
            <td>保留行尾内容</td>
        </tr>
    </table>
    
    <h2>4. 颜色和样式 (SGR)</h2>
    
    <h3>4.1 文本样式</h3>
    <table>
        <tr>
            <th>序列</th>
            <th>功能</th>
            <th>示例</th>
        </tr>
        <tr>
            <td><code>\\033[0m</code></td>
            <td>重置所有属性</td>
            <td>恢复默认样式</td>
        </tr>
        <tr>
            <td><code>\\033[1m</code></td>
            <td>粗体</td>
            <td><strong>粗体文本</strong></td>
        </tr>
        <tr>
            <td><code>\\033[2m</code></td>
            <td>暗淡</td>
            <td>暗淡文本</td>
        </tr>
        <tr>
            <td><code>\\033[3m</code></td>
            <td>斜体</td>
            <td><em>斜体文本</em></td>
        </tr>
        <tr>
            <td><code>\\033[4m</code></td>
            <td>下划线</td>
            <td><u>下划线文本</u></td>
        </tr>
        <tr>
            <td><code>\\033[7m</code></td>
            <td>反显</td>
            <td>反显文本</td>
        </tr>
        <tr>
            <td><code>\\033[9m</code></td>
            <td>删除线</td>
            <td><s>删除线文本</s></td>
        </tr>
    </table>
    
    <h3>4.2 基本 16 色</h3>
    <table>
        <tr>
            <th>颜色</th>
            <th>前景色</th>
            <th>背景色</th>
            <th>亮前景色</th>
            <th>亮背景色</th>
        </tr>
        <tr>
            <td>黑色</td>
            <td><code>\\033[30m</code></td>
            <td><code>\\033[40m</code></td>
            <td><code>\\033[90m</code></td>
            <td><code>\\033[100m</code></td>
        </tr>
        <tr>
            <td>红色</td>
            <td><code>\\033[31m</code></td>
            <td><code>\\033[41m</code></td>
            <td><code>\\033[91m</code></td>
            <td><code>\\033[101m</code></td>
        </tr>
        <tr>
            <td>绿色</td>
            <td><code>\\033[32m</code></td>
            <td><code>\\033[42m</code></td>
            <td><code>\\033[92m</code></td>
            <td><code>\\033[102m</code></td>
        </tr>
        <tr>
            <td>黄色</td>
            <td><code>\\033[33m</code></td>
            <td><code>\\033[43m</code></td>
            <td><code>\\033[93m</code></td>
            <td><code>\\033[103m</code></td>
        </tr>
        <tr>
            <td>蓝色</td>
            <td><code>\\033[34m</code></td>
            <td><code>\\033[44m</code></td>
            <td><code>\\033[94m</code></td>
            <td><code>\\033[104m</code></td>
        </tr>
        <tr>
            <td>品红</td>
            <td><code>\\033[35m</code></td>
            <td><code>\\033[45m</code></td>
            <td><code>\\033[95m</code></td>
            <td><code>\\033[105m</code></td>
        </tr>
        <tr>
            <td>青色</td>
            <td><code>\\033[36m</code></td>
            <td><code>\\033[46m</code></td>
            <td><code>\\033[96m</code></td>
            <td><code>\\033[106m</code></td>
        </tr>
        <tr>
            <td>白色</td>
            <td><code>\\033[37m</code></td>
            <td><code>\\033[47m</code></td>
            <td><code>\\033[97m</code></td>
            <td><code>\\033[107m</code></td>
        </tr>
    </table>
    
    <h3>4.3 256 色</h3>
    <p>前景色：<code>\\033[38;5;{n}m</code> (n = 0-255)</p>
    <p>背景色：<code>\\033[48;5;{n}m</code> (n = 0-255)</p>
    
    <h3>4.4 RGB 真彩色</h3>
    <p>前景色：<code>\\033[38;2;{r};{g};{b}m</code></p>
    <p>背景色：<code>\\033[48;2;{r};{g};{b}m</code></p>
    <p>示例：<code>\\033[38;2;255;100;50m</code> 橙色文本</p>
    
    <h2>5. 模式设置</h2>
    <table>
        <tr>
            <th>序列</th>
            <th>功能</th>
            <th>说明</th>
        </tr>
        <tr>
            <td><code>\\033[?25h</code></td>
            <td>显示光标</td>
            <td>DECTCEM</td>
        </tr>
        <tr>
            <td><code>\\033[?25l</code></td>
            <td>隐藏光标</td>
            <td>DECTCEM</td>
        </tr>
        <tr>
            <td><code>\\033[?1049h</code></td>
            <td>启用备用屏幕缓冲</td>
            <td>用于全屏应用</td>
        </tr>
        <tr>
            <td><code>\\033[?1049l</code></td>
            <td>禁用备用屏幕缓冲</td>
            <td>恢复正常屏幕</td>
        </tr>
    </table>
    
    <h2>6. 参考资源</h2>
    <ul>
        <li><a href="https://www.ecma-international.org/publications-and-standards/standards/ecma-48/">ECMA-48 官方标准</a></li>
        <li><a href="https://en.wikipedia.org/wiki/ANSI_escape_code">Wikipedia - ANSI escape code</a></li>
        <li><a href="https://invisible-island.net/xterm/ctlseqs/ctlseqs.html">XTerm Control Sequences</a></li>
        <li><a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">ANSI Escape Sequences Gist</a></li>
    </ul>
    
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
        <p>生成时间: 2024</p>
        <p>基于 ECMA-48 标准</p>
    </footer>
</body>
</html>
"""

    # 保存到文件
    with open("ansi_reference.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("HTML 参考文档已生成: ansi_reference.html")
    print("在浏览器中打开即可查看")


# 生成文档
generate_html_reference()
