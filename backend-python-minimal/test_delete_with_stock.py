import requests
import json

# 测试新的删除功能（库存设为0）
def test_delete_with_stock_zero():
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
        
        # 显示商品信息
        for product in products:
            print(f"  ID: {product['ProductID']}, 名称: {product['Name']}, 库存: {product['Stock']}, 类别: {product['Category']}")
        
        if products:
            # 2. 尝试删除第一个商品
            first_product = products[0]
            product_id = first_product['ProductID']
            product_name = first_product['Name']
            original_stock = first_product['Stock']
            
            print(f"\n2. 尝试删除商品 ID: {product_id}, 名称: {product_name}, 当前库存: {original_stock}")
            
            delete_response = requests.delete(f"{base_url}/products/{product_id}", headers=headers)
            print(f"删除响应状态码: {delete_response.status_code}")
            print(f"删除响应内容: {delete_response.text}")
            
            if delete_response.status_code == 200:
                result = delete_response.json()
                print(f"✅ 操作成功！")
                print(f"   操作类型: {result.get('action')}")
                print(f"   消息: {result.get('message')}")
                
                # 3. 验证商品状态
                print(f"\n3. 验证商品状态...")
                verify_response = requests.get(f"{base_url}/products", headers=headers)
                if verify_response.status_code == 200:
                    remaining_products = verify_response.json()
                    # 查找被操作的商品
                    updated_product = None
                    for p in remaining_products:
                        if p['ProductID'] == product_id:
                            updated_product = p
                            break
                    
                    if updated_product:
                        print(f"   商品ID: {updated_product['ProductID']}")
                        print(f"   商品名称: {updated_product['Name']}")
                        print(f"   当前库存: {updated_product['Stock']}")
                        
                        if result.get('action') == 'stock_zero':
                            if updated_product['Stock'] == 0:
                                print("✅ 验证成功：商品库存已设为0")
                            else:
                                print("❌ 验证失败：商品库存未设为0")
                        elif result.get('action') == 'deleted':
                            print("✅ 验证成功：商品已被删除")
                    else:
                        print("✅ 验证成功：商品已被删除（列表中找不到）")
                else:
                    print(f"❌ 验证失败：获取商品列表失败 - {verify_response.status_code}")
            else:
                print("❌ 删除失败！")
        else:
            print("没有商品可以删除")
    else:
        print(f"获取商品列表失败: {response.status_code}")

if __name__ == "__main__":
    test_delete_with_stock_zero() 