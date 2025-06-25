#!/usr/bin/env python3
"""
测试客户等级自动更新功能
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:9527"

def test_customer_level_update():
    """测试客户等级自动更新功能"""
    print("测试客户等级自动更新功能")
    print("=" * 50)
    
    # 测试数据
    test_cases = [
        {"name": "测试客户1", "phone": "13800000001", "points": 1500, "expected_level": "normal"},
        {"name": "测试客户2", "phone": "13800000002", "points": 2500, "expected_level": "vip"},
        {"name": "测试客户3", "phone": "13800000003", "points": 5500, "expected_level": "diamond"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试案例 {i}: {test_case['name']}")
        print(f"积分: {test_case['points']}, 期望等级: {test_case['expected_level']}")
        
        try:
            # 1. 创建测试客户
            create_data = {
                "Name": test_case["name"],
                "Phone": test_case["phone"],
                "Points": test_case["points"],
                "Level": "normal"  # 初始设置为普通客户
            }
            
            response = requests.post(f"{BASE_URL}/guests", json=create_data)
            if response.status_code == 200:
                customer = response.json()
                print(f"   创建客户成功: ID={customer['id']}")
                
                # 2. 更新积分，测试等级自动更新
                update_data = {
                    "Points": test_case["points"]
                    # 不传递Level字段，让后端自动计算
                }
                
                response = requests.put(f"{BASE_URL}/guests/{customer['id']}", json=update_data)
                if response.status_code == 200:
                    updated_customer = response.json()
                    actual_level = updated_customer['level']
                    expected_level = test_case['expected_level']
                    
                    print(f"   更新积分成功")
                    print(f"   实际等级: {actual_level}, 期望等级: {expected_level}")
                    
                    if actual_level == expected_level:
                        print("   ✅ 等级自动更新正确")
                    else:
                        print("   ❌ 等级自动更新错误")
                        
                    # 3. 清理测试数据
                    try:
                        requests.delete(f"{BASE_URL}/guests/{customer['id']}")
                        print("   测试数据已清理")
                    except:
                        print("   清理测试数据失败")
                        
                else:
                    print(f"   ❌ 更新客户失败: {response.status_code}")
                    print(f"   错误信息: {response.text}")
            else:
                print(f"   ❌ 创建客户失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
    
    print("\n测试完成！")
    print("\n功能说明:")
    print("1. 当更新客户积分时，系统会自动根据积分计算客户等级")
    print("2. 积分规则: 0-1999=普通客户, 2000-4999=VIP客户, 5000+=钻石客户")
    print("3. 如果手动设置了等级，则使用手动设置的等级")
    print("4. 如果只更新积分，则根据积分自动更新等级")

if __name__ == "__main__":
    test_customer_level_update() 