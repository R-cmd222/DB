#!/usr/bin/env python3
"""
测试商品分类分析API的新功能
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_product_report():
    """测试商品分析API"""
    print("=== 测试商品分析API ===")
    
    try:
        # 测试商品分析API
        response = requests.get(f"{BASE_URL}/report/product")
        if response.status_code == 200:
            data = response.json()
            print("商品分析数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 检查必要字段
            required_fields = ['totalProducts', 'topProducts', 'categorySales', 'priceRanges']
            for field in required_fields:
                if field in data:
                    if field == 'topProducts':
                        print(f"✓ {field}: {len(data[field])} 个商品")
                    elif field == 'categorySales':
                        print(f"✓ {field}: {len(data[field])} 个商品类别")
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

def test_category_sales_data():
    """测试商品分类销量数据"""
    print("\n=== 测试商品分类销量数据 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/report/product")
        if response.status_code == 200:
            data = response.json()
            
            # 检查商品分类销量数据
            category_sales = data.get('categorySales', [])
            print(f"商品分类销量数据:")
            print(f"  分类数量: {len(category_sales)}")
            
            if category_sales:
                print("  各分类销量排行:")
                for i, category in enumerate(category_sales):
                    print(f"    {i+1}. {category['name']}: {category['sales']} 件 (¥{category['revenue']:.2f})")
                
                # 检查数据格式
                first_category = category_sales[0] if category_sales else None
                if first_category:
                    required_fields = ['name', 'sales', 'revenue']
                    for field in required_fields:
                        if field in first_category:
                            print(f"✓ 字段 {field} 存在")
                        else:
                            print(f"✗ 缺少字段: {field}")
            else:
                print("⚠ 商品分类销量数据为空")
                
    except Exception as e:
        print(f"测试商品分类销量数据时出错: {e}")

def test_customer_report():
    """测试客户分析API"""
    print("\n=== 测试客户分析API ===")
    
    try:
        response = requests.get(f"{BASE_URL}/report/customer")
        if response.status_code == 200:
            data = response.json()
            
            # 检查客户消费排行数据
            top_customers = data.get('topCustomers', [])
            print(f"客户消费排行数据:")
            print(f"  客户数量: {len(top_customers)}")
            
            if top_customers:
                print("  前5个客户:")
                for i, customer in enumerate(top_customers[:5]):
                    print(f"    {i+1}. {customer['name']} ({customer['level']}): ¥{customer['totalSpent']:.2f} ({customer['orderCount']} 单)")
                
                # 检查数据格式
                first_customer = top_customers[0] if top_customers else None
                if first_customer:
                    required_fields = ['rank', 'name', 'level', 'totalSpent', 'orderCount', 'lastOrderDate']
                    for field in required_fields:
                        if field in first_customer:
                            print(f"✓ 字段 {field} 存在")
                        else:
                            print(f"✗ 缺少字段: {field}")
            else:
                print("⚠ 客户消费排行数据为空")
                
    except Exception as e:
        print(f"测试客户分析API时出错: {e}")

if __name__ == "__main__":
    print("开始测试商品分类分析和客户消费排行功能...")
    
    # 测试商品分析API
    test_product_report()
    
    # 测试商品分类销量数据
    test_category_sales_data()
    
    # 测试客户分析API
    test_customer_report()
    
    print("\n测试完成!") 