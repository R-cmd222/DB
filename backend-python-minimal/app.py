from fastapi import FastAPI, HTTPException, Depends, Query
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
from models import SessionLocal, Category, Product, Employee, Guest, Bill, BillItem

# 配置日志
logging.basicConfig(level=logging.INFO)
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
    CategoryID: int
    Unit: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    ProductID: int

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    Name: str

class CategoryResponse(CategoryBase):
    CategoryID: int

    class Config:
        orm_mode = True

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
    
    db.delete(db_product)
    db.commit()
    return {"message": "商品删除成功"}

# 类别管理API
@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """获取所有类别"""
    categories = db.query(Category).all()
    return categories

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
            result.append({
                **bill.__dict__,
                "guest_name": bill.guest.Name if bill.guest else "散客",
                "employee_name": bill.employee.Name if bill.employee else "",
                "items": bill.items
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
        return {
            **bill.__dict__,
            "guest_name": bill.guest.Name if bill.guest else "散客",
            "employee_name": bill.employee.Name if bill.employee else "",
            "items": bill.items
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
        # 创建订单
        db_bill = Bill(
            GuestID=bill.GuestID,
            EmployeeID=bill.EmployeeID,
            TotalAmount=bill.TotalAmount,
            PaymentMethod=bill.PaymentMethod,
            Status=bill.Status,
            BillDate=datetime.now()
        )
        db.add(db_bill)
        db.commit()
        db.refresh(db_bill)
        
        logger.info(f"订单 {db_bill.BillID} 创建成功，正在添加订单项...")
        # 创建订单项
        for item in bill.items:
            db_item = BillItem(
                BillID=db_bill.BillID,
                ProductID=item.ProductID,
                Quantity=item.Quantity,
                Price=item.Price
            )
            db.add(db_item)
        
        db.commit()
        logger.info(f"订单 {db_bill.BillID} 及其订单项创建完成")
        return db_bill
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
    orders = db.query(Bill).filter(
        Bill.BillDate >= start_date,
        Bill.BillDate <= end_date,
        (Bill.Status == '已结账')
    ).all()
    total_sales = sum(float(o.TotalAmount) for o in orders)
    order_count = len(orders)
    avg_order_value = total_sales / order_count if order_count else 0
    guest_ids = set(o.GuestID for o in orders if o.GuestID)
    new_customers = len(guest_ids)
    # 趋势数据
    trend = []
    if unit == "day":
        delta = timedelta(days=1)
        fmt = "%Y-%m-%d"
    elif unit == "week":
        delta = timedelta(weeks=1)
        fmt = "%Y-%W"
    else:
        delta = None
        fmt = "%Y-%m"
    # 这里只返回空趋势，前端可扩展
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
    return {
        "totalSales": total_sales,
        "orderCount": order_count,
        "avgOrderValue": avg_order_value,
        "newCustomers": new_customers,
        "trend": trend,
        "topProducts": [
            {"rank": i+1, "name": r[0], "sales": int(r[1]), "revenue": float(r[2]), "percentage": 0} for i, r in enumerate(top_products)
        ]
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
    # 新增客户
    new_customers = 0
    if start and end:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        new_customers = db.query(Guest).filter(Guest.bills.any(Bill.BillDate >= start_date), Guest.bills.any(Bill.BillDate <= end_date)).count()
    # 活跃客户、VIP、满意度等可根据实际需求扩展
    return {
        "totalCustomers": total_customers,
        "newCustomers": new_customers,
        "activeCustomers": 0,
        "vipCustomers": 0,
        "satisfaction": 100.0
    }

@app.get("/report/product")
def report_product(db: Session = Depends(get_db), start: str = Query(None), end: str = Query(None)):
    from datetime import datetime
    products = db.query(Product).all()
    total_products = len(products)
    active_products = total_products
    avg_price = sum(float(p.Price) for p in products) / total_products if total_products else 0
    # 类别数
    category_count = len(set(p.CategoryID for p in products))
    # 销量排行
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
        ]
    }

# 客户管理API
@app.get("/guests")
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
            "membershipID": getattr(g, 'MembershipID', None),
            "points": getattr(g, 'Points', 0),
            "orderCount": order_count,
            "lastOrderDate": last_order_date.isoformat() if last_order_date else None,
            # 下面字段如有可补充
            "phone": None,
            "email": None,
            "level": "normal",
            "createdAt": None,
            "address": None,
            "notes": None
        })
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9527) 