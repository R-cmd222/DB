#!/usr/bin/env python3
"""
超市管理系统启动脚本
"""

import subprocess
import webbrowser
import time
import os
import sys
from pathlib import Path

def start_backend():
    """启动后端服务器"""
    print("正在启动后端服务器...")
    backend_dir = Path("backend-python-minimal")
    
    if not backend_dir.exists():
        print("错误：找不到后端目录")
        return None
    
    try:
        # 启动后端服务器
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 等待服务器启动
        time.sleep(3)
        
        # 检查服务器是否成功启动
        if process.poll() is None:
            print("✅ 后端服务器启动成功 (http://localhost:8000)")
            return process
        else:
            print("❌ 后端服务器启动失败")
            return None
            
    except Exception as e:
        print(f"启动后端服务器时出错: {e}")
        return None

def start_frontend():
    """启动前端页面"""
    print("正在启动前端页面...")
    
    frontend_file = Path("frontend/supermarket-system.html")
    if not frontend_file.exists():
        print("错误：找不到前端文件")
        return False
    
    try:
        # 打开前端页面
        webbrowser.open(f"file://{frontend_file.absolute()}")
        print("✅ 前端页面已打开")
        return True
    except Exception as e:
        print(f"打开前端页面时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("超市管理系统启动器")
    print("=" * 50)
    
    # 启动后端
    backend_process = start_backend()
    if not backend_process:
        print("无法启动后端服务器，请检查依赖是否正确安装")
        return
    
    # 启动前端
    if start_frontend():
        print("\n🎉 系统启动完成！")
        print("前端页面：supermarket-system.html")
        print("后端API：http://localhost:8000")
        print("API文档：http://localhost:8000/docs")
        print("\n按 Ctrl+C 停止服务器")
        
        try:
            # 保持程序运行
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n正在停止服务器...")
            backend_process.terminate()
            print("服务器已停止")
    else:
        print("前端启动失败")
        backend_process.terminate()

if __name__ == "__main__":
    main() 