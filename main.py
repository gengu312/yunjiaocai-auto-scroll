#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云教材自动刷课程序
主程序入口文件
"""

import sys
import os
import json
import threading
import time
from tkinter import *
from tkinter import ttk, messagebox
import pyautogui

# 禁用pyautogui的安全机制
pyautogui.FAILSAFE = False

class AutoScrollApp:
    def __init__(self, root):
        self.root = root
        self.root.title("云教材自动刷课工具 v1.0")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        
        # 配置文件路径
        self.config_file = "config.json"
        
        # 默认配置
        self.config = {
            "scroll_distance": 100,
            "scroll_speed": 0.1,
            "scroll_duration": 10,
            "scroll_direction": "down"
        }
        
        # 运行状态
        self.is_running = False
        self.scroll_thread = None
        
        # 加载配置
        self.load_config()
        
        # 创建GUI
        self.create_widgets()
        
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")
    
    def create_widgets(self):
        """创建GUI界面"""
        # 主标题
        title_label = Label(self.root, text="云教材自动刷课工具", 
                           font=("微软雅黑", 16, "bold"), fg="#2E86AB")
        title_label.pack(pady=15)
        
        # 配置框架
        config_frame = LabelFrame(self.root, text="参数配置", font=("微软雅黑", 10))
        config_frame.pack(fill="x", padx=20, pady=10)
        
        # 滚动距离
        distance_frame = Frame(config_frame)
        distance_frame.pack(fill="x", padx=10, pady=8)
        Label(distance_frame, text="滚动距离:", width=12, anchor="w", font=("微软雅黑", 9)).pack(side="left")
        self.distance_var = IntVar(value=self.config["scroll_distance"])
        distance_scale = Scale(distance_frame, from_=10, to=500, orient="horizontal",
                              variable=self.distance_var, length=250)
        distance_scale.pack(side="left", padx=5)
        Label(distance_frame, text="像素", font=("微软雅黑", 9)).pack(side="left")
        
        # 滚动速度
        speed_frame = Frame(config_frame)
        speed_frame.pack(fill="x", padx=10, pady=8)
        Label(speed_frame, text="滚动速度:", width=12, anchor="w", font=("微软雅黑", 9)).pack(side="left")
        self.speed_var = DoubleVar(value=self.config["scroll_speed"])
        speed_scale = Scale(speed_frame, from_=0.01, to=1.0, resolution=0.01,
                           orient="horizontal", variable=self.speed_var, length=250)
        speed_scale.pack(side="left", padx=5)
        Label(speed_frame, text="秒/次", font=("微软雅黑", 9)).pack(side="left")
        
        # 持续时间
        duration_frame = Frame(config_frame)
        duration_frame.pack(fill="x", padx=10, pady=8)
        Label(duration_frame, text="持续时间:", width=12, anchor="w", font=("微软雅黑", 9)).pack(side="left")
        self.duration_var = IntVar(value=self.config["scroll_duration"])
        duration_scale = Scale(duration_frame, from_=1, to=300, orient="horizontal",
                              variable=self.duration_var, length=250)
        duration_scale.pack(side="left", padx=5)
        Label(duration_frame, text="秒", font=("微软雅黑", 9)).pack(side="left")
        
        # 滚动方向
        direction_frame = Frame(config_frame)
        direction_frame.pack(fill="x", padx=10, pady=8)
        Label(direction_frame, text="滚动方向:", width=12, anchor="w", font=("微软雅黑", 9)).pack(side="left")
        self.direction_var = StringVar(value=self.config["scroll_direction"])
        direction_combo = ttk.Combobox(direction_frame, textvariable=self.direction_var,
                                      values=["down", "up", "both"], state="readonly", width=20)
        direction_combo.pack(side="left", padx=5)
        
        # 控制按钮框架
        control_frame = LabelFrame(self.root, text="控制面板", font=("微软雅黑", 10))
        control_frame.pack(fill="x", padx=20, pady=15)
        
        # 倒计时显示
        self.countdown_var = StringVar(value="准备就绪")
        countdown_label = Label(control_frame, textvariable=self.countdown_var, 
                               font=("微软雅黑", 12, "bold"), fg="#28A745")
        countdown_label.pack(pady=10)
        
        # 按钮框架
        button_frame = Frame(control_frame)
        button_frame.pack(pady=10)
        
        # 开始按钮
        self.start_btn = Button(button_frame, text="开始滚动 (3秒后)", command=self.start_scroll_with_countdown,
                               bg="#28A745", fg="white", font=("微软雅黑", 11, "bold"), width=15, height=2)
        self.start_btn.pack(side="left", padx=10)
        
        # 停止按钮
        self.stop_btn = Button(button_frame, text="停止滚动", command=self.stop_scrolling,
                              bg="#DC3545", fg="white", font=("微软雅黑", 11, "bold"), width=15, height=2)
        self.stop_btn.pack(side="left", padx=10)
        self.stop_btn.config(state="disabled")
        
        # 配置按钮框架
        config_btn_frame = Frame(self.root)
        config_btn_frame.pack(fill="x", padx=20, pady=10)
        
        # 保存配置按钮
        save_btn = Button(config_btn_frame, text="保存配置", command=self.save_current_config,
                         bg="#17A2B8", fg="white", font=("微软雅黑", 10), width=12)
        save_btn.pack(side="left", padx=5)
        
        # 测试按钮
        test_btn = Button(config_btn_frame, text="测试滚动", command=self.test_scroll,
                         bg="#FFC107", fg="black", font=("微软雅黑", 10), width=12)
        test_btn.pack(side="left", padx=5)
        
        # 使用说明
        help_frame = LabelFrame(self.root, text="使用说明", font=("微软雅黑", 10))
        help_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        help_text = """1. 调整滚动参数（距离、速度、时间、方向）
2. 点击'保存配置'保存设置
3. 将鼠标移动到目标滚动条位置
4. 点击'开始滚动'按钮
5. 程序会倒计时3秒后开始自动滚动
6. 点击'停止滚动'可随时停止

注意：开始前请确保鼠标在正确位置！"""
        
        help_label = Label(help_frame, text=help_text, justify="left",
                          font=("微软雅黑", 9), fg="#666666")
        help_label.pack(anchor="w", padx=10, pady=10)
    
    def save_current_config(self):
        """保存当前配置"""
        try:
            self.config["scroll_distance"] = self.distance_var.get()
            self.config["scroll_speed"] = self.speed_var.get()
            self.config["scroll_duration"] = self.duration_var.get()
            self.config["scroll_direction"] = self.direction_var.get()
            
            self.save_config()
            messagebox.showinfo("成功", "配置已保存！")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")
    
    def test_scroll(self):
        """测试滚动功能"""
        if self.is_running:
            messagebox.showwarning("警告", "滚动正在进行中，请先停止！")
            return
        
        # 给用户3秒时间准备
        self.start_scroll_with_countdown()
    
    def start_scroll_with_countdown(self):
        """带倒计时的开始滚动"""
        if self.is_running:
            self.stop_scrolling()
            return
        
        # 禁用开始按钮
        self.start_btn.config(state="disabled")
        
        # 开始倒计时
        def countdown():
            for i in range(3, 0, -1):
                self.countdown_var.set(f"倒计时: {i} 秒")
                self.root.update()
                time.sleep(1)
                if not self.start_btn.cget("state") == "disabled":
                    return  # 如果按钮被重新启用，说明被取消了
            
            self.countdown_var.set("开始滚动...")
            self.start_scrolling()
        
        # 在新线程中执行倒计时
        countdown_thread = threading.Thread(target=countdown)
        countdown_thread.daemon = True
        countdown_thread.start()
    
    def start_scrolling(self):
        """开始滚动"""
        self.is_running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.countdown_var.set("正在滚动中...")
        
        # 在新线程中执行滚动
        self.scroll_thread = threading.Thread(target=self.scroll_worker)
        self.scroll_thread.daemon = True
        self.scroll_thread.start()
    
    def stop_scrolling(self):
        """停止滚动"""
        self.is_running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.countdown_var.set("已停止")
        
        # 释放鼠标按键
        try:
            pyautogui.mouseUp()
        except:
            pass
        
        # 1秒后恢复准备状态
        def reset_status():
            time.sleep(1)
            if not self.is_running:
                self.countdown_var.set("准备就绪")
        
        reset_thread = threading.Thread(target=reset_status)
        reset_thread.daemon = True
        reset_thread.start()
    
    def scroll_worker(self):
        """滚动工作线程"""
        try:
            # 获取当前鼠标位置
            start_x, start_y = pyautogui.position()
            
            # 获取配置参数
            distance = self.distance_var.get()
            speed = self.speed_var.get()
            duration = self.duration_var.get()
            direction = self.direction_var.get()
            
            # 按住鼠标左键
            pyautogui.mouseDown(start_x, start_y)
            
            start_time = time.time()
            
            while self.is_running and (time.time() - start_time) < duration:
                if direction == "down":
                    # 向下滚动
                    pyautogui.moveTo(start_x, start_y + distance, duration=speed)
                    if not self.is_running:
                        break
                    time.sleep(speed)
                    pyautogui.moveTo(start_x, start_y, duration=speed)
                    
                elif direction == "up":
                    # 向上滚动
                    pyautogui.moveTo(start_x, start_y - distance, duration=speed)
                    if not self.is_running:
                        break
                    time.sleep(speed)
                    pyautogui.moveTo(start_x, start_y, duration=speed)
                    
                elif direction == "both":
                    # 上下滚动
                    pyautogui.moveTo(start_x, start_y + distance, duration=speed)
                    if not self.is_running:
                        break
                    time.sleep(speed)
                    pyautogui.moveTo(start_x, start_y - distance, duration=speed)
                    if not self.is_running:
                        break
                    time.sleep(speed)
                    pyautogui.moveTo(start_x, start_y, duration=speed)
                
                time.sleep(speed)
            
            # 释放鼠标
            pyautogui.mouseUp()
            
        except Exception as e:
            print(f"滚动过程中出错: {e}")
            messagebox.showerror("错误", f"滚动过程中出错: {e}")
        finally:
            self.is_running = False
            self.root.after(0, self.stop_scrolling)  # 在主线程中更新GUI
    
    def on_closing(self):
        """程序关闭时的清理工作"""
        self.is_running = False
        try:
            pyautogui.mouseUp()
        except:
            pass
        self.root.destroy()

def main():
    """主函数"""
    root = Tk()
    app = AutoScrollApp(root)
    
    # 设置关闭事件
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # 启动GUI
    root.mainloop()

if __name__ == "__main__":
    main()