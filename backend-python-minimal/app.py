from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models import SessionLocal, Category, Product, Employee, Guest, Bill, BillItem

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
    total_stock = db.query(Product).with_entities(func.sum(Product.Stock)).scalar() or 0
    low_stock_products = db.query(Product).filter(Product.Stock < 10).count()
    
    return {
        "total_products": total_products,
        "total_stock": total_stock,
        "low_stock_products": low_stock_products
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 