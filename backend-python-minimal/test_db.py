from models import SessionLocal, Category, Product, Employee, Guest, Bill, BillItem
from sqlalchemy.exc import SQLAlchemyError

def test_database_connection():
    try:
        # 创建数据库会话
        db = SessionLocal()
        
        # 测试查询 - 获取所有类别
        categories = db.query(Category).all()
        print("\n=== 类别列表 ===")
        for category in categories:
            print(f"类别ID: {category.CategoryID}, 名称: {category.Name}")
        
        # 测试查询 - 获取所有商品
        products = db.query(Product).all()
        print("\n=== 商品列表 ===")
        for product in products:
            print(f"商品ID: {product.ProductID}, 名称: {product.Name}, 价格: {product.Price}, 库存: {product.Stock}")
        
        # 测试查询 - 获取所有员工
        employees = db.query(Employee).all()
        print("\n=== 员工列表 ===")
        for employee in employees:
            print(f"员工ID: {employee.EmployeeID}, 姓名: {employee.Name}, 职位: {employee.Position}")
        
        print("\n数据库连接测试成功！")
        
    except SQLAlchemyError as e:
        print(f"\n数据库连接或查询出错：{str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    test_database_connection() 