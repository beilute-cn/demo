from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTabBar,
    QPushButton,
)
from PyQt6.QtCore import Qt, QMimeData, QPoint, pyqtSignal, QRect
from PyQt6.QtGui import QDrag, QPixmap, QMouseEvent, QRegion
import sys
import pickle


class CustomTitleBar(QWidget):
    """自定义标题栏"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(35)
        self.setStyleSheet(
            """
            QWidget {
                background: #f0f0f0;
                border-bottom: 1px solid #c0c0c0;
            }
            QPushButton {
                background: transparent;
                border: none;
                font-size: 16px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background: #e0e0e0;
            }
            QPushButton#closeBtn:hover {
                background: #e81123;
                color: white;
            }
        """
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)

        # 标题
        self.title_label = QLabel("浏览器风格标签页")
        self.title_label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(self.title_label)

        layout.addStretch()

        # 最小化按钮
        min_btn = QPushButton("−")
        min_btn.setFixedSize(45, 35)
        min_btn.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(min_btn)

        # 最大化/还原按钮
        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(45, 35)
        self.max_btn.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.max_btn)

        # 关闭按钮
        close_btn = QPushButton("×")
        close_btn.setObjectName("closeBtn")
        close_btn.setFixedSize(45, 35)
        close_btn.clicked.connect(self.parent_window.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

        # 用于拖动窗口
        self.drag_pos = None

    def toggle_maximize(self):
        """切换最大化状态"""
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.max_btn.setText("□")
        else:
            self.parent_window.showMaximized()
            self.max_btn.setText("❐")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = (
                event.globalPosition().toPoint()
                - self.parent_window.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_pos:
            self.parent_window.move(event.globalPosition().toPoint() - self.drag_pos)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()


class DraggableTabBar(QTabBar):
    """可拖拽的标签栏"""

    tab_detached = pyqtSignal(int, QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setElideMode(Qt.TextElideMode.ElideRight)
        self.setSelectionBehaviorOnRemove(QTabBar.SelectionBehavior.SelectLeftTab)
        self.setMovable(True)
        self.drag_start_pos = None
        self.dragging_out = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.pos()
            self.dragging_out = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if not self.drag_start_pos:
            return

        # 计算拖拽距离
        distance = (event.pos() - self.drag_start_pos).manhattanLength()

        # 检查是否拖出标签栏区域（向上或向下超过30像素）
        if abs(event.pos().y() - self.drag_start_pos.y()) > 30:
            if distance > QApplication.startDragDistance() and not self.dragging_out:
                self.dragging_out = True
                self.start_drag(event)
                return

        # 在标签栏内正常移动
        super().mouseMoveEvent(event)

    def start_drag(self, event):
        """开始拖拽到窗口外"""
        tab_index = self.tabAt(self.drag_start_pos)
        if tab_index == -1:
            return

        # 创建拖拽对象
        drag = QDrag(self)
        mime_data = QMimeData()

        # 保存标签数据
        tab_widget = self.parent()
        window = tab_widget.window()

        tab_data = {
            "index": tab_index,
            "text": tab_widget.tabText(tab_index),
            "window_id": id(window),
        }
        mime_data.setData("application/x-tabdata", pickle.dumps(tab_data))

        # 创建拖拽预览图
        # pixmap = tab_widget.widget(tab_index).grab()
        # drag.setPixmap(pixmap.scaled(200, 150, Qt.AspectRatioMode.KeepAspectRatio))
        # drag.setMimeData(mime_data)

        tab_rect = self.tabRect(tab_index)
        pixmap = QPixmap(tab_rect.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        self.render(pixmap, QPoint(), QRegion(tab_rect))
        drag.setPixmap(pixmap)

        # 执行拖拽
        drop_action = drag.exec(Qt.DropAction.MoveAction)

        # 如果拖拽到窗口外，发出分离信号
        if drop_action == Qt.DropAction.IgnoreAction:
            self.tab_detached.emit(tab_index, event.globalPosition().toPoint())

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-tabdata"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-tabdata"):
            event.acceptProposedAction()


class DraggableTabWidget(QTabWidget):
    """支持拖拽的标签页控件"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 使用自定义标签栏
        self.tab_bar = DraggableTabBar(self)
        self.setTabBar(self.tab_bar)

        self.setMovable(True)
        self.setTabsClosable(True)
        self.setAcceptDrops(True)
        self.setDocumentMode(True)

        # 连接信号
        self.tab_bar.tab_detached.connect(self.detach_tab)

    def detach_tab(self, index, point):
        """分离标签页到新窗口"""
        if self.count() <= 1:
            return

        # 获取标签信息
        name = self.tabText(index)
        icon = self.tabIcon(index)
        widget = self.widget(index)

        # 从当前窗口移除
        self.removeTab(index)

        # 创建新窗口
        new_window = BrowserWindow()
        new_window.move(point)

        # 添加到新窗口
        new_window.tab_widget.clear()
        new_window.tab_widget.addTab(widget, icon, name)
        new_window.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-tabdata"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """拖动过程中更新"""
        if event.mimeData().hasFormat("application/x-tabdata"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-tabdata"):
            # 反序列化标签数据
            tab_data = pickle.loads(event.mimeData().data("application/x-tabdata"))
            source_window_id = tab_data["window_id"]
            source_index = tab_data["index"]

            # 查找源窗口
            source_window = None
            for window in BrowserWindow.windows:
                if id(window) == source_window_id:
                    source_window = window
                    break

            if source_window and source_window != self.window():
                # 跨窗口拖拽
                source_tab_widget = source_window.tab_widget

                # 获取标签信息
                name = source_tab_widget.tabText(source_index)
                icon = source_tab_widget.tabIcon(source_index)
                widget = source_tab_widget.widget(source_index)

                # 从源窗口移除
                source_tab_widget.removeTab(source_index)

                # 计算插入位置 - 根据鼠标在标签栏的位置
                drop_pos = event.position().toPoint()

                # 将坐标转换到标签栏坐标系
                tab_bar_pos = self.tab_bar.mapFrom(self, drop_pos)

                # 查找最接近的标签位置
                target_index = -1
                for i in range(self.count()):
                    tab_rect = self.tab_bar.tabRect(i)
                    if tab_bar_pos.x() < tab_rect.center().x():
                        target_index = i
                        break

                # 如果没有找到合适位置，插入到末尾
                if target_index == -1:
                    target_index = self.count()

                # 插入标签页
                self.insertTab(target_index, widget, icon, name)
                self.setCurrentIndex(target_index)

                # 如果源窗口没有标签了，关闭它
                if source_tab_widget.count() == 0:
                    source_window.close()

            event.acceptProposedAction()


class BrowserWindow(QMainWindow):
    """浏览器风格的主窗口"""

    windows = []

    def __init__(self):
        super().__init__()

        # 无边框窗口
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(100, 100, 600, 400)

        # 主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 添加自定义标题栏
        # self.title_bar = CustomTitleBar(self)
        # main_layout.addWidget(self.title_bar)

        # 创建标签页控件
        self.tab_widget = DraggableTabWidget(self)
        main_layout.addWidget(self.tab_widget)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 设置样式表
        self.setStyleSheet(
            """
            QMainWindow {
                background: white;
                border: 1px solid #c0c0c0;
            }
            QTabWidget::pane {
                border: 0px;
                background: white;
            }
            QTabBar::tab {
                background: #e8e8e8;
                border: 1px solid #c0c0c0;
                border-bottom: 0px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 8px 16px;
                margin-right: 2px;
                min-width: 120px;
                max-width: 200px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid white;
            }
            QTabBar::tab:hover {
                background: #f0f0f0;
            }
        """
        )

        # 添加示例标签页
        for i in range(1, 4):
            self.add_tab(f"标签页 {i}")

        # 标签页关闭事件
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        BrowserWindow.windows.append(self)

    def add_tab(self, title):
        """添加新标签页"""
        widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel(
            f"<h2>{title}</h2>"
            "<p><b>操作说明：</b></p>"
            "<p>• 在标签栏内左右拖动改变顺序</p>"
            "<p>• 向上或向下拖出30像素创建新窗口</p>"
            "<p>• 拖到其他窗口标签栏的指定位置插入</p>"
            "<p>• 双击标题栏最大化/还原窗口</p>"
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # 添加新建标签按钮
        btn = QPushButton("+ 新建标签页")
        btn.setStyleSheet(
            """
            QPushButton {
                background: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #106ebe;
            }
        """
        )
        btn.clicked.connect(
            lambda: self.add_tab(f"新标签 {self.tab_widget.count() + 1}")
        )
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        widget.setLayout(layout)

        self.tab_widget.addTab(widget, title)

    def close_tab(self, index):
        """关闭标签页"""
        self.tab_widget.removeTab(index)

        # 如果没有标签页了，关闭窗口
        if self.tab_widget.count() == 0:
            self.close()

    def closeEvent(self, event):
        """窗口关闭事件"""
        if self in BrowserWindow.windows:
            BrowserWindow.windows.remove(self)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建第一个窗口
    window1 = BrowserWindow()
    window1.show()

    sys.exit(app.exec())
