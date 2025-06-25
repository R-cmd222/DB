from app import get_db, Guest
from sqlalchemy.orm import Session

def check_database():
    """检查数据库中的客户数据"""
    print("=== 数据库客户数据检查 ===\n")
    
    db = next(get_db())
    try:
        guests = db.query(Guest).all()
        print(f"找到 {len(guests)} 个客户:")
        for guest in guests:
            phone = getattr(guest, 'Phone', '无')
            print(f"  ID: {guest.GuestID}, 姓名: {guest.Name}, 电话: {phone}, 积分: {guest.Points}")
    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database() 