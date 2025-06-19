# 超市管理系统

一个基于FastAPI后端和HTML/JavaScript前端的超市管理系统。

## 系统架构

- **后端**: FastAPI (Python) - 提供RESTful API
- **前端**: HTML + CSS + JavaScript - 用户界面
- **数据存储**: 内存存储（演示用，生产环境应使用数据库）

## 功能特性

### 后端API功能
- ✅ 商品管理 (CRUD操作)
- ✅ 订单管理
- ✅ 基础统计信息
- ✅ 简单的Bearer Token认证
- ✅ CORS支持

### 前端功能
- ✅ 响应式仪表板
- ✅ 商品管理界面
- ✅ 库存管理
- ✅ 收银台功能
- ✅ 员工管理
- ✅ 会员管理
- ✅ 报表统计
- ✅ 系统设置

## 快速开始

### 方法一：使用启动脚本（推荐）

1. 确保已安装Python 3.7+
2. 安装依赖：
   ```bash
   cd backend-python-minimal
   pip install -r requirements.txt
   ```
3. 运行启动脚本：
   ```bash
   python start_system.py
   ```

### 方法二：手动启动

1. 启动后端服务器：
   ```bash
   cd backend-python-minimal
   python app.py
   ```

2. 打开前端页面：
   - 直接双击 `supermarket-system.html` 文件
   - 或在浏览器中打开该文件

## 访问地址

- **前端页面**: `frontend/supermarket-system.html`
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **交互式API文档**: http://localhost:8000/redoc

## API认证

系统使用简单的Bearer Token认证：
- Token: `admin123`
- 在请求头中添加: `Authorization: Bearer admin123`

## API端点

### 商品管理
- `GET /products` - 获取所有商品
- `GET /products/{id}` - 获取单个商品
- `POST /products` - 创建商品
- `PUT /products/{id}` - 更新商品
- `DELETE /products/{id}` - 删除商品

### 订单管理
- `GET /orders` - 获取所有订单
- `POST /orders` - 创建订单

### 统计信息
- `GET /stats` - 获取基础统计信息

## 文件结构

```
DB课设/
├── backend-python-minimal/     # 后端代码
│   ├── app.py                 # FastAPI主应用
│   ├── requirements.txt       # Python依赖
│   └── README.md             # 后端说明
├── frontend/                  # 前端代码
│   ├── supermarket-system.html    # 前端主页面
│   ├── supermarket-script.js      # 前端JavaScript
│   └── supermarket-styles.css     # 前端样式
├── start_system.py           # 启动脚本
└── README.md                 # 项目说明
```

## 开发说明

### 后端开发
- 使用FastAPI框架
- 支持热重载（开发模式）
- 包含完整的API文档

### 前端开发
- 纯HTML/CSS/JavaScript
- 响应式设计
- 模块化JavaScript代码

### 数据流
1. 前端通过fetch API调用后端接口
2. 后端处理请求并返回JSON数据
3. 前端更新DOM显示数据

## 故障排除

### 常见问题

1. **后端启动失败**
   - 检查Python版本 (需要3.7+)
   - 检查依赖是否正确安装
   - 检查端口8000是否被占用

2. **前端无法连接后端**
   - 确保后端服务器正在运行
   - 检查浏览器控制台是否有CORS错误
   - 确认API地址配置正确

3. **API请求失败**
   - 检查认证token是否正确
   - 查看后端日志获取详细错误信息

### 调试模式

启动后端时添加调试信息：
```bash
cd backend-python-minimal
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 扩展功能

### 计划中的功能
- [ ] 数据库集成 (SQLite/PostgreSQL)
- [ ] 用户认证系统
- [ ] 文件上传功能
- [ ] 更详细的报表
- [ ] 打印功能
- [ ] 数据导出功能

### 贡献指南
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

MIT License 