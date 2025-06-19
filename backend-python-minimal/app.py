from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import json

# 简单的内存数据存储（实际项目中应使用数据库）
products_db = [
    {"id": 1, "name": "苹果", "price": 5.99, "stock": 100, "category": "水果"},
    {"id": 2, "name": "牛奶", "price": 8.50, "stock": 50, "category": "乳制品"},
    {"id": 3, "name": "面包", "price": 3.99, "stock": 30, "category": "烘焙"},
]

orders_db = []
users_db = [
    {"id": 1, "username": "admin", "password": "admin123", "role": "admin"}
]

# Pydantic模型
class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    stock: int
    category: str

class Order(BaseModel):
    id: Optional[int] = None
    customer_name: str
    items: List[dict]
    total: float
    created_at: Optional[datetime] = None

class User(BaseModel):
    username: str
    password: str

# 简单的认证（实际项目中应使用JWT）
security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    # 简单验证，实际项目中应验证JWT token
    if token.credentials != "admin123":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": "admin", "role": "admin"}

# 创建FastAPI应用
app = FastAPI(title="超市管理系统", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
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
@app.get("/products", response_model=List[Product])
def get_products():
    """获取所有商品"""
    return products_db

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    """根据ID获取商品"""
    for product in products_db:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="商品不存在")

@app.post("/products", response_model=Product)
def create_product(product: Product, current_user: dict = Depends(get_current_user)):
    """创建新商品"""
    product.id = max([p["id"] for p in products_db]) + 1 if products_db else 1
    product_dict = product.dict()
    products_db.append(product_dict)
    return product_dict

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product, current_user: dict = Depends(get_current_user)):
    """更新商品"""
    for i, p in enumerate(products_db):
        if p["id"] == product_id:
            product.id = product_id
            products_db[i] = product.dict()
            return products_db[i]
    raise HTTPException(status_code=404, detail="商品不存在")

@app.delete("/products/{product_id}")
def delete_product(product_id: int, current_user: dict = Depends(get_current_user)):
    """删除商品"""
    for i, product in enumerate(products_db):
        if product["id"] == product_id:
            del products_db[i]
            return {"message": "商品删除成功"}
    raise HTTPException(status_code=404, detail="商品不存在")

# 订单管理API
@app.get("/orders", response_model=List[Order])
def get_orders():
    """获取所有订单"""
    return orders_db

@app.post("/orders", response_model=Order)
def create_order(order: Order):
    """创建新订单"""
    order.id = max([o["id"] for o in orders_db]) + 1 if orders_db else 1
    order.created_at = datetime.now()
    order_dict = order.dict()
    orders_db.append(order_dict)
    return order_dict

# 简单的统计API
@app.get("/stats")
def get_stats():
    """获取基础统计信息"""
    total_products = len(products_db)
    total_orders = len(orders_db)
    total_stock = sum(p["stock"] for p in products_db)
    
    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_stock": total_stock,
        "low_stock_products": len([p for p in products_db if p["stock"] < 10])
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 