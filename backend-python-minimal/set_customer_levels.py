#!/usr/bin/env python3
"""
设置客户等级脚本：根据积分设置客户等级
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

def set_customer_levels():
    """根据积分设置客户等级"""
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            print("开始设置客户等级...")
            
            # 根据积分设置等级
            # 0-1999: normal (普通客户)
            # 2000-4999: vip (VIP客户)
            # 5000+: diamond (钻石客户)
            
            update_levels = text("""
                UPDATE Guests 
                SET Level = CASE 
                    WHEN Points >= 5000 THEN 'diamond'
                    WHEN Points >= 2000 THEN 'vip'
                    ELSE 'normal'
                END
                WHERE Level IS NULL OR Level = ''
            """)
            
            result = conn.execute(update_levels)
            print(f"更新了 {result.rowcount} 个客户的等级")
            
            # 提交事务
            conn.commit()
            print("客户等级设置完成！")
            
    except Exception as e:
        print(f"设置失败: {e}")
        return False
    
    return True

def show_customer_levels():
    """显示客户等级分布"""
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            print("\n客户等级分布:")
            print("-" * 40)
            
            # 统计各等级客户数量
            stats_query = text("""
                SELECT Level, COUNT(*) as count, AVG(Points) as avg_points
                FROM Guests 
                GROUP BY Level
                ORDER BY 
                    CASE Level 
                        WHEN 'diamond' THEN 3
                        WHEN 'vip' THEN 2
                        WHEN 'normal' THEN 1
                        ELSE 0
                    END DESC
            """)
            
            result = conn.execute(stats_query)
            stats = result.fetchall()
            
            for stat in stats:
                level_name = {
                    'normal': '普通客户',
                    'vip': 'VIP客户', 
                    'diamond': '钻石客户'
                }.get(stat[0], stat[0])
                
                print(f"{level_name}: {stat[1]} 人 (平均积分: {stat[2]:.0f})")
            
            # 显示详细客户列表
            print("\n客户详细信息:")
            print("-" * 60)
            
            detail_query = text("""
                SELECT GuestID, Name, Level, Points, Phone
                FROM Guests 
                ORDER BY Points DESC
            """)
            
            result = conn.execute(detail_query)
            customers = result.fetchall()
            
            for customer in customers:
                level_name = {
                    'normal': '普通客户',
                    'vip': 'VIP客户',
                    'diamond': '钻石客户'
                }.get(customer[2], customer[2])
                
                phone = customer[4] if customer[4] else '无'
                print(f"ID: {customer[0]:2d}, 姓名: {customer[1]:<8}, 等级: {level_name:<6}, 积分: {customer[3]:4d}, 电话: {phone}")
            
            return True
            
    except Exception as e:
        print(f"查询失败: {e}")
        return False

if __name__ == "__main__":
    print("客户等级设置脚本")
    print("=" * 50)
    
    # 设置客户等级
    if set_customer_levels():
        # 显示结果
        show_customer_levels()
        print("\n设置完成！")
    else:
        print("设置失败！")
        sys.exit(1) 