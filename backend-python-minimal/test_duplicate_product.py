import requests
import json

# 测试重复商品检查功能
def test_duplicate_product_check():
    base_url = "http://localhost:9527"
    headers = {
        'Authorization': 'Bearer admin123',
        'Content-Type': 'application/json'
    }
    
    # 1. 首先获取所有商品
    print("1. 获取所有商品...")
    response = requests.get(f"{base_url}/products", headers=headers)
    if response.status_code == 200:
        products = response.json()
        print(f"找到 {len(products)} 个商品")
        
        if products:
            # 2. 选择第一个商品作为测试基准
            first_product = products[0]
            print(f"\n2. 选择测试商品: {first_product['Name']} (价格: ¥{first_product['Price']})")
            
            # 3. 尝试添加相同名称和价格的商品
            duplicate_product = {
                "Name": first_product['Name'],
                "Price": first_product['Price'],
                "Stock": 50,
                "Category": first_product['Category'],
                "Unit": "个"
            }
            
            print(f"\n3. 尝试添加重复商品...")
            print(f"   商品名称: {duplicate_product['Name']}")
            print(f"   商品价格: ¥{duplicate_product['Price']}")
            
            create_response = requests.post(f"{base_url}/products", 
                                          headers=headers, 
                                          json=duplicate_product)
            
            print(f"创建响应状态码: {create_response.status_code}")
            print(f"创建响应内容: {create_response.text}")
            
            if create_response.status_code == 400:
                result = create_response.json()
                if "已存在" in result.get('detail', ''):
                    print("✅ 重复商品检查功能正常！")
                    print(f"   错误信息: {result['detail']}")
                else:
                    print("❌ 重复商品检查功能异常")
            else:
                print("❌ 应该拒绝重复商品，但创建成功了")
            
            # 4. 尝试添加相同名称但不同价格的商品（应该成功）
            print(f"\n4. 尝试添加相同名称但不同价格的商品...")
            different_price_product = {
                "Name": first_product['Name'],
                "Price": first_product['Price'] + 1.0,  # 价格加1
                "Stock": 30,
                "Category": first_product['Category'],
                "Unit": "个"
            }
            
            print(f"   商品名称: {different_price_product['Name']}")
            print(f"   商品价格: ¥{different_price_product['Price']}")
            
            create_response2 = requests.post(f"{base_url}/products", 
                                           headers=headers, 
                                           json=different_price_product)
            
            print(f"创建响应状态码: {create_response2.status_code}")
            
            if create_response2.status_code == 200:
                print("✅ 不同价格的商品创建成功（符合预期）")
            else:
                print("❌ 不同价格的商品应该创建成功，但失败了")
                print(f"   错误信息: {create_response2.text}")
        else:
            print("没有商品可以测试")
    else:
        print(f"获取商品列表失败: {response.status_code}")

if __name__ == "__main__":
    test_duplicate_product_check() 