import requests
import json

def test_customer_uniqueness():
    """测试客户唯一性逻辑（姓名+电话号码组合）"""
    base_url = "http://localhost:9527"
    headers = {
        'Authorization': 'Bearer admin123',
        'Content-Type': 'application/json'
    }
    
    print("=== 客户唯一性测试 ===\n")
    
    # 1. 创建第一个客户（有电话号码）
    print("1. 创建第一个客户（姓名: 王丽, 电话: 13800138001）...")
    customer1 = {
        "Name": "王丽",
        "Phone": "13800138001",
        "MembershipID": "VIP001",
        "Points": 100
    }
    
    response1 = requests.post(f"{base_url}/guests", headers=headers, json=customer1)
    if response1.status_code == 200:
        created1 = response1.json()
        print(f"✅ 客户1创建成功，ID: {created1['id']}")
        customer1_id = created1['id']
    else:
        print(f"❌ 客户1创建失败: {response1.status_code}")
        print(f"   错误信息: {response1.text}")
        return
    
    # 2. 尝试创建相同姓名但不同电话号码的客户
    print(f"\n2. 创建相同姓名但不同电话号码的客户（姓名: 王丽, 电话: 13800138002）...")
    customer2 = {
        "Name": "王丽",
        "Phone": "13800138002",
        "MembershipID": "VIP002",
        "Points": 200
    }
    
    response2 = requests.post(f"{base_url}/guests", headers=headers, json=customer2)
    if response2.status_code == 200:
        created2 = response2.json()
        print(f"✅ 客户2创建成功，ID: {created2['id']}")
        customer2_id = created2['id']
    else:
        print(f"❌ 客户2创建失败: {response2.status_code}")
        print(f"   错误信息: {response2.text}")
        return
    
    # 3. 尝试创建相同姓名和电话号码的客户（应该被拒绝）
    print(f"\n3. 尝试创建相同姓名和电话号码的客户（应该被拒绝）...")
    customer3 = {
        "Name": "王丽",
        "Phone": "13800138001",
        "MembershipID": "VIP003",
        "Points": 300
    }
    
    response3 = requests.post(f"{base_url}/guests", headers=headers, json=customer3)
    if response3.status_code == 400:
        print("✅ 正确拒绝重复客户创建")
        print(f"   错误信息: {response3.json()['detail']}")
    else:
        print(f"❌ 应该拒绝重复客户，但返回: {response3.status_code}")
        print(f"   响应内容: {response3.text}")
    
    # 4. 创建没有电话号码的客户
    print(f"\n4. 创建没有电话号码的客户（姓名: 张三）...")
    customer4 = {
        "Name": "张三",
        "MembershipID": "VIP004",
        "Points": 150
    }
    
    response4 = requests.post(f"{base_url}/guests", headers=headers, json=customer4)
    if response4.status_code == 200:
        created4 = response4.json()
        print(f"✅ 客户4创建成功，ID: {created4['id']}")
        customer4_id = created4['id']
    else:
        print(f"❌ 客户4创建失败: {response4.status_code}")
        print(f"   错误信息: {response4.text}")
        return
    
    # 5. 尝试创建相同姓名但没有电话号码的客户（应该被拒绝）
    print(f"\n5. 尝试创建相同姓名但没有电话号码的客户（应该被拒绝）...")
    customer5 = {
        "Name": "张三",
        "MembershipID": "VIP005",
        "Points": 250
    }
    
    response5 = requests.post(f"{base_url}/guests", headers=headers, json=customer5)
    if response5.status_code == 400:
        print("✅ 正确拒绝重复客户创建")
        print(f"   错误信息: {response5.json()['detail']}")
    else:
        print(f"❌ 应该拒绝重复客户，但返回: {response5.status_code}")
        print(f"   响应内容: {response5.text}")
    
    # 6. 验证客户列表
    print(f"\n6. 验证客户列表...")
    list_response = requests.get(f"{base_url}/guests", headers=headers)
    if list_response.status_code == 200:
        customers = list_response.json()
        print(f"✅ 客户列表获取成功，共 {len(customers)} 个客户")
        
        # 查找测试客户
        test_customers = [c for c in customers if c['name'] in ['王丽', '张三']]
        for customer in test_customers:
            print(f"   ID: {customer['id']}, 姓名: {customer['name']}, 电话: {customer['phone'] or '无'}")
    else:
        print(f"❌ 获取客户列表失败: {list_response.status_code}")
    
    # 7. 清理测试数据
    print(f"\n7. 清理测试数据...")
    test_ids = [customer1_id, customer2_id, customer4_id]
    for test_id in test_ids:
        delete_response = requests.delete(f"{base_url}/guests/{test_id}", headers=headers)
        if delete_response.status_code == 200:
            print(f"✅ 删除客户ID {test_id} 成功")
        else:
            print(f"❌ 删除客户ID {test_id} 失败: {delete_response.status_code}")
    
    print(f"\n=== 测试完成 ===")

if __name__ == "__main__":
    test_customer_uniqueness() 