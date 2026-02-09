from enum import IntFlag


from all import all


class control(all):

    none = 0
    alt_right = 0x0001
    alt_left = 0x0002
    ctrl_right = 0x0004
    ctrl_left = 0x0008
    shift = 0x0010
    num_lock = 0x0020
    scroll_lock = 0x0040
    caps_lock = 0x0080
    enhanced = 0x0100


control.name = {
    control.alt_right.value: ("alt_right", "右Alt"),
    control.alt_left.value: ("alt_left", "左Alt"),
    control.ctrl_right.value: ("ctrl_right", "右Ctrl"),
    control.ctrl_left.value: ("ctrl_left", "左Ctrl"),
    control.shift.value: ("shift", "Shift"),
    control.num_lock.value: ("num_lock", "数字锁定"),
    control.scroll_lock.value: ("scroll_lock", "滚动锁定"),
    control.caps_lock.value: ("caps_lock", "大写锁定"),
    control.enhanced.value: ("enhanced", "增强键"),
}


control._name = "控制键"
