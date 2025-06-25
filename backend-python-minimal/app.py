from fastapi import FastAPI, HTTPException, Depends, Query, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import logging
import traceback
from models import SessionLocal, Product, Employee, Guest, Bill, BillItem
from sqlalchemy.exc import IntegrityError

# 日志同时输出到控制台和文件
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),  # 控制台
        logging.FileHandler("backend.log", encoding="utf-8")  # 文件
    ]
)
logger = logging.getLogger(__name__)

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic模型
class ProductBase(BaseModel):
    Name: str
    Price: float
    Stock: int
    Category: str
    Unit: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    ProductID: int

    class Config:
        from_attributes = True

# 简单的认证
security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    if token.credentials != "admin123":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": "admin", "role": "admin"}

# 创建FastAPI应用
app = FastAPI(title="超市管理系统", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 基础路由
@app.get("/")
def read_root():
    return {"message": "欢迎使用超市管理系统API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# 商品管理API
@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """获取所有商品"""
    products = db.query(Product).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """根据ID获取商品"""
    product = db.query(Product).filter(Product.ProductID == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

@app.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建新商品"""
    # 检查是否已存在相同名称的商品（不考虑价格）
    existing_product = db.query(Product).filter(
        Product.Name == product.Name
    ).first()
    
    if existing_product:
        # 如果商品名称相同，更新现有商品的信息
        logger.info(f"商品 '{product.Name}' 已存在，更新商品信息")
        
        # 更新商品信息（保留ID，更新其他字段）
        existing_product.Price = product.Price
        existing_product.Stock = product.Stock
        existing_product.Category = product.Category
        existing_product.Unit = product.Unit
        
        db.commit()
        db.refresh(existing_product)
        
        return existing_product
    else:
        # 如果商品名称不存在，创建新商品
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新商品"""
    db_product = db.query(Product).filter(Product.ProductID == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除商品"""
    db_product = db.query(Product).filter(Product.ProductID == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")

    # 检查商品是否被订单引用
    bill_items_count = db.query(BillItem).filter(BillItem.ProductID == product_id).count()
    
    if bill_items_count > 0:
        # 商品被订单引用，将库存设为0而不是删除
        db_product.Stock = 0
        db.commit()
        return {
            "message": f"商品 '{db_product.Name}' 已被 {bill_items_count} 个订单引用，已将库存设为0以保留订单历史。",
            "action": "stock_zero",
            "referenced_count": bill_items_count
        }
    else:
        # 商品未被引用，可以安全删除
        try:
            db.delete(db_product)
            db.commit()
            return {
                "message": f"商品 '{db_product.Name}' 删除成功",
                "action": "deleted"
            }
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="删除商品时发生错误，请稍后重试。"
            )

# 获取所有商品类别
@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """获取所有商品类别"""
    categories = db.query(Product.Category).distinct().all()
    return [{"CategoryID": i+1, "Name": cat[0]} for i, cat in enumerate(categories)]

# 统计API
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """获取基础统计信息"""
    total_products = db.query(Product).count()
    total_orders = db.query(Bill).count()
    total_stock = db.query(Product).with_entities(func.sum(Product.Stock)).scalar() or 0
    low_stock_products = db.query(Product).filter(Product.Stock < 10).count()
    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_stock": total_stock,
        "low_stock_products": low_stock_products
    }

# 订单相关模型
class BillItemBase(BaseModel):
    ProductID: int
    Quantity: int
    Price: float

    class Config:
        from_attributes = True

class BillItemResponse(BillItemBase):
    BillItemID: int
    BillID: int
    product_name: Optional[str] = None
    product_category: Optional[str] = None

    class Config:
        from_attributes = True

class BillBase(BaseModel):
    GuestID: Optional[int] = None
    EmployeeID: int
    TotalAmount: float
    PaymentMethod: str = '现金'
    Status: Optional[str] = '已完成'

    class Config:
        from_attributes = True

class BillCreate(BillBase):
    items: List[BillItemBase]

class BillResponse(BillBase):
    BillID: int
    BillDate: datetime
    items: List[BillItemResponse]
    guest_name: Optional[str] = None
    employee_name: Optional[str] = None

    class Config:
        from_attributes = True

# 订单管理API
@app.get("/bills", response_model=List[BillResponse])
def get_bills(db: Session = Depends(get_db)):
    """获取所有订单"""
    try:
        logger.info("正在获取订单列表...")
        bills = db.query(Bill).order_by(Bill.BillDate.desc()).all()
        logger.info(f"成功获取到 {len(bills)} 个订单")
        result = []
        for bill in bills:
            # 为每个订单项添加商品信息
            items_with_product_info = []
            for item in bill.items:
                # 获取商品信息
                product = db.query(Product).filter(Product.ProductID == item.ProductID).first()
                item_data = {
                    "BillItemID": item.BillItemID,
                    "BillID": item.BillID,
                    "ProductID": item.ProductID,
                    "Quantity": item.Quantity,
                    "Price": float(item.Price),
                    "product_name": product.Name if product else "未知商品",
                    "product_category": product.Category if product else "未知类别"
                }
                items_with_product_info.append(item_data)
            
            result.append({
                "BillID": bill.BillID,
                "GuestID": bill.GuestID,
                "EmployeeID": bill.EmployeeID,
                "TotalAmount": float(bill.TotalAmount),
                "PaymentMethod": bill.PaymentMethod,
                "Status": bill.Status,
                "BillDate": bill.BillDate,
                "guest_name": bill.guest.Name if bill.guest else "散客",
                "employee_name": bill.employee.Name if bill.employee else "",
                "items": items_with_product_info
            })
        return result
    except Exception as e:
        logger.error(f"获取订单列表时出错: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取订单列表时出错: {str(e)}")

@app.get("/bills/{bill_id}", response_model=BillResponse)
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    """根据ID获取订单"""
    try:
        logger.info(f"正在获取订单 {bill_id}...")
        bill = db.query(Bill).filter(Bill.BillID == bill_id).first()
        if not bill:
            logger.warning(f"订单 {bill_id} 不存在")
            raise HTTPException(status_code=404, detail="订单不存在")
        logger.info(f"成功获取订单 {bill_id}")
        
        # 为订单项添加商品信息
        items_with_product_info = []
        for item in bill.items:
            # 获取商品信息
            product = db.query(Product).filter(Product.ProductID == item.ProductID).first()
            item_data = {
                "BillItemID": item.BillItemID,
                "BillID": item.BillID,
                "ProductID": item.ProductID,
                "Quantity": item.Quantity,
                "Price": float(item.Price),
                "product_name": product.Name if product else "未知商品",
                "product_category": product.Category if product else "未知类别"
            }
            items_with_product_info.append(item_data)
        
        return {
            "BillID": bill.BillID,
            "GuestID": bill.GuestID,
            "EmployeeID": bill.EmployeeID,
            "TotalAmount": float(bill.TotalAmount),
            "PaymentMethod": bill.PaymentMethod,
            "Status": bill.Status,
            "BillDate": bill.BillDate,
            "guest_name": bill.guest.Name if bill.guest else "散客",
            "employee_name": bill.employee.Name if bill.employee else "",
            "items": items_with_product_info
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取订单 {bill_id} 时出错: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取订单时出错: {str(e)}")

@app.post("/bills", response_model=BillResponse)
def create_bill(
    bill: BillCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建新订单"""
    try:
        logger.info("正在创建新订单...")
        
        # 处理客户信息
        guest_id = bill.GuestID
        if not guest_id:
            # 如果没有提供客户ID，需要创建或查找客户
            # 这里假设前端会传递客户信息，我们需要创建一个新的客户处理逻辑
            # 暂时使用默认客户ID为1
            guest_id = 1
            logger.info(f"使用默认客户ID: {guest_id}")
        
        # 验证库存
        for item in bill.items:
            product = db.query(Product).filter(Product.ProductID == item.ProductID).first()
            if not product:
                raise HTTPException(status_code=400, detail=f"商品ID {item.ProductID} 不存在")
            if (product.Stock or 0) < item.Quantity:
                raise HTTPException(status_code=400, detail=f"商品 {product.Name} 库存不足，当前库存: {product.Stock}，需要: {item.Quantity}")
        
        # 创建订单
        db_bill = Bill(
            GuestID=guest_id,
            EmployeeID=current_user.get('id', 1),  # 使用当前登录员工ID
            TotalAmount=bill.TotalAmount,
            PaymentMethod=bill.PaymentMethod,
            Status=bill.Status,
            BillDate=datetime.now()
        )
        db.add(db_bill)
        db.flush()  # 获取BillID但不提交事务
        
        logger.info(f"订单 {db_bill.BillID} 创建成功，正在添加订单项...")
        
        # 创建订单项并更新库存
        for item in bill.items:
            # 创建订单项
            db_item = BillItem(
                BillID=db_bill.BillID,
                ProductID=item.ProductID,
                Quantity=item.Quantity,
                Price=item.Price
            )
            db.add(db_item)
            
            # 更新库存
            product = db.query(Product).filter(Product.ProductID == item.ProductID).first()
            product.Stock = (product.Stock or 0) - item.Quantity
            logger.info(f"商品 {product.Name} 库存从 {product.Stock + item.Quantity} 更新为 {product.Stock}")
        
        # 提交所有更改
        db.commit()
        db.refresh(db_bill)
        
        logger.info(f"订单 {db_bill.BillID} 及其订单项创建完成，库存已更新")
        
        # 返回完整的订单信息
        return get_bill(db_bill.BillID, db)
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"创建订单时出错: {str(e)}")
        logger.error(traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建订单时出错: {str(e)}")

@app.get("/dashboard/sales")
def get_dashboard_sales(db: Session = Depends(get_db)):
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = datetime(now.year, now.month, 1)

    # 今日销售额
    today_sales = db.query(func.sum(Bill.TotalAmount)).filter(
        Bill.BillDate >= today_start,
        (Bill.Status == '已结账')
    ).scalar() or 0

    # 本周销售额
    week_sales = db.query(func.sum(Bill.TotalAmount)).filter(
        Bill.BillDate >= week_start,
        (Bill.Status == '已结账')
    ).scalar() or 0

    # 上周销售额
    last_week_start = week_start - timedelta(days=7)
    last_week_end = week_start - timedelta(seconds=1)
    last_week_sales = db.query(func.sum(Bill.TotalAmount)).filter(
        Bill.BillDate >= last_week_start,
        Bill.BillDate <= last_week_end,
        (Bill.Status == '已结账')
    ).scalar() or 0

    # 本月销售额
    month_sales = db.query(func.sum(Bill.TotalAmount)).filter(
        Bill.BillDate >= month_start,
        (Bill.Status == '已结账')
    ).scalar() or 0

    return {
        "today_sales": float(today_sales),
        "week_sales": float(week_sales),
        "last_week_sales": float(last_week_sales),
        "month_sales": float(month_sales)
    }

@app.get("/dashboard/top-products")
def get_top_products(db: Session = Depends(get_db), limit: int = 5):
    result = db.query(
        Product.Name,
        func.sum(BillItem.Quantity).label('sales')
    ).join(BillItem, BillItem.ProductID == Product.ProductID
    ).join(Bill, Bill.BillID == BillItem.BillID
    ).filter((Bill.Status == '已结账')
    ).group_by(Product.Name
    ).order_by(func.sum(BillItem.Quantity).desc()
    ).limit(limit).all()

    return [{"name": r[0], "sales": int(r[1])} for r in result]

@app.get("/report/sales")
def report_sales(
    db: Session = Depends(get_db),
    start: str = Query(...),
    end: str = Query(...),
    unit: str = Query("day")
):
    from datetime import datetime, timedelta
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
    
    # 获取订单数据
    orders = db.query(Bill).filter(
        Bill.BillDate >= start_date,
        Bill.BillDate <= end_date,
        (Bill.Status == '已结账')
    ).all()
    
    total_sales = sum(float(o.TotalAmount) for o in orders)
    order_count = len(orders)
    avg_order_value = total_sales / order_count if order_count else 0
    guest_ids = set(o.GuestID for o in orders if o.GuestID is not None)
    new_customers = len(guest_ids)
    
    # 生成趋势数据
    trend = []
    if unit == "day":
        delta = timedelta(days=1)
        fmt = "%Y-%m-%d"
        current = start_date
        while current <= end_date:
            day_end = current + timedelta(days=1) - timedelta(seconds=1)
            day_orders = [o for o in orders if current <= o.BillDate <= day_end]
            day_sales = sum(float(o.TotalAmount) for o in day_orders)
            day_count = len(day_orders)
            trend.append({
                "date": current.strftime(fmt),
                "sales": float(day_sales),
                "orders": day_count
            })
            current += delta
    elif unit == "week":
        delta = timedelta(weeks=1)
        fmt = "%Y-W%W"
        current = start_date
        while current <= end_date:
            week_end = current + timedelta(weeks=1) - timedelta(seconds=1)
            week_orders = [o for o in orders if current <= o.BillDate <= week_end]
            week_sales = sum(float(o.TotalAmount) for o in week_orders)
            week_count = len(week_orders)
            trend.append({
                "date": current.strftime(fmt),
                "sales": float(week_sales),
                "orders": week_count
            })
            current += delta
    else:  # month
        current = start_date
        while current <= end_date:
            if current.month == 12:
                next_month = datetime(current.year + 1, 1, 1)
            else:
                next_month = datetime(current.year, current.month + 1, 1)
            month_end = next_month - timedelta(seconds=1)
            month_orders = [o for o in orders if current <= o.BillDate <= month_end]
            month_sales = sum(float(o.TotalAmount) for o in month_orders)
            month_count = len(month_orders)
            trend.append({
                "date": current.strftime("%Y-%m"),
                "sales": float(month_sales),
                "orders": month_count
            })
            current = next_month
    
    # 计算增长率（与上一个周期比较）
    sales_growth = 0
    order_growth = 0
    avg_order_growth = 0
    customer_growth = 0
    
    if len(trend) >= 2:
        current_period = trend[-1]
        previous_period = trend[-2]
        
        if previous_period["sales"] > 0:
            sales_growth = ((current_period["sales"] - previous_period["sales"]) / previous_period["sales"]) * 100
        if previous_period["orders"] > 0:
            order_growth = ((current_period["orders"] - previous_period["orders"]) / previous_period["orders"]) * 100
        if previous_period["orders"] > 0 and current_period["orders"] > 0:
            current_avg = current_period["sales"] / current_period["orders"]
            previous_avg = previous_period["sales"] / previous_period["orders"]
            if previous_avg > 0:
                avg_order_growth = ((current_avg - previous_avg) / previous_avg) * 100
    
    # TOP商品
    top_products = db.query(
        Product.Name,
        func.sum(BillItem.Quantity).label('sales'),
        func.sum(BillItem.Price * BillItem.Quantity).label('revenue')
    ).join(BillItem, BillItem.ProductID == Product.ProductID
    ).join(Bill, Bill.BillID == BillItem.BillID
    ).filter(
        Bill.BillDate >= start_date,
        Bill.BillDate <= end_date,
        (Bill.Status == '已结账')
    ).group_by(Product.Name
    ).order_by(func.sum(BillItem.Quantity).desc()
    ).limit(10).all()
    
    # 计算商品占比
    total_revenue = sum(float(r[2]) for r in top_products)
    top_products_with_percentage = []
    for i, r in enumerate(top_products):
        percentage = (float(r[2]) / total_revenue * 100) if total_revenue > 0 else 0
        top_products_with_percentage.append({
            "rank": i+1, 
            "name": r[0], 
            "sales": int(r[1]), 
            "revenue": float(r[2]), 
            "percentage": percentage
        })
    
    return {
        "totalSales": total_sales,
        "orderCount": order_count,
        "avgOrderValue": avg_order_value,
        "newCustomers": new_customers,
        "salesGrowth": sales_growth,
        "orderGrowth": order_growth,
        "avgOrderGrowth": avg_order_growth,
        "customerGrowth": customer_growth,
        "trend": trend,
        "topProducts": top_products_with_percentage
    }

@app.get("/report/inventory")
def report_inventory(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    total_value = sum(float(p.Price) * (p.Stock or 0) for p in products)
    product_count = len(products)
    low_stock = [
        {"name": p.Name, "currentStock": p.Stock, "minStock": 10, "status": "critical" if (p.Stock or 0) <= 0 else "warning"}
        for p in products if (p.Stock or 0) < 10
    ]
    low_stock_count = len(low_stock)
    # 周转率、分布等可根据实际需求扩展
    return {
        "totalValue": total_value,
        "productCount": product_count,
        "lowStockCount": low_stock_count,
        "turnoverRate": 0,
        "lowStockProducts": low_stock
    }

@app.get("/report/customer")
def report_customer(db: Session = Depends(get_db), start: str = Query(None), end: str = Query(None)):
    from datetime import datetime
    guests = db.query(Guest).all()
    total_customers = len(guests)
    
    # 统计各等级客户数量
    vip_customers = db.query(Guest).filter(Guest.Level == 'vip').count()
    diamond_customers = db.query(Guest).filter(Guest.Level == 'diamond').count()
    normal_customers = db.query(Guest).filter(Guest.Level == 'normal').count()
    
    # 新增客户
    new_customers = 0
    if start and end:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        new_customers = db.query(Guest).filter(Guest.bills.any(Bill.BillDate >= start_date), Guest.bills.any(Bill.BillDate <= end_date)).count()
    
    # 活跃客户（有订单的客户）
    active_customers = db.query(Guest).filter(Guest.bills.any()).count()
    
    # 客户消费排行TOP 10
    top_customers = db.query(
        Guest.Name,
        Guest.Level,
        func.sum(Bill.TotalAmount).label('total_spent'),
        func.count(Bill.BillID).label('order_count'),
        func.max(Bill.BillDate).label('last_order_date')
    ).join(Bill, Bill.GuestID == Guest.GuestID
    ).filter(Bill.Status == '已结账'
    ).group_by(Guest.GuestID, Guest.Name, Guest.Level
    ).order_by(func.sum(Bill.TotalAmount).desc()
    ).limit(10).all()
    
    top_customers_data = []
    for i, customer in enumerate(top_customers):
        top_customers_data.append({
            "rank": i + 1,
            "name": customer[0],
            "level": customer[1] or 'normal',
            "totalSpent": float(customer[2]),
            "orderCount": int(customer[3]),
            "lastOrderDate": customer[4].isoformat() if customer[4] else None
        })
    
    return {
        "totalCustomers": total_customers,
        "newCustomers": new_customers,
        "activeCustomers": active_customers,
        "normalCustomers": normal_customers,
        "vipCustomers": vip_customers,
        "diamondCustomers": diamond_customers,
        "satisfaction": 100.0,
        "topCustomers": top_customers_data
    }

@app.get("/report/product")
def report_product(db: Session = Depends(get_db), start: str = Query(None), end: str = Query(None)):
    from datetime import datetime
    products = db.query(Product).all()
    total_products = len(products)
    active_products = total_products
    avg_price = sum(float(p.Price) for p in products) / total_products if total_products else 0
    # 类别数
    category_count = len(set(p.Category for p in products))
    
    # 价格分布统计
    price_ranges = [
        {'range': '0-10元', 'min': 0, 'max': 10, 'count': 0},
        {'range': '10-20元', 'min': 10, 'max': 20, 'count': 0},
        {'range': '20-50元', 'min': 20, 'max': 50, 'count': 0},
        {'range': '50-100元', 'min': 50, 'max': 100, 'count': 0},
        {'range': '100元以上', 'min': 100, 'max': float('inf'), 'count': 0}
    ]
    
    for product in products:
        price = float(product.Price)
        for range_info in price_ranges:
            if range_info['min'] <= price < range_info['max']:
                range_info['count'] += 1
                break
    
    # 按商品类别统计销量排行
    category_sales = db.query(
        Product.Category,
        func.sum(BillItem.Quantity).label('sales'),
        func.sum(BillItem.Price * BillItem.Quantity).label('revenue')
    ).join(BillItem, BillItem.ProductID == Product.ProductID
    ).join(Bill, Bill.BillID == BillItem.BillID
    ).filter((Bill.Status == '已结账')
    ).group_by(Product.Category
    ).order_by(func.sum(BillItem.Quantity).desc()
    ).all()
    
    # 商品销量排行（保留原来的功能）
    top_products = db.query(
        Product.Name,
        func.sum(BillItem.Quantity).label('sales')
    ).join(BillItem, BillItem.ProductID == Product.ProductID
    ).join(Bill, Bill.BillID == BillItem.BillID
    ).filter((Bill.Status == '已结账')
    ).group_by(Product.Name
    ).order_by(func.sum(BillItem.Quantity).desc()
    ).limit(10).all()
    
    return {
        "totalProducts": total_products,
        "activeProducts": active_products,
        "avgPrice": avg_price,
        "categoryCount": category_count,
        "topProducts": [
            {"name": r[0], "sales": int(r[1])} for r in top_products
        ],
        "categorySales": [
            {"name": r[0], "sales": int(r[1]), "revenue": float(r[2])} for r in category_sales
        ],
        "priceRanges": [
            {"range": r['range'], "count": r['count']} for r in price_ranges
        ]
    }

# 客户管理API
class GuestCreate(BaseModel):
    Name: str
    Level: Optional[str] = 'normal'  # normal, vip, diamond
    Points: Optional[int] = 0
    Phone: Optional[str] = None

class GuestUpdate(BaseModel):
    Name: Optional[str] = None
    Level: Optional[str] = None  # normal, vip, diamond
    Points: Optional[int] = None
    Phone: Optional[str] = None

class GuestResponse(BaseModel):
    id: int
    name: str
    level: str  # normal, vip, diamond
    points: int
    orderCount: int
    lastOrderDate: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True

@app.get("/guests", response_model=List[GuestResponse])
def get_guests(db: Session = Depends(get_db)):
    """获取所有客户详细信息"""
    guests = db.query(Guest).all()
    result = []
    for g in guests:
        bills = list(getattr(g, 'bills', []))
        order_count = len(bills)
        last_order_date = None
        if bills:
            bill_dates = [b.BillDate for b in bills if hasattr(b, 'BillDate') and b.BillDate]
            if bill_dates:
                last_order_date = max(bill_dates)
        result.append({
            "id": g.GuestID,
            "name": g.Name,
            "level": getattr(g, 'Level', 'normal'),
            "points": getattr(g, 'Points', 0),
            "orderCount": order_count,
            "lastOrderDate": last_order_date.isoformat() if last_order_date else None,
            "phone": getattr(g, 'Phone', None)
        })
    return result

@app.post("/guests", response_model=GuestResponse)
def create_guest(
    guest: GuestCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建新客户"""
    # 检查是否已存在相同姓名和电话号码的客户
    existing_guest = None
    if guest.Phone:
        # 如果有电话号码，检查姓名+电话号码的组合
        existing_guest = db.query(Guest).filter(
            Guest.Name == guest.Name,
            Guest.Phone == guest.Phone
        ).first()
    else:
        # 如果没有电话号码，只检查姓名
        existing_guest = db.query(Guest).filter(
            Guest.Name == guest.Name,
            Guest.Phone.is_(None)
        ).first()
    
    if existing_guest:
        if guest.Phone:
            raise HTTPException(
                status_code=400,
                detail=f"客户 '{guest.Name}' (电话: {guest.Phone}) 已存在"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"客户 '{guest.Name}' 已存在"
            )
    
    db_guest = Guest(
        Name=guest.Name,
        Level=guest.Level,
        Points=guest.Points or 0,
        Phone=guest.Phone  # 添加电话号码
    )
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    
    return {
        "id": db_guest.GuestID,
        "name": db_guest.Name,
        "level": db_guest.Level,
        "points": db_guest.Points,
        "orderCount": 0,
        "lastOrderDate": None,
        "phone": db_guest.Phone
    }

@app.put("/guests/{guest_id}", response_model=GuestResponse)
def update_guest(
    guest_id: int,
    guest: GuestUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新客户信息"""
    try:
        db_guest = db.query(Guest).filter(Guest.GuestID == guest_id).first()
        if not db_guest:
            raise HTTPException(status_code=404, detail="客户不存在")
        
        # 更新字段
        if guest.Name is not None:
            db_guest.Name = guest.Name
        if guest.Phone is not None:
            db_guest.Phone = guest.Phone
        
        # 处理积分和等级更新
        points_updated = False
        if guest.Points is not None:
            old_points = db_guest.Points or 0
            db_guest.Points = guest.Points
            points_updated = True
            logger.info(f"客户 {db_guest.Name} 积分更新: {old_points} -> {guest.Points}")
        
        # 如果手动设置了等级，使用手动设置的等级
        if guest.Level is not None:
            db_guest.Level = guest.Level
            logger.info(f"客户 {db_guest.Name} 等级手动设置为: {guest.Level}")
        elif points_updated:
            # 如果积分更新了但没有手动设置等级，根据积分自动更新等级
            old_level = db_guest.Level
            if db_guest.Points >= 5000:
                db_guest.Level = 'diamond'
            elif db_guest.Points >= 2000:
                db_guest.Level = 'vip'
            else:
                db_guest.Level = 'normal'
            
            if old_level != db_guest.Level:
                logger.info(f"客户 {db_guest.Name} 等级自动更新: {old_level} -> {db_guest.Level}")
        
        db.commit()
        db.refresh(db_guest)
        
        # 简化订单统计计算，使用数据库查询而不是加载所有关联对象
        order_count = db.query(Bill).filter(Bill.GuestID == guest_id).count()
        
        # 获取最后订单日期
        last_order = db.query(Bill).filter(
            Bill.GuestID == guest_id
        ).order_by(Bill.BillDate.desc()).first()
        
        last_order_date = last_order.BillDate if last_order else None
        
        return {
            "id": db_guest.GuestID,
            "name": db_guest.Name,
            "level": db_guest.Level,
            "points": db_guest.Points,
            "orderCount": order_count,
            "lastOrderDate": last_order_date.isoformat() if last_order_date else None,
            "phone": db_guest.Phone
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新客户失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="更新客户时发生错误，请稍后重试")

@app.delete("/guests/{guest_id}")
def delete_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除客户"""
    db_guest = db.query(Guest).filter(Guest.GuestID == guest_id).first()
    if not db_guest:
        raise HTTPException(status_code=404, detail="客户不存在")
    
    # 检查客户是否有关联订单
    bills_count = db.query(Bill).filter(Bill.GuestID == guest_id).count()
    
    if bills_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"客户 '{db_guest.Name}' 有 {bills_count} 个关联订单，无法删除。请先删除相关订单。"
        )
    
    try:
        db.delete(db_guest)
        db.commit()
        return {
            "message": f"客户 '{db_guest.Name}' 删除成功",
            "action": "deleted"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="删除客户时发生错误，请稍后重试。"
        )

class ChangePasswordRequest(BaseModel):
    id: int
    newPwd: str

@app.post("/change_password")
def change_password(data: ChangePasswordRequest, db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.EmployeeID == data.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="员工不存在")
    user.password = data.newPwd
    db.commit()
    return {"message": "密码修改成功"}

@app.post("/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    username = data.get("username")
    password = data.get("password")
    user = db.query(Employee).filter(Employee.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {
        "token": "admin123",
        "employee": {
            "id": user.EmployeeID,
            "name": user.Name,
            "role": getattr(user, 'role', ''),
            "position": user.Position
        }
    }

# 收银台结算API
class CashierCheckoutRequest(BaseModel):
    customer_name: str
    customer_phone: str
    items: List[BillItemBase]
    total_amount: float
    payment_method: str = '现金'
    discount: float = 0
    employee_id: Optional[int] = None  # 新增

@app.post("/cashier/checkout", response_model=BillResponse)
def cashier_checkout(
    checkout_data: CashierCheckoutRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """收银台结算"""
    try:
        logger.info(f"收到结算请求: {checkout_data.dict()}")
        
        # 1. 处理客户信息 - 查找或创建客户
        guest = db.query(Guest).filter(
            Guest.Name == checkout_data.customer_name,
            Guest.Phone == checkout_data.customer_phone
        ).first()
        
        if not guest:
            # 创建新客户
            guest = Guest(
                Name=checkout_data.customer_name,
                Phone=checkout_data.customer_phone,
                Level='normal',
                Points=0
            )
            db.add(guest)
            db.flush()  # 获取GuestID
            logger.info(f"创建新客户: {guest.Name} (ID: {guest.GuestID})")
        else:
            logger.info(f"找到现有客户: {guest.Name} (ID: {guest.GuestID})")
        
        # 2. 验证库存
        for item in checkout_data.items:
            product = db.query(Product).filter(Product.ProductID == item.ProductID).first()
            if not product:
                raise HTTPException(status_code=400, detail=f"商品ID {item.ProductID} 不存在")
            if (product.Stock or 0) < item.Quantity:
                raise HTTPException(status_code=400, detail=f"商品 {product.Name} 库存不足，当前库存: {product.Stock}，需要: {item.Quantity}")
        
        # 3. 获取员工ID
        employee_id = getattr(checkout_data, 'employee_id', None)
        emp = db.query(Employee).filter(Employee.EmployeeID == employee_id).first()
        if not emp:
            logger.error(f"结算失败：找不到员工ID {employee_id}")
            raise HTTPException(status_code=400, detail=f"找不到员工ID {employee_id}，请重新登录")
        logger.info(f"收银台结算 employee_id={employee_id}, employee_name={emp.Name}")
        
        # 4. 创建订单
        db_bill = Bill(
            GuestID=guest.GuestID,
            EmployeeID=employee_id,
            TotalAmount=checkout_data.total_amount,
            PaymentMethod=checkout_data.payment_method,
            Status='已结账',
            BillDate=datetime.now()
        )
        db.add(db_bill)
        db.flush()  # 获取BillID
        
        logger.info(f"创建订单: {db_bill.BillID}")
        
        # 4. 创建订单项并更新库存
        total_points = 0
        for item in checkout_data.items:
            # 创建订单项
            db_item = BillItem(
                BillID=db_bill.BillID,
                ProductID=item.ProductID,
                Quantity=item.Quantity,
                Price=item.Price
            )
            db.add(db_item)
            
            # 更新库存
            product = db.query(Product).filter(Product.ProductID == item.ProductID).first()
            old_stock = product.Stock or 0
            product.Stock = old_stock - item.Quantity
            logger.info(f"商品 {product.Name} 库存: {old_stock} -> {product.Stock}")
        
        # 5. 计算积分（支付金额的10倍）
        total_points = int(checkout_data.total_amount * 10)
        
        # 6. 更新客户积分
        old_points = guest.Points or 0
        guest.Points = old_points + total_points
        
        # 7. 根据积分更新客户等级
        old_level = guest.Level
        if guest.Points >= 5000:  # 5000积分 = 500元消费 = 钻石客户
            guest.Level = 'diamond'
        elif guest.Points >= 2000:  # 2000积分 = 200元消费 = VIP客户
            guest.Level = 'vip'
        else:  # 2000积分以下 = 普通客户
            guest.Level = 'normal'
        
        logger.info(f"客户 {guest.Name} 积分: {old_points} -> {guest.Points} (+{total_points})")
        logger.info(f"客户等级: {old_level} -> {guest.Level}")
        
        # 8. 提交所有更改
        db.commit()
        db.refresh(db_bill)
        
        logger.info(f"收银台结算完成，订单ID: {db_bill.BillID}")
        
        # 9. 返回完整的订单信息
        return get_bill(db_bill.BillID, db)
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"收银台结算失败: {str(e)}")
        logger.error(traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail=f"收银台结算失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9527) 