from sqlalchemy import create_engine, MetaData, Column, Integer, String, DECIMAL, DateTime, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv()

# 数据库连接配置
SERVER = os.getenv('DB_SERVER', 'localhost')
DATABASE = os.getenv('DB_NAME', 'supermarket')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

# 创建数据库连接URL
DATABASE_URL = f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()
metadata = MetaData()

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 员工模型
class Employee(Base):
    __tablename__ = "Employees"
    
    EmployeeID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    Gender = Column(String(4))
    BirthDate = Column(Date, nullable=False)
    Position = Column(String(50), nullable=False)
    Phone = Column(String(20), unique=True)
    
    bills = relationship("Bill", back_populates="employee")

# 会员模型
class Guest(Base):
    __tablename__ = "Guests"
    
    GuestID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    MembershipID = Column(String(50))
    Points = Column(Integer, default=0)
    
    bills = relationship("Bill", back_populates="guest")

# 商品类别模型
class Category(Base):
    __tablename__ = "Categories"
    
    CategoryID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False, unique=True)
    
    products = relationship("Product", back_populates="category")

# 商品模型
class Product(Base):
    __tablename__ = "Products"
    
    ProductID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)
    Stock = Column(Integer, default=0)
    Unit = Column(String(10))
    LastInDate = Column(DateTime)
    CategoryID = Column(Integer, ForeignKey("Categories.CategoryID"), nullable=False)
    
    category = relationship("Category", back_populates="products")
    bill_items = relationship("BillItem", back_populates="product")

# 账单模型
class Bill(Base):
    __tablename__ = "Bills"
    
    BillID = Column(Integer, primary_key=True)
    TotalAmount = Column(DECIMAL(10, 2), nullable=False)
    Status = Column(String(20))
    PaymentMethod = Column(String(20), nullable=False, default='现金')
    BillDate = Column(DateTime, default=datetime.utcnow)
    EmployeeID = Column(Integer, ForeignKey("Employees.EmployeeID"), nullable=False)
    GuestID = Column(Integer, ForeignKey("Guests.GuestID"))
    
    employee = relationship("Employee", back_populates="bills")
    guest = relationship("Guest", back_populates="bills")
    items = relationship("BillItem", back_populates="bill")

# 账单项目模型
class BillItem(Base):
    __tablename__ = "BillItems"
    
    BillItemID = Column(Integer, primary_key=True)
    BillID = Column(Integer, ForeignKey("Bills.BillID"), nullable=False)
    ProductID = Column(Integer, ForeignKey("Products.ProductID"), nullable=False)
    Quantity = Column(Integer, nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)
    
    bill = relationship("Bill", back_populates="items")
    product = relationship("Product", back_populates="bill_items")
