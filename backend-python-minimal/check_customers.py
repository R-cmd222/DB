import requests

def check_customers():
    """检查现有客户数据"""
    base_url = "http://localhost:9527"
    headers = {
        'Authorization': 'Bearer admin123',
        'Content-Type': 'application/json'
    }
    
    print("=== 现有客户数据 ===\n")
    
    response = requests.get(f"{base_url}/guests", headers=headers)
    if response.status_code == 200:
        customers = response.json()
        print(f"共 {len(customers)} 个客户:")
        for customer in customers:
            print(f"  ID: {customer['id']}, 姓名: {customer['name']}, 电话: {customer['phone'] or '无'}, 积分: {customer['points']}")
    else:
        print(f"获取客户失败: {response.status_code}")

if __name__ == "__main__":
    check_customers() 