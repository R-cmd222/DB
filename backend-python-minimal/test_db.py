from models import SessionLocal, Product, Employee, Guest, Bill, BillItem
from sqlalchemy.exc import SQLAlchemyError

def test_database_connection():
    try:
        # 创建数据库会话
        db = SessionLocal()
        
        # 测试查询 - 获取所有商品类别
        categories = db.query(Product.Category).distinct().all()
        print("\n=== 商品类别列表 ===")
        for i, category in enumerate(categories):
            print(f"类别ID: {i+1}, 名称: {category[0]}")
        
        # 测试查询 - 获取所有商品
        products = db.query(Product).all()
        print("\n=== 商品列表 ===")
        for product in products:
            print(f"商品ID: {product.ProductID}, 名称: {product.Name}, 价格: {product.Price}, 库存: {product.Stock}, 类别: {product.Category}")
        
        # 测试查询 - 获取所有员工
        employees = db.query(Employee).all()
        print("\n=== 员工列表 ===")
        for employee in employees:
            print(f"员工ID: {employee.EmployeeID}, 姓名: {employee.Name}, 职位: {employee.Position}, 用户名: {employee.username}")
        
        print("\n数据库连接测试成功！")
        
    except SQLAlchemyError as e:
        print(f"\n数据库连接或查询出错：{str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    test_database_connection() 