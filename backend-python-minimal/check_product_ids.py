from models import SessionLocal, Product
from sqlalchemy import text

def check_product_ids():
    db = SessionLocal()
    try:
        print("=== 检查商品ID分布情况 ===\n")
        
        # 获取所有商品，按ID排序
        products = db.query(Product).order_by(Product.ProductID).all()
        
        print(f"总商品数量: {len(products)}")
        print("\n商品ID分布:")
        
        if products:
            min_id = products[0].ProductID
            max_id = products[-1].ProductID
            print(f"最小ID: {min_id}")
            print(f"最大ID: {max_id}")
            print(f"ID范围: {max_id - min_id + 1}")
            
            # 检查缺失的ID
            existing_ids = {p.ProductID for p in products}
            missing_ids = []
            for i in range(min_id, max_id + 1):
                if i not in existing_ids:
                    missing_ids.append(i)
            
            if missing_ids:
                print(f"\n缺失的ID: {missing_ids}")
                print(f"缺失数量: {len(missing_ids)}")
            else:
                print("\n✅ 没有缺失的ID，ID连续")
            
            # 显示所有商品详情
            print(f"\n所有商品详情:")
            for product in products:
                status = "已下架" if product.Stock == 0 else "正常"
                print(f"  ID: {product.ProductID:2d}, 名称: {product.Name:10s}, 库存: {product.Stock:3d}, 状态: {status}")
        
        # 检查是否有被删除但ID被占用的商品
        print(f"\n=== 检查数据库中的实际ID分布 ===")
        result = db.execute(text("SELECT IDENT_CURRENT('Products') as current_id"))
        current_id = result.fetchone()[0]
        print(f"当前自增ID值: {current_id}")
        
        # 检查是否有被软删除的商品（库存为0）
        zero_stock_products = db.query(Product).filter(Product.Stock == 0).all()
        print(f"\n库存为0的商品数量: {len(zero_stock_products)}")
        if zero_stock_products:
            print("库存为0的商品:")
            for p in zero_stock_products:
                print(f"  ID: {p.ProductID}, 名称: {p.Name}")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_product_ids() 