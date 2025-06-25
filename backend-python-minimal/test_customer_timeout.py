#!/usr/bin/env python3
"""
测试客户更新API的性能和超时问题
"""

import requests
import time
import json

# API基础URL
BASE_URL = "http://localhost:9527"

def test_customer_update_performance():
    """测试客户更新API的性能"""
    print("测试客户更新API性能")
    print("=" * 50)
    
    try:
        # 1. 获取现有客户
        print("1. 获取现有客户...")
        response = requests.get(f"{BASE_URL}/guests")
        if response.status_code != 200:
            print(f"   ❌ 获取客户失败: {response.status_code}")
            return
        
        customers = response.json()
        if not customers:
            print("   没有找到客户，创建测试客户...")
            # 创建测试客户
            create_data = {
                "Name": "性能测试客户",
                "Phone": "13800000000",
                "Points": 1000,
                "Level": "normal"
            }
            response = requests.post(f"{BASE_URL}/guests", json=create_data)
            if response.status_code == 200:
                test_customer = response.json()
                print(f"   创建测试客户成功: ID={test_customer['id']}")
            else:
                print(f"   ❌ 创建测试客户失败: {response.status_code}")
                return
        else:
            test_customer = customers[0]
            print(f"   使用现有客户: ID={test_customer['id']}, 姓名={test_customer['name']}")
        
        # 2. 测试更新性能
        print("\n2. 测试客户更新性能...")
        test_cases = [
            {"points": 1500, "description": "普通客户积分更新"},
            {"points": 2500, "description": "VIP客户积分更新"},
            {"points": 5500, "description": "钻石客户积分更新"},
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n   测试案例 {i}: {test_case['description']}")
            print(f"   积分: {test_case['points']}")
            
            start_time = time.time()
            
            update_data = {
                "Points": test_case["points"]
            }
            
            try:
                response = requests.put(
                    f"{BASE_URL}/guests/{test_customer['id']}", 
                    json=update_data,
                    timeout=30  # 30秒超时
                )
                
                end_time = time.time()
                duration = end_time - start_time
                
                if response.status_code == 200:
                    updated_customer = response.json()
                    print(f"   ✅ 更新成功")
                    print(f"   耗时: {duration:.2f}秒")
                    print(f"   新等级: {updated_customer['level']}")
                    print(f"   新积分: {updated_customer['points']}")
                    
                    if duration > 5:
                        print(f"   ⚠️  响应时间较长 ({duration:.2f}秒)")
                    elif duration > 10:
                        print(f"   ❌ 响应时间过长 ({duration:.2f}秒)")
                    else:
                        print(f"   ✅ 响应时间正常")
                        
                else:
                    print(f"   ❌ 更新失败: {response.status_code}")
                    print(f"   错误信息: {response.text}")
                    
            except requests.exceptions.Timeout:
                print(f"   ❌ 请求超时 (>30秒)")
            except Exception as e:
                print(f"   ❌ 请求失败: {e}")
        
        # 3. 清理测试数据
        if not customers:  # 如果是我们创建的测试客户
            print(f"\n3. 清理测试数据...")
            try:
                response = requests.delete(f"{BASE_URL}/guests/{test_customer['id']}")
                if response.status_code == 200:
                    print("   ✅ 测试数据已清理")
                else:
                    print(f"   ⚠️  清理测试数据失败: {response.status_code}")
            except Exception as e:
                print(f"   ⚠️  清理测试数据失败: {e}")
        
        print("\n测试完成！")
        print("\n性能优化说明:")
        print("1. 优化了订单统计计算，使用数据库查询而不是加载所有关联对象")
        print("2. 添加了异常处理和事务回滚")
        print("3. 前端添加了重试机制和超时处理")
        print("4. 增加了详细的错误日志")
        
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_customer_update_performance() 