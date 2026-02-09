
import sys
from PyQt6 import QtWidgets


class NoWrapDial(QtWidgets.QDial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRange(0, 100)
        self.setWrapping(False)       # 首先确保关闭绕回
        self.setNotchesVisible(True)
        self._last = self.value()
        self.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, v: int):
        """防御性处理：若检测到一次性跨越半个量程，判定为绕回并夹紧到端点。"""
        rng = self.maximum() - self.minimum()
        if rng <= 0:
            self._last = v
            return

        if abs(v - self._last) > rng / 2:
            # 发生了从 0→最大 或 最大→0 的“绕回式跳变”
            self.blockSignals(True)
            if v > self._last:
                # 例如 0 → 100 的跳变，强制留在最小
                self.setValue(self.minimum())
                v = self.minimum()
            else:
                # 例如 100 → 0 的跳变，强制留在最大
                self.setValue(self.maximum())
                v = self.maximum()
            self.blockSignals(False)

        self._last = v

    def wheelEvent(self, e):
        """在 0 时禁止继续向更小滚；在最大时禁止继续向更大滚。"""
        delta = e.angleDelta().y()
        if (self.value() <= self.minimum() and delta < 0) or \
           (self.value() >= self.maximum() and delta > 0):
            e.ignore()
            return
        super().wheelEvent(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)

    label = QtWidgets.QLabel("值：0")
    dial = NoWrapDial()
    dial.setValue(0)
    dial.valueChanged.connect(lambda v: label.setText(f"值：{v}"))

    # 对比：开启绕回的 dial（演示问题）
    dial_wrap = QtWidgets.QDial()
    dial_wrap.setRange(0, 100)
    dial_wrap.setWrapping(True)     # 故意打开绕回
    dial_wrap.setNotchesVisible(True)
    lbl2 = QtWidgets.QLabel("对比（wrapping=True）：0")
    dial_wrap.valueChanged.connect(lambda v: lbl2.setText(f"对比：{v}"))

    lay.addWidget(label)
    lay.addWidget(dial)
    lay.addSpacing(12)
    lay.addWidget(lbl2)
    lay.addWidget(dial_wrap)

    w.setWindowTitle("QDial 无绕回示例")
    w.resize(260, 320)
    w.show()
    sys.exit(app.exec())
