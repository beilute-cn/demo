#!/bin/bash

# 光标键编码查看器

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 清屏
clear

echo -e "${YELLOW}╔════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║     光标键编码实时查看器                  ║${NC}"
echo -e "${YELLOW}╔════════════════════════════════════════════╗${NC}"
echo ""

# 当前模式
MODE="normal"

# 显示帮助
show_help() {
    echo -e "${BLUE}命令:${NC}"
    echo "  1 - 切换到正常模式"
    echo "  2 - 切换到应用模式"
    echo "  h - 显示帮助"
    echo "  q - 退出"
    echo "  其他 - 显示按键编码"
    echo ""
}

# 显示当前模式
show_mode() {
    if [[ $MODE == "normal" ]]; then
        echo -e "${GREEN}当前模式: 正常模式 (CSI)${NC}"
    else
        echo -e "${GREEN}当前模式: 应用模式 (SS3)${NC}"
    fi
    echo ""
}

# 切换到正常模式
set_normal_mode() {
    printf '\033[?1l'
    MODE="normal"
    echo -e "${GREEN}✓ 已切换到正常模式${NC}"
    echo ""
}

# 切换到应用模式
set_app_mode() {
    printf '\033[?1h'
    MODE="application"
    echo -e "${GREEN}✓ 已切换到应用模式${NC}"
    echo ""
}

# 显示编码
show_encoding() {
    local input="$1"
    
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # 识别按键
    case "$input" in
        $'\x1b[A') echo -e "${BLUE}按键: ↑ UP (正常模式)${NC}" ;;
        $'\x1b[B') echo -e "${BLUE}按键: ↓ DOWN (正常模式)${NC}" ;;
        $'\x1b[C') echo -e "${BLUE}按键: → RIGHT (正常模式)${NC}" ;;
        $'\x1b[D') echo -e "${BLUE}按键: ← LEFT (正常模式)${NC}" ;;
        $'\x1bOA') echo -e "${BLUE}按键: ↑ UP (应用模式)${NC}" ;;
        $'\x1bOB') echo -e "${BLUE}按键: ↓ DOWN (应用模式)${NC}" ;;
        $'\x1bOC') echo -e "${BLUE}按键: → RIGHT (应用模式)${NC}" ;;
        $'\x1bOD') echo -e "${BLUE}按键: ← LEFT (应用模式)${NC}" ;;
        *) echo -e "${BLUE}按键: 其他${NC}" ;;
    esac
    
    # 显示十六进制
    echo -n "十六进制: "
    echo -n "$input" | od -An -tx1 | xargs
    
    # 显示十进制
    echo -n "十进制:   "
    echo -n "$input" | od -An -tu1 | xargs
    
    # 显示八进制
    echo -n "八进制:   "
    echo -n "$input" | od -An -to1 | xargs
    
    # 显示字符
    echo -n "字符:     "
    echo "$input" | cat -v
    
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# 初始化
set_normal_mode
show_help
show_mode

# 主循环
while true; do
    # 读取输入
    read -rsn1 char
    
    # 如果是 ESC，读取后续字符
    if [[ $char == $'\x1b' ]]; then
        read -rsn2 -t 0.01 rest
        char="$char$rest"
    fi
    
    # 处理命令
    case "$char" in
        "1")
            set_normal_mode
            show_mode
            ;;
        "2")
            set_app_mode
            show_mode
            ;;
        "h")
            show_help
            ;;
        "q")
            printf '\033[?1l'  # 恢复正常模式
            echo -e "${GREEN}再见！${NC}"
            exit 0
            ;;
        *)
            show_encoding "$char"
            ;;
    esac
done
