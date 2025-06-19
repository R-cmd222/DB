# 超市管理系统扩展指南

## 🎯 扩展路线图

### 阶段一：数据库集成 (1-2天)

#### 1.1 添加SQLite数据库
```python
# 安装依赖
pip install sqlalchemy

# 创建数据库模型
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### 1.2 数据库操作
```python
# 数据库连接
engine = create_engine("sqlite:///./supermarket.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建表
Base.metadata.create_all(bind=engine)

# 数据库操作函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 阶段二：用户认证 (2-3天)

#### 2.1 JWT认证实现
```python
# 安装依赖
pip install python-jose[cryptography] passlib[bcrypt]

# JWT工具函数
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

#### 2.2 用户模型和认证
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

# 认证依赖
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
```

### 阶段三：库存管理 (2-3天)

#### 3.1 库存模型
```python
class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)
    min_stock = Column(Integer, default=10)
    last_updated = Column(DateTime, default=datetime.utcnow)

class InventoryRecord(Base):
    __tablename__ = "inventory_records"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    type = Column(String)  # "in", "out", "adjust"
    quantity = Column(Integer)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### 3.2 库存操作
```python
def update_stock(db: Session, product_id: int, quantity: int, type: str, reason: str):
    # 更新库存
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        inventory = Inventory(product_id=product_id, quantity=0)
        db.add(inventory)
    
    if type == "in":
        inventory.quantity += quantity
    elif type == "out":
        inventory.quantity -= quantity
    elif type == "adjust":
        inventory.quantity = quantity
    
    # 记录库存变动
    record = InventoryRecord(
        product_id=product_id,
        type=type,
        quantity=quantity,
        reason=reason
    )
    db.add(record)
    db.commit()
    return inventory
```

### 阶段四：会员系统 (2-3天)

#### 4.1 会员模型
```python
class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    member_no = Column(String, unique=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True)
    email = Column(String)
    points = Column(Integer, default=0)
    level = Column(String, default="普通会员")
    created_at = Column(DateTime, default=datetime.utcnow)

class MemberTransaction(Base):
    __tablename__ = "member_transactions"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    type = Column(String)  # "earn", "spend"
    points = Column(Integer)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### 4.2 会员操作
```python
def add_member_points(db: Session, member_id: int, points: int, description: str):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="会员不存在")
    
    member.points += points
    
    transaction = MemberTransaction(
        member_id=member_id,
        type="earn",
        points=points,
        description=description
    )
    db.add(transaction)
    db.commit()
    return member
```

### 阶段五：收银台功能 (3-4天)

#### 5.1 购物车和订单
```python
class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String, unique=True, index=True)
    customer_name = Column(String)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=True)
    total_amount = Column(Float)
    discount_amount = Column(Float, default=0)
    final_amount = Column(Float)
    payment_method = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### 5.2 收银流程
```python
def create_order_from_cart(db: Session, session_id: str, customer_name: str, 
                          member_id: int = None, payment_method: str = "cash"):
    # 获取购物车商品
    cart_items = db.query(Cart).filter(Cart.session_id == session_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="购物车为空")
    
    # 计算总金额
    total_amount = 0
    order_items = []
    
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue
        
        item_total = product.price * item.quantity
        total_amount += item_total
        
        order_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": item.quantity,
            "unit_price": product.price,
            "total_price": item_total
        })
    
    # 创建订单
    order = Order(
        order_no=f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
        customer_name=customer_name,
        member_id=member_id,
        total_amount=total_amount,
        final_amount=total_amount,
        payment_method=payment_method
    )
    db.add(order)
    
    # 清空购物车
    db.query(Cart).filter(Cart.session_id == session_id).delete()
    
    db.commit()
    return order
```

### 阶段六：报表统计 (2-3天)

#### 6.1 销售报表
```python
def get_sales_report(db: Session, start_date: datetime, end_date: datetime):
    orders = db.query(Order).filter(
        Order.created_at >= start_date,
        Order.created_at <= end_date,
        Order.status == "completed"
    ).all()
    
    total_sales = sum(order.final_amount for order in orders)
    total_orders = len(orders)
    
    # 按日期分组统计
    daily_sales = {}
    for order in orders:
        date = order.created_at.date()
        if date not in daily_sales:
            daily_sales[date] = {"amount": 0, "count": 0}
        daily_sales[date]["amount"] += order.final_amount
        daily_sales[date]["count"] += 1
    
    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "daily_sales": daily_sales
    }
```

#### 6.2 库存报表
```python
def get_inventory_report(db: Session):
    inventory_items = db.query(Inventory).join(Product).all()
    
    low_stock = []
    out_of_stock = []
    
    for item in inventory_items:
        if item.quantity <= 0:
            out_of_stock.append({
                "product_name": item.product.name,
                "current_stock": item.quantity
            })
        elif item.quantity <= item.min_stock:
            low_stock.append({
                "product_name": item.product.name,
                "current_stock": item.quantity,
                "min_stock": item.min_stock
            })
    
    return {
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "total_products": len(inventory_items)
    }
```

### 阶段七：文件上传 (1-2天)

#### 7.1 图片上传
```python
# 安装依赖
pip install python-multipart aiofiles

from fastapi import File, UploadFile
import aiofiles
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/product-image/{product_id}")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 验证文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    
    # 保存文件
    file_path = f"{UPLOAD_DIR}/product_{product_id}_{file.filename}"
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)
    
    # 更新商品图片路径
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.image_url = file_path
        db.commit()
    
    return {"filename": file.filename, "file_path": file_path}
```

### 阶段八：缓存优化 (1-2天)

#### 8.1 Redis缓存
```python
# 安装依赖
pip install redis

import redis
import json

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def get_cached_products():
    cached = redis_client.get("products")
    if cached:
        return json.loads(cached)
    return None

def cache_products(products):
    redis_client.setex("products", 300, json.dumps(products))  # 缓存5分钟

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    # 先尝试从缓存获取
    cached = get_cached_products()
    if cached:
        return cached
    
    # 从数据库获取
    products = db.query(Product).all()
    product_list = [{"id": p.id, "name": p.name, "price": p.price} for p in products]
    
    # 缓存结果
    cache_products(product_list)
    
    return product_list
```

### 阶段九：部署配置 (2-3天)

#### 9.1 Docker配置
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 9.2 Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/supermarket
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=supermarket
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 阶段十：测试和监控 (2-3天)

#### 10.1 单元测试
```python
# 安装依赖
pip install pytest httpx

# tests/test_products.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product():
    product_data = {
        "name": "测试商品",
        "price": 10.99,
        "stock": 50,
        "category": "测试分类"
    }
    response = client.post(
        "/products",
        json=product_data,
        headers={"Authorization": "Bearer admin123"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "测试商品"
```

#### 10.2 健康检查和监控
```python
@app.get("/health")
def health_check():
    try:
        # 检查数据库连接
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

## 📚 学习资源

### FastAPI官方文档
- https://fastapi.tiangolo.com/
- https://fastapi.tiangolo.com/tutorial/

### SQLAlchemy文档
- https://docs.sqlalchemy.org/

### JWT认证
- https://jwt.io/
- https://python-jose.readthedocs.io/

### 数据库设计
- https://www.postgresql.org/docs/
- https://sqlite.org/docs.html

## 🎯 最佳实践

1. **代码组织**: 按功能模块分离代码
2. **错误处理**: 统一的异常处理机制
3. **日志记录**: 记录关键操作和错误信息
4. **数据验证**: 使用Pydantic进行数据验证
5. **安全考虑**: 输入验证、SQL注入防护
6. **性能优化**: 数据库索引、缓存策略
7. **测试覆盖**: 单元测试、集成测试

按照这个扩展指南，你可以逐步构建一个完整的超市管理系统。每个阶段都是独立的，可以单独开发和测试。 