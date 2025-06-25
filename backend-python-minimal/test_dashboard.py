#!/usr/bin/env python3
"""
测试仪表盘API的数据返回
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_dashboard_sales():
    """测试仪表盘销售额API"""
    print("=== 测试仪表盘销售额API ===")
    
    try:
        response = requests.get(f"{BASE_URL}/dashboard/sales")
        if response.status_code == 200:
            data = response.json()
            print("仪表盘销售额数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 检查必要字段
            required_fields = ['today_sales', 'week_sales', 'last_week_sales', 'month_sales']
            for field in required_fields:
                if field in data:
                    print(f"✓ {field}: ¥{data[field]:.2f}")
                else:
                    print(f"✗ 缺少字段: {field}")
        else:
            print(f"API请求失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"测试仪表盘销售额API时出错: {e}")

def test_top_products():
    """测试热销商品API"""
    print("\n=== 测试热销商品API ===")
    
    try:
        response = requests.get(f"{BASE_URL}/dashboard/top-products?limit=5")
        if response.status_code == 200:
            data = response.json()
            print("热销商品数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            print(f"热销商品数量: {len(data)}")
            
            if data:
                print("前5个热销商品:")
                for i, product in enumerate(data):
                    print(f"  {i+1}. {product['name']}: {product['sales']} 件")
                
                # 检查数据格式
                first_product = data[0] if data else None
                if first_product:
                    required_fields = ['name', 'sales']
                    for field in required_fields:
                        if field in first_product:
                            print(f"✓ 字段 {field} 存在")
                        else:
                            print(f"✗ 缺少字段: {field}")
            else:
                print("⚠ 热销商品数据为空")
        else:
            print(f"API请求失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"测试热销商品API时出错: {e}")

def test_stats():
    """测试基础统计API"""
    print("\n=== 测试基础统计API ===")
    
    try:
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            data = response.json()
            print("基础统计数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 检查必要字段
            required_fields = ['total_products', 'total_orders', 'total_stock', 'low_stock_products']
            for field in required_fields:
                if field in data:
                    print(f"✓ {field}: {data[field]}")
                else:
                    print(f"✗ 缺少字段: {field}")
        else:
            print(f"API请求失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"测试基础统计API时出错: {e}")

def test_health_check():
    """测试健康检查API"""
    print("\n=== 测试健康检查API ===")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ 健康检查API正常")
            print(f"响应: {response.text}")
        else:
            print(f"✗ 健康检查API异常: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"测试健康检查API时出错: {e}")

if __name__ == "__main__":
    print("开始测试仪表盘API...")
    
    # 测试健康检查
    test_health_check()
    
    # 测试基础统计API
    test_stats()
    
    # 测试仪表盘销售额API
    test_dashboard_sales()
    
    # 测试热销商品API
    test_top_products()
    
    print("\n测试完成!") 