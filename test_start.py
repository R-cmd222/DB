#!/usr/bin/env python3
"""
测试启动脚本
"""

import subprocess
import time
import sys
from pathlib import Path

def test_npm():
    """测试 npm 命令"""
    print("测试 npm 命令...")
    try:
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, 
                              text=True, 
                              shell=True)
        print(f"npm 版本: {result.stdout.strip()}")
        print(f"返回码: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"npm 测试失败: {e}")
        return False

def test_vue_cli():
    """测试 vue-cli-service"""
    print("\n测试 vue-cli-service...")
    frontend_dir = Path("frontend-vue")
    if not frontend_dir.exists():
        print("frontend-vue 目录不存在")
        return False
    
    try:
        result = subprocess.run(['npx', 'vue-cli-service', '--version'], 
                              cwd=frontend_dir,
                              capture_output=True, 
                              text=True, 
                              shell=True)
        print(f"vue-cli-service 版本: {result.stdout.strip()}")
        print(f"返回码: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"vue-cli-service 测试失败: {e}")
        return False

def test_npm_serve():
    """测试 npm run serve"""
    print("\n测试 npm run serve...")
    frontend_dir = Path("frontend-vue")
    
    try:
        # 启动服务
        process = subprocess.Popen(
            ['npm', 'run', 'serve'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        
        print("等待 5 秒...")
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ 进程正在运行")
            stdout, stderr = process.communicate(timeout=1)
            if stderr:
                print(f"错误输出: {stderr.decode('utf-8', errors='ignore')}")
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ 进程已退出，返回码: {process.returncode}")
            if stderr:
                print(f"错误输出: {stderr.decode('utf-8', errors='ignore')}")
            return False
            
    except Exception as e:
        print(f"测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("启动诊断测试")
    print("=" * 50)
    
    test_npm()
    test_vue_cli()
    test_npm_serve()
    
    print("\n诊断完成") 