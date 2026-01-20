#!/bin/bash

# 正常模式
printf '\033[?1l'

while true; do
    read -rsn1 char
    
    # 检查是否是 ESC
    if [[ $char == $'\x1b' ]]; then
        read -rsn2 -t 0.01 rest
        char="$char$rest"
    fi
    
    # 显示编码
    echo -n "输入: "
    echo -n "$char" | od -An -tx1
    echo ""
    
    # q 退出
    [[ $char == "q" ]] && break
done



# 正常模式
printf '\033[?1h'

while true; do
    read -rsn1 char
    
    # 检查是否是 ESC
    if [[ $char == $'\x1b' ]]; then
        read -rsn2 -t 0.01 rest
        char="$char$rest"
    fi
    
    # 显示编码
    echo -n "输入: "
    echo -n "$char" | od -An -tx1
    echo ""
    
    # q 退出
    [[ $char == "q" ]] && break
done