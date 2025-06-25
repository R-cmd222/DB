import requests
import json

# 测试订单API是否返回商品名称
def test_orders_with_product_info():
    base_url = "http://localhost:9527"
    headers = {
        'Authorization': 'Bearer admin123',
        'Content-Type': 'application/json'
    }
    
    # 获取所有订单
    print("1. 获取所有订单...")
    response = requests.get(f"{base_url}/bills", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        print(f"找到 {len(orders)} 个订单")
        
        if orders:
            # 显示第一个订单的详细信息
            first_order = orders[0]
            print(f"\n2. 第一个订单详情:")
            print(f"   订单ID: {first_order['BillID']}")
            print(f"   客户: {first_order['guest_name']}")
            print(f"   员工: {first_order['employee_name']}")
            print(f"   总价: ¥{first_order['TotalAmount']}")
            print(f"   状态: {first_order['Status']}")
            
            # 显示订单项的商品信息
            items = first_order.get('items', [])
            print(f"\n3. 订单项商品信息:")
            for i, item in enumerate(items, 1):
                print(f"   {i}. 商品名称: {item.get('product_name', 'N/A')}")
                print(f"      商品类别: {item.get('product_category', 'N/A')}")
                print(f"      数量: {item['Quantity']}")
                print(f"      单价: ¥{item['Price']}")
                print(f"      小计: ¥{item['Price'] * item['Quantity']}")
                print()
            
            if items:
                print("✅ 订单API成功返回商品名称信息！")
            else:
                print("⚠️  该订单没有商品项")
        else:
            print("没有找到订单")
    else:
        print(f"获取订单失败: {response.status_code}")
        print(f"错误信息: {response.text}")

if __name__ == "__main__":
    test_orders_with_product_info() 