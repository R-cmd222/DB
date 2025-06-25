#!/usr/bin/env python3
"""
测试客户等级系统
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

def test_customer_api():
    """测试客户API"""
    print("测试客户等级系统")
    print("=" * 50)
    
    # 登录获取token
    print("0. 登录获取认证...")
    token = login()
    if not token:
        print("   登录失败，无法进行需要认证的测试")
        return False
    
    print("   登录成功")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试获取客户列表
    print("\n1. 获取客户列表...")
    try:
        response = requests.get(f"{BASE_URL}/guests")
        if response.status_code == 200:
            customers = response.json()
            print(f"   成功获取 {len(customers)} 个客户")
            
            # 显示客户等级分布
            level_counts = {}
            for customer in customers:
                level = customer.get('level', 'unknown')
                level_counts[level] = level_counts.get(level, 0) + 1
            
            print("   客户等级分布:")
            for level, count in level_counts.items():
                level_name = {
                    'normal': '普通客户',
                    'vip': 'VIP客户',
                    'diamond': '钻石客户'
                }.get(level, level)
                print(f"     {level_name}: {count} 人")
            
            # 显示前3个客户详情
            print("   前3个客户详情:")
            for i, customer in enumerate(customers[:3]):
                level_name = {
                    'normal': '普通客户',
                    'vip': 'VIP客户',
                    'diamond': '钻石客户'
                }.get(customer.get('level', 'unknown'), customer.get('level', 'unknown'))
                
                print(f"     {i+1}. {customer['name']} - {level_name} - 积分: {customer['points']}")
        else:
            print(f"   失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   错误: {e}")
        return False
    
    # 测试创建新客户
    print("\n2. 测试创建新客户...")
    try:
        new_customer = {
            "Name": "测试客户等级",
            "Level": "vip",
            "Points": 1500,
            "Phone": "13800138000"
        }
        
        response = requests.post(f"{BASE_URL}/guests", json=new_customer, headers=headers)
        if response.status_code == 200:
            created_customer = response.json()
            print(f"   成功创建客户: {created_customer['name']} - {created_customer['level']}")
            
            # 测试更新客户等级
            print("\n3. 测试更新客户等级...")
            update_data = {
                "Level": "diamond",
                "Points": 3500
            }
            
            response = requests.put(f"{BASE_URL}/guests/{created_customer['id']}", json=update_data, headers=headers)
            if response.status_code == 200:
                updated_customer = response.json()
                print(f"   成功更新客户等级: {updated_customer['name']} - {updated_customer['level']} - 积分: {updated_customer['points']}")
            else:
                print(f"   更新失败: {response.status_code}")
        else:
            print(f"   创建失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    # 测试客户报表
    print("\n4. 测试客户报表...")
    try:
        response = requests.get(f"{BASE_URL}/report/customer")
        if response.status_code == 200:
            report = response.json()
            print("   客户报表数据:")
            print(f"     总客户数: {report['totalCustomers']}")
            print(f"     活跃客户: {report['activeCustomers']}")
            print(f"     VIP客户: {report['vipCustomers']}")
            print(f"     钻石客户: {report.get('diamondCustomers', 0)}")
            print(f"     普通客户: {report.get('normalCustomers', 0)}")
        else:
            print(f"   报表获取失败: {response.status_code}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n测试完成！")
    return True

if __name__ == "__main__":
    test_customer_api() 