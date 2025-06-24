# 超市管理系统（现代版）

本项目为现代化超市管理系统，采用 FastAPI + SQLAlchemy（Python）为后端，Vue 3 + Element Plus + Font Awesome 为前端，支持商品、库存、订单、会员、报表等全流程管理。

## 目录结构
```
DB课设/
├── backend-python-minimal/   # 后端服务（FastAPI）
├── frontend-vue/            # 前端服务（Vue 3）
├── SQL/                     # 数据库脚本
├── start_system.py          # 一键启动脚本
└── README.md                # 项目说明
```

## 依赖环境
- Python 3.8+
- Node.js 16+
- npm 8+
- SQL Server（或兼容数据库）

## 安装与启动

### 一键启动（推荐）
```bash
# 安装后端依赖
cd backend-python-minimal
pip install -r requirements.txt

# 回到项目根目录，运行一键启动脚本
cd ..
python start_system.py
```

### 手动启动
```bash
# 启动后端
cd backend-python-minimal
python app.py

# 启动前端
cd ../frontend-vue
npm install
npm run serve
```

## 访问方式
- 前端页面：http://localhost:9528
- 后端API：http://localhost:9527
- API文档：http://localhost:9527/docs

## 主要功能
- 仪表盘（数据总览、预警）
- 商品管理（增删改查、库存）
- 订单管理（下单、明细、状态）
- 库存管理（库存调整、预警）
- 会员管理（会员档案、积分）
- 报表统计（销售、库存、客户分析）
- 系统设置（主题、备份恢复）

## 依赖说明
### 后端主要依赖
- fastapi
- uvicorn
- sqlalchemy
- pyodbc
- python-dotenv

### 前端主要依赖
- vue@3
- element-plus
- axios
- @fortawesome/fontawesome-free

## 常见问题
- 端口冲突：如 9527/9528 被占用，请在配置文件中修改
- 数据库连接失败：请检查 backend-python-minimal/.env 配置
- 依赖安装失败：请确认 Python/Node/npm 版本符合要求

---
如需详细开发文档，请分别参考 backend-python-minimal/README.md 和 frontend-vue/README.md。 