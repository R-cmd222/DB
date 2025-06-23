#!/usr/bin/env python3
"""
超市管理系统启动脚本
支持同时启动后端和 Vue 前端
"""

import subprocess
import webbrowser
import time
import os
import sys
import threading
from pathlib import Path

def check_node_installed():
    """检查 Node.js 是否已安装"""
    try:
        # 在 Windows 上使用 shell=True 来确保能找到命令
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, 
                              text=True, 
                              shell=True)
        if result.returncode == 0:
            print(f"✅ 检测到 Node.js: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Node.js 检测失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Node.js 检测异常: {e}")
        return False

def check_npm_installed():
    """检查 npm 是否已安装"""
    try:
        # 在 Windows 上使用 shell=True 来确保能找到命令
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, 
                              text=True, 
                              shell=True)
        if result.returncode == 0:
            print(f"✅ 检测到 npm: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ npm 检测失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ npm 检测异常: {e}")
        return False

def install_frontend_dependencies():
    """安装前端依赖"""
    print("正在安装前端依赖...")
    frontend_dir = Path("frontend-vue")
    
    try:
        # 检查 node_modules 是否存在
        if (frontend_dir / "node_modules").exists():
            print("✅ 前端依赖已存在，跳过安装")
            return True
        
        # 安装依赖
        result = subprocess.run(
            ['npm', 'install'],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print("✅ 前端依赖安装成功")
            return True
        else:
            print(f"❌ 前端依赖安装失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"安装前端依赖时出错: {e}")
        return False

def start_backend():
    """启动后端服务器"""
    print("正在启动后端服务器...")
    backend_dir = Path("backend-python-minimal")
    log_file_path = Path("backend.log")
    
    if not backend_dir.exists():
        print("错误：找不到后端目录")
        return None, None
    
    try:
        # 打开日志文件
        log_file = open(log_file_path, "w", encoding="utf-8")
        
        # 启动后端服务器
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=backend_dir,
            stdout=log_file,
            stderr=log_file,
            shell=True
        )
        
        # 等待服务器启动
        time.sleep(3)
        
        # 检查服务器是否成功启动
        if process.poll() is None:
            print(f"✅ 后端服务器启动成功 (http://localhost:9527)")
            print(f"   日志文件: {log_file_path.absolute()}")
            return process, log_file
        else:
            print(f"❌ 后端服务器启动失败，请查看日志: {log_file_path.absolute()}")
            log_file.close()
            return None, None
            
    except Exception as e:
        print(f"启动后端服务器时出错: {e}")
        return None, None

def start_vue_frontend():
    """启动 Vue 前端开发服务器"""
    print("正在启动 Vue 前端开发服务器...")
    frontend_dir = Path("frontend-vue")
    log_file_path = Path("frontend.log")
    
    if not frontend_dir.exists():
        print("错误：找不到 Vue 前端目录")
        return None, None
    
    try:
        # 打开日志文件
        log_file = open(log_file_path, "w", encoding="utf-8")
        
        # 启动 Vue 开发服务器
        process = subprocess.Popen(
            ['npm', 'run', 'serve'],
            cwd=frontend_dir,
            stdout=log_file,
            stderr=log_file,
            shell=True
        )
        
        print("等待前端服务器启动...")
        # 增加等待时间，Vue 开发服务器启动较慢
        time.sleep(10)
        
        # 检查服务器是否成功启动
        if process.poll() is None:
            print("✅ Vue 前端开发服务器启动成功 (http://localhost:9528)")
            print(f"   日志文件: {log_file_path.absolute()}")
            return process, log_file
        else:
            print(f"❌ Vue 前端开发服务器启动失败，请查看日志: {log_file_path.absolute()}")
            log_file.close()
            return None, None
            
    except Exception as e:
        print(f"启动 Vue 前端开发服务器时出错: {e}")
        return None, None

def open_browser():
    """延迟打开浏览器"""
    time.sleep(8)  # 等待前端服务器完全启动
    try:
        webbrowser.open("http://localhost:9528")
        print("✅ 浏览器已自动打开前端页面")
    except Exception as e:
        print(f"打开浏览器时出错: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 超市管理系统启动器 (Vue 版)")
    print("=" * 60)
    
    # 检查 Node.js 和 npm
    if not check_node_installed():
        print("❌ 错误：未检测到 Node.js，请先安装 Node.js")
        print("下载地址：https://nodejs.org/")
        return
    
    if not check_npm_installed():
        print("❌ 错误：未检测到 npm，请先安装 npm")
        return
    
    print(f"✅ Node.js 环境检查通过")
    
    # 安装前端依赖
    if not install_frontend_dependencies():
        print("前端依赖安装失败，请手动执行：cd frontend-vue && npm install")
        return
    
    # 启动后端
    backend_process, backend_log = start_backend()
    if not backend_process:
        print("无法启动后端服务器，请检查依赖是否正确安装")
        return
    
    # 启动前端
    frontend_process, frontend_log = start_vue_frontend()
    if not frontend_process:
        print("无法启动前端开发服务器")
        if backend_process:
            backend_process.terminate()
        if backend_log:
            backend_log.close()
        return
    
    # 在后台线程中打开浏览器
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("\n🎉 系统启动完成！")
    print("=" * 60)
    print("📱 前端页面：http://localhost:9528")
    print("🔧 后端API：http://localhost:9527")
    print("📚 API文档：http://localhost:9527/docs")
    print("=" * 60)
    print("💡 提示：")
    print("   - 前端支持热重载，修改代码后会自动刷新")
    print("   - 后端 API 文档可在浏览器中查看")
    print("   - 按 Ctrl+C 停止所有服务")
    print("=" * 60)
    
    try:
        # 保持程序运行，等待用户中断
        while True:
            time.sleep(1)
            # 检查进程是否还在运行
            if backend_process.poll() is not None:
                print("❌ 后端服务器意外停止")
                break
            if frontend_process.poll() is not None:
                print("❌ 前端服务器意外停止")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 正在停止所有服务...")
        
        # 停止前端
        if frontend_process and frontend_process.poll() is None:
            print("正在停止前端服务...")
            if sys.platform == "win32":
                subprocess.run(f"taskkill /F /PID {frontend_process.pid} /T", shell=True, capture_output=True)
            else:
                frontend_process.terminate()
            if frontend_log:
                frontend_log.close()
            print("✅ 前端开发服务器已停止")
        
        # 停止后端
        if backend_process and backend_process.poll() is None:
            print("正在停止后端服务...")
            if sys.platform == "win32":
                subprocess.run(f"taskkill /F /PID {backend_process.pid} /T", shell=True, capture_output=True)
            else:
                backend_process.terminate()
            if backend_log:
                backend_log.close()
            print("✅ 后端服务器已停止")

        print("🎯 所有服务已停止")

if __name__ == "__main__":
    main() 