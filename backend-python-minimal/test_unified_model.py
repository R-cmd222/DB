import requests
import json

def test_unified_customer_model():
    """测试统一后的客户数据模型"""
    base_url = "http://localhost:9527"
    headers = {
        'Authorization': 'Bearer admin123',
        'Content-Type': 'application/json'
    }
    
    print("=== 统一客户数据模型测试 ===\n")
    
    # 1. 获取所有客户，检查返回的字段
    print("1. 获取所有客户，检查返回字段...")
    response = requests.get(f"{base_url}/guests", headers=headers)
    if response.status_code == 200:
        customers = response.json()
        print(f"✅ 成功获取 {len(customers)} 个客户")
        
        if customers:
            # 检查第一个客户的字段
            first_customer = customers[0]
            print(f"客户字段结构:")
            for key, value in first_customer.items():
                print(f"  {key}: {value} (类型: {type(value).__name__})")
            
            # 检查是否包含扩展字段
            extended_fields = ['email', 'level', 'createdAt', 'address', 'notes', 'totalSpent']
            found_extended = [field for field in extended_fields if field in first_customer]
            if found_extended:
                print(f"❌ 发现扩展字段: {found_extended}")
            else:
                print("✅ 没有发现扩展字段，数据模型已统一")
        else:
            print("没有客户数据")
    else:
        print(f"❌ 获取客户失败: {response.status_code}")
        return
    
    # 2. 创建新客户，测试完整字段
    print(f"\n2. 创建新客户，测试完整字段...")
    new_customer = {
        "Name": "统一模型测试客户",
        "Phone": "13800138003",
        "MembershipID": "TEST001",
        "Points": 500
    }
    
    create_response = requests.post(f"{base_url}/guests", headers=headers, json=new_customer)
    if create_response.status_code == 200:
        created_customer = create_response.json()
        print(f"✅ 客户创建成功")
        print(f"返回字段:")
        for key, value in created_customer.items():
            print(f"  {key}: {value}")
        
        customer_id = created_customer['id']
        
        # 3. 更新客户，测试字段更新
        print(f"\n3. 更新客户信息...")
        update_data = {
            "Name": "统一模型测试客户(已更新)",
            "Points": 1000
        }
        
        update_response = requests.put(f"{base_url}/guests/{customer_id}", headers=headers, json=update_data)
        if update_response.status_code == 200:
            updated_customer = update_response.json()
            print(f"✅ 客户更新成功")
            print(f"更新后字段:")
            for key, value in updated_customer.items():
                print(f"  {key}: {value}")
        else:
            print(f"❌ 更新失败: {update_response.status_code}")
            print(f"错误信息: {update_response.text}")
        
        # 4. 删除测试客户
        print(f"\n4. 清理测试数据...")
        delete_response = requests.delete(f"{base_url}/guests/{customer_id}", headers=headers)
        if delete_response.status_code == 200:
            print(f"✅ 测试客户删除成功")
        else:
            print(f"❌ 删除失败: {delete_response.status_code}")
    
    else:
        print(f"❌ 创建客户失败: {create_response.status_code}")
        print(f"错误信息: {create_response.text}")
    
    print(f"\n=== 测试完成 ===")

if __name__ == "__main__":
    test_unified_customer_model() 