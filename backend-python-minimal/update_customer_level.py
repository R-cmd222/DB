#!/usr/bin/env python3
"""
数据库迁移脚本：将客户表的MembershipID字段改为Level字段
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接配置
SERVER = os.getenv('DB_SERVER', 'localhost')
DATABASE = os.getenv('DB_NAME', 'supermarket')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

# 创建数据库连接URL
DATABASE_URL = f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"

def update_customer_schema():
    """更新客户表结构"""
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            print("开始更新客户表结构...")
            
            # 检查Level字段是否已存在
            check_level = text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Guests' AND COLUMN_NAME = 'Level'
            """)
            result = conn.execute(check_level)
            level_exists = result.fetchone() is not None
            
            if not level_exists:
                print("添加Level字段...")
                # 添加Level字段
                add_level = text("ALTER TABLE Guests ADD Level NVARCHAR(20) DEFAULT 'normal'")
                conn.execute(add_level)
                print("Level字段添加成功")
            else:
                print("Level字段已存在")
            
            # 检查MembershipID字段是否存在
            check_membership = text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Guests' AND COLUMN_NAME = 'MembershipID'
            """)
            result = conn.execute(check_membership)
            membership_exists = result.fetchone() is not None
            
            if membership_exists:
                print("删除MembershipID字段...")
                # 删除MembershipID字段
                drop_membership = text("ALTER TABLE Guests DROP COLUMN MembershipID")
                conn.execute(drop_membership)
                print("MembershipID字段删除成功")
            else:
                print("MembershipID字段不存在")
            
            # 提交事务
            conn.commit()
            print("客户表结构更新完成！")
            
    except Exception as e:
        print(f"更新失败: {e}")
        return False
    
    return True

def test_customer_data():
    """测试客户数据"""
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            print("\n测试客户数据...")
            
            # 查询客户数据
            query = text("SELECT GuestID, Name, Level, Points, Phone FROM Guests")
            result = conn.execute(query)
            customers = result.fetchall()
            
            print(f"找到 {len(customers)} 个客户:")
            for customer in customers[:5]:  # 只显示前5个
                print(f"  ID: {customer[0]}, 姓名: {customer[1]}, 等级: {customer[2]}, 积分: {customer[3]}, 电话: {customer[4]}")
            
            if len(customers) > 5:
                print(f"  ... 还有 {len(customers) - 5} 个客户")
            
            return True
            
    except Exception as e:
        print(f"测试失败: {e}")
        return False

if __name__ == "__main__":
    print("客户等级系统迁移脚本")
    print("=" * 50)
    
    # 更新数据库结构
    if update_customer_schema():
        # 测试数据
        test_customer_data()
        print("\n迁移完成！")
    else:
        print("迁移失败！")
        sys.exit(1) 