#!/usr/bin/env python3
"""
测试积分系统
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

def test_points_system():
    """测试积分系统"""
    print("测试积分系统")
    print("=" * 50)
    
    # 登录获取token
    print("1. 登录获取认证...")
    token = login()
    if not token:
        print("   登录失败，无法进行测试")
        return False
    
    print("   登录成功")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试不同消费金额的积分计算
    test_cases = [
        {"name": "测试客户积分1", "phone": "13900139001", "amount": 50, "expected_points": 500},
        {"name": "测试客户积分2", "phone": "13900139002", "amount": 200, "expected_points": 2000},
        {"name": "测试客户积分3", "phone": "13900139003", "amount": 500, "expected_points": 5000},
        {"name": "测试客户积分4", "phone": "13900139004", "amount": 1000, "expected_points": 10000}
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. 测试消费金额: ¥{test_case['amount']}")
        
        try:
            # 创建测试订单
            checkout_data = {
                "customer_name": test_case["name"],
                "customer_phone": test_case["phone"],
                "items": [
                    {
                        "ProductID": 1,
                        "Quantity": 1,
                        "Price": test_case["amount"]
                    }
                ],
                "total_amount": test_case["amount"],
                "payment_method": "现金",
                "discount": 0
            }
            
            response = requests.post(f"{BASE_URL}/cashier/checkout", json=checkout_data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"   订单创建成功，ID: {result['BillID']}")
                
                # 检查客户积分
                guests_response = requests.get(f"{BASE_URL}/guests")
                if guests_response.status_code == 200:
                    guests = guests_response.json()
                    customer = next((g for g in guests if g['name'] == test_case["name"]), None)
                    if customer:
                        print(f"   客户: {customer['name']}")
                        print(f"   积分: {customer['points']} (期望: {test_case['expected_points']})")
                        print(f"   等级: {customer['level']}")
                        
                        # 验证积分计算
                        if customer['points'] == test_case['expected_points']:
                            print(f"   ✅ 积分计算正确")
                        else:
                            print(f"   ❌ 积分计算错误")
                        
                        # 验证等级晋升
                        expected_level = 'normal'
                        if customer['points'] >= 5000:
                            expected_level = 'diamond'
                        elif customer['points'] >= 2000:
                            expected_level = 'vip'
                        
                        if customer['level'] == expected_level:
                            print(f"   ✅ 等级晋升正确")
                        else:
                            print(f"   ❌ 等级晋升错误，期望: {expected_level}")
                    else:
                        print("   ❌ 未找到客户")
                else:
                    print("   ❌ 获取客户列表失败")
            else:
                print(f"   ❌ 订单创建失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
    
    print("\n积分系统测试完成！")
    return True

def show_points_rules():
    """显示积分规则"""
    print("\n积分规则说明:")
    print("-" * 30)
    print("1. 积分获取: 消费1元获得10积分")
    print("2. 等级晋升:")
    print("   - 普通客户: 0-1999积分")
    print("   - VIP客户: 2000-4999积分")
    print("   - 钻石客户: 5000积分及以上")
    print("3. 晋升条件:")
    print("   - 消费200元晋升VIP客户")
    print("   - 消费500元晋升钻石客户")

if __name__ == "__main__":
    show_points_rules()
    test_points_system() 