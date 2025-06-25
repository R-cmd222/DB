from models import SessionLocal, Product, Bill, BillItem
from sqlalchemy.orm import Session

def debug_orders_and_products():
    db = SessionLocal()
    try:
        print("=== 调试订单和商品关联关系 ===\n")
        
        # 1. 获取所有商品
        products = db.query(Product).all()
        print("1. 所有商品:")
        for p in products:
            print(f"   ProductID: {p.ProductID}, 名称: {p.Name}, 类别: {p.Category}")
        
        # 2. 获取所有订单
        bills = db.query(Bill).all()
        print(f"\n2. 所有订单 (共{len(bills)}个):")
        for bill in bills:
            print(f"   订单ID: {bill.BillID}, 客户: {bill.guest.Name if bill.guest else '散客'}")
            
            # 3. 获取订单项
            items = db.query(BillItem).filter(BillItem.BillID == bill.BillID).all()
            print(f"   订单项:")
            for item in items:
                # 尝试获取对应的商品
                product = db.query(Product).filter(Product.ProductID == item.ProductID).first()
                product_name = product.Name if product else "商品不存在"
                product_category = product.Category if product else "类别不存在"
                
                print(f"     - ProductID: {item.ProductID}, 商品名称: {product_name}, 类别: {product_category}")
                print(f"       数量: {item.Quantity}, 单价: {item.Price}")
            print()
        
        # 4. 检查是否有孤立的订单项（ProductID不存在于商品表中）
        print("3. 检查孤立的订单项:")
        all_product_ids = {p.ProductID for p in products}
        all_bill_items = db.query(BillItem).all()
        
        orphan_items = []
        for item in all_bill_items:
            if item.ProductID not in all_product_ids:
                orphan_items.append(item)
        
        if orphan_items:
            print(f"   发现 {len(orphan_items)} 个孤立的订单项:")
            for item in orphan_items:
                print(f"     - BillItemID: {item.BillItemID}, ProductID: {item.ProductID} (商品不存在)")
        else:
            print("   没有发现孤立的订单项")
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_orders_and_products() 