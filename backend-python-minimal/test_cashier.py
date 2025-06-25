#!/usr/bin/env python3
"""
测试收银台功能
"""

import requests
import json

BASE_URL = "http://localhost:9527"

def login():
    """登录获取token"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        if response.status_code == 200:
            return response.json().get("token")
        else:
            print(f"登录失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"登录错误: {e}")
        return None

def test_cashier_checkout():
    """测试收银台结算"""
    print("测试收银台结算功能")
    print("=" * 50)
    
    # 登录获取token
    print("1. 登录获取认证...")
    token = login()
    if not token:
        print("   登录失败，无法进行测试")
        return False
    
    print("   登录成功")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试收银台结算
    print("\n2. 测试收银台结算...")
    try:
        checkout_data = {
            "customer_name": "测试客户收银台",
            "customer_phone": "13900139000",
            "items": [
                {
                    "ProductID": 1,
                    "Quantity": 2,
                    "Price": 10.50
                },
                {
                    "ProductID": 2,
                    "Quantity": 1,
                    "Price": 25.00
                }
            ],
            "total_amount": 46.00,
            "payment_method": "现金",
            "discount": 0
        }
        
        response = requests.post(f"{BASE_URL}/cashier/checkout", json=checkout_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"   结算成功！")
            print(f"   订单ID: {result['BillID']}")
            print(f"   客户: {result.get('guest_name', 'N/A')}")
            print(f"   总金额: ¥{result['TotalAmount']}")
            print(f"   支付方式: {result['PaymentMethod']}")
            print(f"   订单状态: {result['Status']}")
            print(f"   商品数量: {len(result['items'])}")
            
            # 检查库存是否更新
            print("\n3. 检查库存更新...")
            for item in result['items']:
                product_response = requests.get(f"{BASE_URL}/products/{item['ProductID']}")
                if product_response.status_code == 200:
                    product = product_response.json()
                    print(f"   商品: {product['Name']}, 库存: {product['Stock']}")
            
            # 检查客户信息
            print("\n4. 检查客户信息...")
            guests_response = requests.get(f"{BASE_URL}/guests")
            if guests_response.status_code == 200:
                guests = guests_response.json()
                test_customer = next((g for g in guests if g['name'] == "测试客户收银台"), None)
                if test_customer:
                    print(f"   客户: {test_customer['name']}")
                    print(f"   电话: {test_customer['phone']}")
                    print(f"   等级: {test_customer['level']}")
                    print(f"   积分: {test_customer['points']}")
                else:
                    print("   未找到测试客户")
            
        else:
            print(f"   结算失败: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   错误: {e}")
        return False
    
    print("\n测试完成！")
    return True

if __name__ == "__main__":
    test_cashier_checkout() 