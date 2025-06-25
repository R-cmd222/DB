import pyodbc
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接配置
SERVER = os.getenv('DB_SERVER', 'localhost')
DATABASE = os.getenv('DB_NAME', 'supermarket')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

def update_guests_table():
    """为Guests表添加Phone字段"""
    # 构建连接字符串
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}"
    
    try:
        # 连接数据库
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        print("=== 数据库表结构更新 ===\n")
        
        # 检查Phone字段是否已存在
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'Guests' AND COLUMN_NAME = 'Phone'
        """)
        
        if cursor.fetchone():
            print("✅ Phone字段已存在，无需添加")
        else:
            # 添加Phone字段
            print("正在为Guests表添加Phone字段...")
            cursor.execute("ALTER TABLE Guests ADD Phone NVARCHAR(20)")
            conn.commit()
            print("✅ Phone字段添加成功")
        
        # 验证表结构
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'Guests'
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = cursor.fetchall()
        print("\n当前Guests表结构:")
        for col in columns:
            print(f"  {col[0]}: {col[1]} ({'可空' if col[2] == 'YES' else '非空'})")
        
        # 显示现有客户数据
        cursor.execute("SELECT GuestID, Name, MembershipID, Points FROM Guests")
        guests = cursor.fetchall()
        print(f"\n现有客户数据 (共 {len(guests)} 个):")
        for guest in guests:
            print(f"  ID: {guest[0]}, 姓名: {guest[1]}, 会员ID: {guest[2] or '无'}, 积分: {guest[3]}")
        
        conn.close()
        print("\n✅ 数据库更新完成")
        
    except Exception as e:
        print(f"❌ 数据库更新失败: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    update_guests_table() 