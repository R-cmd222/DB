import requests
import json

def test_customer_management():
    """测试客户管理功能"""
    base_url = "http://localhost:9527"
    headers = {
        'Authorization': 'Bearer admin123',
        'Content-Type': 'application/json'
    }
    
    print("=== 客户管理功能测试 ===\n")
    
    # 1. 获取所有客户
    print("1. 获取所有客户...")
    response = requests.get(f"{base_url}/guests", headers=headers)
    if response.status_code == 200:
        customers = response.json()
        print(f"✅ 成功获取 {len(customers)} 个客户")
        for customer in customers:
            print(f"   ID: {customer['id']}, 姓名: {customer['name']}, 积分: {customer['points']}")
    else:
        print(f"❌ 获取客户失败: {response.status_code}")
        return
    
    # 2. 创建新客户
    print(f"\n2. 创建新客户...")
    new_customer = {
        "Name": "测试客户张三",
        "MembershipID": "VIP001",
        "Points": 100
    }
    
    create_response = requests.post(f"{base_url}/guests", headers=headers, json=new_customer)
    if create_response.status_code == 200:
        created_customer = create_response.json()
        print(f"✅ 客户创建成功")
        print(f"   客户ID: {created_customer['id']}")
        print(f"   客户姓名: {created_customer['name']}")
        print(f"   会员ID: {created_customer['membershipID']}")
        print(f"   积分: {created_customer['points']}")
        
        customer_id = created_customer['id']
    else:
        print(f"❌ 创建客户失败: {create_response.status_code}")
        print(f"   错误信息: {create_response.text}")
        return
    
    # 3. 更新客户信息
    print(f"\n3. 更新客户信息...")
    update_data = {
        "Name": "测试客户张三(已更新)",
        "Points": 200
    }
    
    update_response = requests.put(f"{base_url}/guests/{customer_id}", headers=headers, json=update_data)
    if update_response.status_code == 200:
        updated_customer = update_response.json()
        print(f"✅ 客户更新成功")
        print(f"   更新后姓名: {updated_customer['name']}")
        print(f"   更新后积分: {updated_customer['points']}")
    else:
        print(f"❌ 更新客户失败: {update_response.status_code}")
        print(f"   错误信息: {update_response.text}")
    
    # 4. 验证客户列表更新
    print(f"\n4. 验证客户列表更新...")
    verify_response = requests.get(f"{base_url}/guests", headers=headers)
    if verify_response.status_code == 200:
        updated_customers = verify_response.json()
        print(f"✅ 客户列表已更新，共 {len(updated_customers)} 个客户")
        
        # 查找刚创建的客户
        found_customer = None
        for customer in updated_customers:
            if customer['id'] == customer_id:
                found_customer = customer
                break
        
        if found_customer:
            print(f"✅ 找到更新后的客户: {found_customer['name']}, 积分: {found_customer['points']}")
        else:
            print("❌ 未找到更新后的客户")
    else:
        print(f"❌ 验证失败: {verify_response.status_code}")
    
    # 5. 测试重复客户创建
    print(f"\n5. 测试重复客户创建...")
    # 使用更新后的客户名称来测试重复
    duplicate_customer = {
        "Name": "测试客户张三(已更新)",  # 使用更新后的名称
        "MembershipID": "VIP002",
        "Points": 300
    }
    duplicate_response = requests.post(f"{base_url}/guests", headers=headers, json=duplicate_customer)
    if duplicate_response.status_code == 400:
        print("✅ 正确拒绝重复客户创建")
        print(f"   错误信息: {duplicate_response.json()['detail']}")
    else:
        print(f"❌ 应该拒绝重复客户，但返回: {duplicate_response.status_code}")
        print(f"   响应内容: {duplicate_response.text}")
    
    # 6. 删除测试客户
    print(f"\n6. 删除测试客户...")
    delete_response = requests.delete(f"{base_url}/guests/{customer_id}", headers=headers)
    if delete_response.status_code == 200:
        result = delete_response.json()
        print(f"✅ 客户删除成功")
        print(f"   删除信息: {result['message']}")
    else:
        print(f"❌ 删除客户失败: {delete_response.status_code}")
        print(f"   错误信息: {delete_response.text}")
    
    # 7. 最终验证
    print(f"\n7. 最终验证...")
    final_response = requests.get(f"{base_url}/guests", headers=headers)
    if final_response.status_code == 200:
        final_customers = final_response.json()
        print(f"✅ 最终客户数量: {len(final_customers)}")
        
        # 检查测试客户是否已被删除
        test_customer_exists = any(c['id'] == customer_id for c in final_customers)
        if not test_customer_exists:
            print("✅ 测试客户已成功删除")
        else:
            print("❌ 测试客户仍然存在")
    else:
        print(f"❌ 最终验证失败: {final_response.status_code}")
    
    print(f"\n=== 测试完成 ===")

if __name__ == "__main__":
    test_customer_management() 