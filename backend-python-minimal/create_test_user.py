#!/usr/bin/env python3
"""
创建测试用户脚本
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

def create_test_user():
    """创建测试用户"""
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            print("检查并创建测试用户...")
            
            # 检查admin用户是否存在
            check_user = text("""
                SELECT EmployeeID, Name, username 
                FROM Employees 
                WHERE username = 'admin'
            """)
            result = conn.execute(check_user)
            existing_user = result.fetchone()
            
            if existing_user:
                print(f"用户 'admin' 已存在 (ID: {existing_user[0]}, 姓名: {existing_user[1]})")
            else:
                print("创建测试用户 'admin'...")
                # 创建admin用户
                create_user = text("""
                    INSERT INTO Employees (Name, Gender, BirthDate, Position, Phone, username, password, role)
                    VALUES ('管理员', '男', '1990-01-01', '管理员', '13800138000', 'admin', 'admin123', 'admin')
                """)
                conn.execute(create_user)
                conn.commit()
                print("测试用户创建成功！")
            
            # 显示所有员工
            print("\n当前员工列表:")
            all_users = text("SELECT EmployeeID, Name, username, Position FROM Employees")
            result = conn.execute(all_users)
            users = result.fetchall()
            
            for user in users:
                print(f"  ID: {user[0]}, 姓名: {user[1]}, 用户名: {user[2]}, 职位: {user[3]}")
            
            return True
            
    except Exception as e:
        print(f"创建用户失败: {e}")
        return False

if __name__ == "__main__":
    print("创建测试用户脚本")
    print("=" * 30)
    
    if create_test_user():
        print("\n脚本执行完成！")
        print("可以使用以下凭据登录:")
        print("  用户名: admin")
        print("  密码: admin123")
    else:
        print("脚本执行失败！")
        sys.exit(1) 