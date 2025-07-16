@echo off
chcp 65001 > nul
title 股市热点信息获取器

echo ========================================
echo 中国股市热点信息获取器
echo ========================================
echo.

echo 正在启动程序...
echo.

cd /d %~dp0

REM 检查Python是否已安装
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查requests库是否已安装
python -c "import requests" > nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 正在安装requests库...
    pip install requests
    if %errorlevel% neq 0 (
        echo ❌ 错误: 无法安装requests库
        pause
        exit /b 1
    )
)

echo 🚀 运行股市热点信息获取程序...
echo.

REM 运行主程序
python stock_hotspots_scraper.py

echo.
echo ✅ 程序运行完成！
echo.
pause