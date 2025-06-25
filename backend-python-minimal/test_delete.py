import requests
import json

# 测试删除商品功能
def test_delete_product():
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
        for product in products:
            print(f"  ID: {product['ProductID']}, 名称: {product['Name']}, 类别: {product['Category']}")
        
        if products:
            # 2. 尝试删除第一个商品
            first_product = products[0]
            product_id = first_product['ProductID']
            print(f"\n2. 尝试删除商品 ID: {product_id}, 名称: {first_product['Name']}")
            
            delete_response = requests.delete(f"{base_url}/products/{product_id}", headers=headers)
            print(f"删除响应状态码: {delete_response.status_code}")
            print(f"删除响应内容: {delete_response.text}")
            
            if delete_response.status_code == 200:
                print("✅ 删除成功！")
                
                # 3. 验证商品已被删除
                print("\n3. 验证商品已被删除...")
                verify_response = requests.get(f"{base_url}/products", headers=headers)
                if verify_response.status_code == 200:
                    remaining_products = verify_response.json()
                    print(f"剩余商品数量: {len(remaining_products)}")
                    if len(remaining_products) == len(products) - 1:
                        print("✅ 验证成功：商品已被正确删除")
                    else:
                        print("❌ 验证失败：商品数量不正确")
                else:
                    print(f"❌ 验证失败：获取商品列表失败 - {verify_response.status_code}")
            else:
                print("❌ 删除失败！")
        else:
            print("没有商品可以删除")
    else:
        print(f"获取商品列表失败: {response.status_code}")

if __name__ == "__main__":
    test_delete_product() 