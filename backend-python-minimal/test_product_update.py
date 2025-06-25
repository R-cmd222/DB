import requests
import json

# 测试商品更新功能（相同名称时更新而不是创建新条目）
def test_product_update():
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
            original_id = first_product['ProductID']
            original_price = first_product['Price']
            original_stock = first_product['Stock']
            
            print(f"\n2. 选择测试商品: {first_product['Name']}")
            print(f"   原始ID: {original_id}")
            print(f"   原始价格: ¥{original_price}")
            print(f"   原始库存: {original_stock}")
            
            # 3. 尝试添加相同名称但不同价格的商品
            updated_product = {
                "Name": first_product['Name'],
                "Price": original_price + 5.0,  # 价格加5
                "Stock": original_stock + 100,  # 库存加100
                "Category": first_product['Category'],
                "Unit": "个"
            }
            
            print(f"\n3. 尝试添加相同名称但不同价格的商品...")
            print(f"   商品名称: {updated_product['Name']}")
            print(f"   新价格: ¥{updated_product['Price']}")
            print(f"   新库存: {updated_product['Stock']}")
            
            create_response = requests.post(f"{base_url}/products", 
                                          headers=headers, 
                                          json=updated_product)
            
            print(f"创建响应状态码: {create_response.status_code}")
            
            if create_response.status_code == 200:
                result = create_response.json()
                print(f"✅ 操作成功！")
                print(f"   返回的商品ID: {result['ProductID']}")
                print(f"   返回的商品价格: ¥{result['Price']}")
                print(f"   返回的商品库存: {result['Stock']}")
                
                # 4. 验证商品是否被更新而不是创建新条目
                if result['ProductID'] == original_id:
                    print("✅ 验证成功：商品被更新，ID保持不变")
                else:
                    print("❌ 验证失败：应该更新现有商品，但创建了新商品")
                
                # 5. 验证价格和库存是否被更新
                if result['Price'] == updated_product['Price'] and result['Stock'] == updated_product['Stock']:
                    print("✅ 验证成功：价格和库存已正确更新")
                else:
                    print("❌ 验证失败：价格或库存未正确更新")
                
                # 6. 再次获取商品列表，确认没有重复条目
                print(f"\n4. 验证商品列表...")
                verify_response = requests.get(f"{base_url}/products", headers=headers)
                if verify_response.status_code == 200:
                    updated_products = verify_response.json()
                    print(f"更新后商品总数: {len(updated_products)}")
                    
                    # 查找同名商品
                    same_name_products = [p for p in updated_products if p['Name'] == first_product['Name']]
                    print(f"同名商品数量: {len(same_name_products)}")
                    
                    if len(same_name_products) == 1:
                        print("✅ 验证成功：只有一个同名商品，没有重复条目")
                    else:
                        print("❌ 验证失败：存在多个同名商品")
                        for p in same_name_products:
                            print(f"   ID: {p['ProductID']}, 价格: ¥{p['Price']}, 库存: {p['Stock']}")
                else:
                    print(f"❌ 验证失败：获取商品列表失败 - {verify_response.status_code}")
            else:
                print("❌ 操作失败！")
                print(f"   错误信息: {create_response.text}")
        else:
            print("没有商品可以测试")
    else:
        print(f"获取商品列表失败: {response.status_code}")

if __name__ == "__main__":
    test_product_update() 