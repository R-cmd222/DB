import requests
import json

def cleanup_duplicate_products():
    """清理重复的商品，保留ID最小的那个"""
    base_url = "http://localhost:9527"
    headers = {
        'Authorization': 'Bearer admin123',
        'Content-Type': 'application/json'
    }
    
    # 1. 获取所有商品
    print("1. 获取所有商品...")
    response = requests.get(f"{base_url}/products", headers=headers)
    if response.status_code != 200:
        print(f"获取商品失败: {response.status_code}")
        return
    
    products = response.json()
    print(f"找到 {len(products)} 个商品")
    
    # 2. 按名称分组，找出重复的商品
    product_groups = {}
    for product in products:
        name = product['Name']
        if name not in product_groups:
            product_groups[name] = []
        product_groups[name].append(product)
    
    # 3. 找出有重复的商品
    duplicates = {name: products for name, products in product_groups.items() if len(products) > 1}
    
    if not duplicates:
        print("✅ 没有发现重复的商品")
        return
    
    print(f"\n2. 发现 {len(duplicates)} 个重复商品组:")
    for name, products in duplicates.items():
        print(f"   '{name}': {len(products)} 个商品")
        for p in sorted(products, key=lambda x: x['ProductID']):
            print(f"     ID: {p['ProductID']}, 价格: ¥{p['Price']}, 库存: {p['Stock']}")
    
    # 4. 删除重复商品（保留ID最小的）
    print(f"\n3. 开始清理重复商品...")
    deleted_count = 0
    
    for name, products in duplicates.items():
        # 按ID排序，保留最小的ID
        sorted_products = sorted(products, key=lambda x: x['ProductID'])
        keep_product = sorted_products[0]  # 保留ID最小的
        delete_products = sorted_products[1:]  # 删除其他的
        
        print(f"\n   处理商品 '{name}':")
        print(f"     保留: ID {keep_product['ProductID']} (价格: ¥{keep_product['Price']}, 库存: {keep_product['Stock']})")
        
        for product in delete_products:
            print(f"     删除: ID {product['ProductID']} (价格: ¥{product['Price']}, 库存: {product['Stock']})")
            
            # 检查商品是否被订单引用
            delete_response = requests.delete(f"{base_url}/products/{product['ProductID']}", headers=headers)
            
            if delete_response.status_code == 200:
                result = delete_response.json()
                if result.get('action') == 'deleted':
                    print(f"       ✅ 成功删除")
                    deleted_count += 1
                elif result.get('action') == 'stock_zero':
                    print(f"       ⚠️  商品被订单引用，库存已设为0")
                    deleted_count += 1
                else:
                    print(f"       ❓ 未知操作: {result}")
            else:
                print(f"       ❌ 删除失败: {delete_response.status_code} - {delete_response.text}")
    
    # 5. 验证清理结果
    print(f"\n4. 验证清理结果...")
    verify_response = requests.get(f"{base_url}/products", headers=headers)
    if verify_response.status_code == 200:
        final_products = verify_response.json()
        print(f"清理后商品总数: {len(final_products)}")
        
        # 再次检查重复
        final_groups = {}
        for product in final_products:
            name = product['Name']
            if name not in final_groups:
                final_groups[name] = []
            final_groups[name].append(product)
        
        final_duplicates = {name: products for name, products in final_groups.items() if len(products) > 1}
        
        if not final_duplicates:
            print("✅ 清理完成！没有重复商品")
        else:
            print("❌ 仍有重复商品:")
            for name, products in final_duplicates.items():
                print(f"   '{name}': {len(products)} 个商品")
    else:
        print(f"❌ 验证失败: {verify_response.status_code}")

if __name__ == "__main__":
    cleanup_duplicate_products() 