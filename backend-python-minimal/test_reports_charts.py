#!/usr/bin/env python3
"""
测试报表统计中的客户分析和商品分析API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_customer_report():
    """测试客户分析API"""
    print("=== 测试客户分析API ===")
    
    try:
        # 测试客户分析API
        response = requests.get(f"{BASE_URL}/report/customer")
        if response.status_code == 200:
            data = response.json()
            print("客户分析数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 检查必要字段
            required_fields = ['totalCustomers', 'normalCustomers', 'vipCustomers', 'diamondCustomers']
            for field in required_fields:
                if field in data:
                    print(f"✓ {field}: {data[field]}")
                else:
                    print(f"✗ 缺少字段: {field}")
        else:
            print(f"API请求失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"测试客户分析API时出错: {e}")

def test_product_report():
    """测试商品分析API"""
    print("\n=== 测试商品分析API ===")
    
    try:
        # 测试商品分析API
        response = requests.get(f"{BASE_URL}/report/product")
        if response.status_code == 200:
            data = response.json()
            print("商品分析数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 检查必要字段
            required_fields = ['totalProducts', 'topProducts', 'priceRanges']
            for field in required_fields:
                if field in data:
                    if field == 'topProducts':
                        print(f"✓ {field}: {len(data[field])} 个商品")
                    elif field == 'priceRanges':
                        print(f"✓ {field}: {len(data[field])} 个价格区间")
                    else:
                        print(f"✓ {field}: {data[field]}")
                else:
                    print(f"✗ 缺少字段: {field}")
        else:
            print(f"API请求失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"测试商品分析API时出错: {e}")

def test_chart_data():
    """测试图表数据格式"""
    print("\n=== 测试图表数据格式 ===")
    
    try:
        # 测试客户分析
        response = requests.get(f"{BASE_URL}/report/customer")
        if response.status_code == 200:
            data = response.json()
            
            # 检查客户等级分布数据
            normal_count = data.get('normalCustomers', 0)
            vip_count = data.get('vipCustomers', 0)
            diamond_count = data.get('diamondCustomers', 0)
            
            print(f"客户等级分布数据:")
            print(f"  普通客户: {normal_count}")
            print(f"  VIP客户: {vip_count}")
            print(f"  钻石客户: {diamond_count}")
            print(f"  总计: {normal_count + vip_count + diamond_count}")
            
            if normal_count + vip_count + diamond_count > 0:
                print("✓ 客户等级分布数据有效")
            else:
                print("⚠ 客户等级分布数据为空")
        
        # 测试商品分析
        response = requests.get(f"{BASE_URL}/report/product")
        if response.status_code == 200:
            data = response.json()
            
            # 检查商品销量排行数据
            top_products = data.get('topProducts', [])
            print(f"\n商品销量排行数据:")
            print(f"  商品数量: {len(top_products)}")
            
            if top_products:
                print("  前5个商品:")
                for i, product in enumerate(top_products[:5]):
                    print(f"    {i+1}. {product['name']}: {product['sales']} 件")
            
            # 检查价格分布数据
            price_ranges = data.get('priceRanges', [])
            print(f"\n价格分布数据:")
            print(f"  价格区间数量: {len(price_ranges)}")
            
            if price_ranges:
                print("  各价格区间商品数量:")
                for price_range in price_ranges:
                    print(f"    {price_range['range']}: {price_range['count']} 个商品")
            
            if top_products or price_ranges:
                print("✓ 商品分析数据有效")
            else:
                print("⚠ 商品分析数据为空")
                
    except Exception as e:
        print(f"测试图表数据格式时出错: {e}")

if __name__ == "__main__":
    print("开始测试报表统计API...")
    
    # 测试客户分析API
    test_customer_report()
    
    # 测试商品分析API
    test_product_report()
    
    # 测试图表数据格式
    test_chart_data()
    
    print("\n测试完成!") 