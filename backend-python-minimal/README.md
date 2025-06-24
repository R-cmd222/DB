# 超市管理系统后端（FastAPI）

本项目为超市管理系统的后端服务，基于 FastAPI + SQLAlchemy + pyodbc 实现，支持商品、库存、订单、会员、报表等管理。

## 依赖环境
- Python 3.8+
- SQL Server（或兼容数据库）

## 安装与启动
```bash
cd backend-python-minimal
pip install -r requirements.txt
python app.py
```

默认API地址：[http://localhost:9527](http://localhost:9527)
API文档：[http://localhost:9527/docs](http://localhost:9527/docs)

## 主要依赖
- fastapi
- uvicorn
- sqlalchemy
- pyodbc
- python-dotenv

## 数据库配置
请在 `backend-python-minimal/.env` 文件中配置数据库连接：
```
DB_SERVER=localhost
DB_NAME=supermarket
DB_USERNAME=你的用户名
DB_PASSWORD=你的密码
```

## 主要功能模块
- 商品管理（增删改查、库存）
- 订单管理（下单、明细、状态）
- 库存管理（库存调整、预警）
- 会员管理（会员档案、积分）
- 报表统计（销售、库存、客户分析）
- 系统设置（主题、备份恢复）

## 认证方式
- Bearer Token，默认 `admin123`
- 在请求头添加：`Authorization: Bearer admin123`

## 常见问题
- 端口冲突：如 9527 被占用，请在 app.py 修改
- 数据库连接失败：请检查 .env 配置和数据库服务
- 依赖安装失败：请确认 Python 版本和 pip 可用

---
如需完整系统说明，请参考项目根目录 `README.md`。 