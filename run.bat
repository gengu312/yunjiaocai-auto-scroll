@echo off
chcp 65001 >nul
echo ====================================
echo     云教材自动刷课工具启动器
echo ====================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python环境
    echo 请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查依赖是否安装
echo 检查依赖包...
python -c "import pyautogui, pynput" >nul 2>&1
if %errorlevel% neq 0 (
    echo 依赖包未安装，正在自动安装...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo 依赖包安装失败，请手动执行: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo 依赖包安装完成！
)

echo 启动程序...
echo.
echo 提示: 请以管理员身份运行以确保快捷键功能正常工作
echo.

:: 启动主程序
python main.py

if %errorlevel% neq 0 (
    echo.
    echo 程序运行出错，错误代码: %errorlevel%
    echo 请检查错误信息或联系开发者
    pause
)