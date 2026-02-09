from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QDoubleSpinBox,
    QDial,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QColorDialog,
)
from PyQt6.QtCore import QTimer

import sys
import time


fns = []

"""
PyQt6 主要组件分类

1. 基础窗口组件
QWidget - 所有UI组件的基类
QMainWindow - 主窗口，支持菜单栏、工具栏、状态栏
QDialog - 对话框窗口
QMessageBox - 消息提示框
QFileDialog - 文件选择对话框
QColorDialog - 颜色选择对话框
QFontDialog - 字体选择对话框



















"""

fns.append(1)
# fns.remove(1)

if 1 in fns:

    app = QApplication(sys.argv)

    dialog = QDialog()

    x = 0
    y = 0
    w = 100
    h = 20

    dialog.setWindowTitle("对话框")
    dialog.setGeometry(100, 100, 400, 300)

    label = QLabel("标签", dialog)
    label.setGeometry(x, y, w, h)

    def move():
        global x
        x += 10
        label.setGeometry(x, y, w, h)

    # 创建定时器
    # timer = QTimer()
    # timer.timeout.connect(move)  # 连接到移动函数
    # timer.start(500)  # 每500毫秒（0.5秒）触发一次

    if False:
        # 添加 QDoubleSpinBox
        spinbox = QDoubleSpinBox(dialog)
        spinbox.setGeometry(50, 50, 150, 30)
        spinbox.setMinimum(0.0)
        spinbox.setMaximum(100.0)
        spinbox.setSingleStep(0.1)
        spinbox.setValue(3.14)
        spinbox.setDecimals(2)  # 设置小数位数

    # 添加 QDial
    dial = QDial(dialog)
    dial.setGeometry(200, 50, 100, 100)
    dial.setMinimum(0)
    dial.setMaximum(100)
    dial.setValue(50)
    dial.setNotchesVisible(True)  # 显示刻度
    # dial.setWrapping(True)

    # 连接旋钮值变化信号到标签更新
    def update_label(value):
        label.setText(f"旋钮值: {value}")

    dial.valueChanged.connect(update_label)
    # 初始化标签显示
    update_label(dial.value())

    # 添加颜色选择按钮
    color_button = QPushButton("选择颜色", dialog)
    color_button.setGeometry(50, 160, 100, 30)

    def open_color_dialog():
        color = QColorDialog.getColor()
        if color.isValid():
            label.setStyleSheet(f"background-color: {color.name()};")

    color_button.clicked.connect(open_color_dialog)

    # 添加消息框按钮
    msg_button = QPushButton("显示消息", dialog)
    msg_button.setGeometry(160, 160, 100, 30)

    def show_message():
        QMessageBox.information(dialog, "提示", "这是一个消息框示例！")

    msg_button.clicked.connect(show_message)

    dialog.show()
    sys.exit(app.exec())


if False:
    app = QApplication(sys.argv)
    a = QDialog()
    # a.show()
    a.resize(400, 300)
    a.move(100, 100)
    a.setWindowTitle("PyQt6 Dialog Example")
    sys.exit(app.exec())

    pass


"""
2. 按钮类组件
QPushButton - 普通按钮
QRadioButton - 单选按钮
QCheckBox - 复选框
QToolButton - 工具按钮
QCommandLinkButton - 命令链接按钮
"""

if 2 in fns:
    pass

"""
3. 输入组件
QLineEdit - 单行文本输入框
QTextEdit - 多行富文本编辑器
QPlainTextEdit - 多行纯文本编辑器
QSpinBox - 整数调节框
QDoubleSpinBox - 浮点数调节框
QComboBox - 下拉选择框
QSlider - 滑动条
QDial - 旋钮
"""

if 3 in fns:
    pass

"""
4. 显示组件
QLabel - 文本或图片标签
QTextBrowser - 文本浏览器
QLCDNumber - LCD数字显示
QProgressBar - 进度条
QCalendarWidget - 日历控件
"""

if 4 in fns:
    pass


"""
5. 容器和布局
QGroupBox - 分组框
QTabWidget - 选项卡容器
QScrollArea - 滚动区域
QSplitter - 分割器
QStackedWidget - 堆叠窗口
QHBoxLayout - 水平布局
QVBoxLayout - 垂直布局
QGridLayout - 网格布局
QFormLayout - 表单布局
"""

if 5 in fns:
    pass


"""
6. 列表和树形组件
QListWidget - 列表控件
QTreeWidget - 树形控件
QTableWidget - 表格控件
QListView - 列表视图（MVC模式）
QTreeView - 树形视图（MVC模式）
QTableView - 表格视图（MVC模式）
"""

if 6 in fns:
    pass


"""
7. 菜单和工具栏
QMenuBar - 菜单栏
QMenu - 菜单
QAction - 动作/操作
QToolBar - 工具栏
QStatusBar - 状态栏
"""
if 4 in fns:
    pass


"""
8. 多媒体组件
QMediaPlayer - 媒体播放器
QVideoWidget - 视频显示控件
QAudioOutput - 音频输出
"""
if 4 in fns:
    pass

"""
9. 图形和绘图
QGraphicsView - 图形视图
QGraphicsScene - 图形场景
QGraphicsItem - 图形项
QPainter - 绘图工具
"""
if 4 in fns:
    pass

"""
10. 其他实用组件
QTimer - 定时器
QThread - 线程
QClipboard - 剪贴板
QDrag - 拖放操作
QSystemTrayIcon - 系统托盘图标
QToolTip - 工具提示
QDockWidget - 可停靠窗口
这些是PyQt6中最常用的组件，实际上还有更多专业和高级的组件可供使用。
"""
if 4 in fns:
    pass

"""
11. Web和网络组件
QWebEngineView - 网页浏览器视图
QWebEngineSettings - 网页引擎设置
QNetworkAccessManager - 网络访问管理器
"""
if 4 in fns:
    pass


print(f"test")
