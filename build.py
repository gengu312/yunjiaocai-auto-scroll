#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 将程序打包成exe文件
使用PyInstaller进行打包
"""

import os
import sys
import subprocess
import shutil

def build_exe():
    """打包程序为exe文件"""
    print("开始打包程序...")
    
    # 确保在正确的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 清理之前的构建文件
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('main.spec'):
        os.remove('main.spec')
    
    # PyInstaller命令参数
    cmd = [
        'pyinstaller',
        '--onefile',                    # 打包成单个exe文件
        '--windowed',                   # 不显示控制台窗口
        '--name=云教材刷课工具',          # 设置exe文件名
        '--icon=icon.ico',              # 图标文件（如果有的话）
        '--add-data=config.json;.',     # 包含配置文件
        '--hidden-import=pynput.keyboard._win32',
        '--hidden-import=pynput.mouse._win32',
        '--hidden-import=PIL._tkinter_finder',
        'main.py'
    ]
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("打包成功！")
        print(f"输出目录: {os.path.join(script_dir, 'dist')}")
        
        # 复制配置文件到输出目录
        dist_dir = os.path.join(script_dir, 'dist')
        if os.path.exists('config.json'):
            shutil.copy2('config.json', dist_dir)
            print("配置文件已复制到输出目录")
        
        print("\n打包完成！可执行文件位于 dist 目录中。")
        
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except FileNotFoundError:
        print("错误: 未找到 pyinstaller，请先安装：pip install pyinstaller")
        return False
    
    return True

def install_dependencies():
    """安装依赖包"""
    print("安装依赖包...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("依赖包安装完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装依赖包失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("云教材刷课工具 - 打包脚本")
    print("=" * 50)
    
    # 检查是否存在requirements.txt
    if not os.path.exists('requirements.txt'):
        print("错误: 未找到 requirements.txt 文件")
        return
    
    # 询问是否安装依赖
    install_deps = input("是否需要安装依赖包？(y/n): ").lower().strip()
    if install_deps in ['y', 'yes', '是']:
        if not install_dependencies():
            print("依赖包安装失败，无法继续打包")
            return
    
    # 开始打包
    build_confirm = input("开始打包程序？(y/n): ").lower().strip()
    if build_confirm in ['y', 'yes', '是']:
        build_exe()
    else:
        print("取消打包")

if __name__ == "__main__":
    main()