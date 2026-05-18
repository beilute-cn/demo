@echo off
chcp 65001 >nul
cls

title 测试或修改命令

cd /d %~dp0%
code ..
