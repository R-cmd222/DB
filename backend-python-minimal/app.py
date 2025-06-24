from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
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
        return bills
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
        return bill
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9527) 