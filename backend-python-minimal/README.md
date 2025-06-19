# 超市管理系统 - 最小可运行版本

这是一个最小可运行的超市管理系统后端，基于FastAPI框架开发。

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
python app.py
```

### 3. 访问API文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📋 当前功能

### 基础功能
- ✅ 商品管理 (CRUD)
- ✅ 订单管理
- ✅ 基础统计
- ✅ 简单认证

### API端点

#### 商品管理
- `GET /products` - 获取所有商品
- `GET /products/{id}` - 获取单个商品
- `POST /products` - 创建商品 (需要认证)
- `PUT /products/{id}` - 更新商品 (需要认证)
- `DELETE /products/{id}` - 删除商品 (需要认证)

#### 订单管理
- `GET /orders` - 获取所有订单
- `POST /orders` - 创建订单

#### 其他
- `GET /` - 欢迎页面
- `GET /health` - 健康检查
- `GET /stats` - 统计信息

## 🔐 认证

当前使用简单的Bearer Token认证：
- Token: `admin123`
- 在请求头中添加: `Authorization: Bearer admin123`

## 📝 使用示例

### 获取所有商品
```bash
curl http://localhost:8000/products
```

### 创建商品
```bash
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer admin123" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "香蕉",
    "price": 4.99,
    "stock": 80,
    "category": "水果"
  }'
```

### 创建订单
```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "张三",
    "items": [
      {"product_id": 1, "quantity": 2, "price": 5.99}
    ],
    "total": 11.98
  }'
```

## 🔄 下一步扩展建议

### 第一阶段：基础完善
1. **数据库集成**
   - 添加SQLite或PostgreSQL
   - 使用SQLAlchemy ORM
   - 数据持久化

2. **用户认证**
   - 实现JWT认证
   - 用户注册/登录
   - 密码加密

3. **数据验证**
   - 完善Pydantic模型
   - 添加业务逻辑验证

### 第二阶段：功能扩展
4. **库存管理**
   - 库存变动记录
   - 库存预警
   - 批量操作

5. **会员系统**
   - 会员信息管理
   - 积分系统
   - 会员等级

6. **收银台功能**
   - 购物车
   - 支付处理
   - 小票打印

### 第三阶段：高级功能
7. **报表统计**
   - 销售报表
   - 库存报表
   - 图表展示

8. **文件管理**
   - 商品图片上传
   - 文件存储

9. **缓存优化**
   - Redis缓存
   - 性能优化

### 第四阶段：生产就绪
10. **部署配置**
    - Docker容器化
    - 环境配置
    - 日志系统

11. **监控告警**
    - 健康检查
    - 性能监控
    - 错误告警

12. **安全加固**
    - 输入验证
    - SQL注入防护
    - 权限控制

## 📁 项目结构建议

```
backend-python/
├── app.py                 # 当前主文件
├── requirements.txt       # 依赖文件
├── README.md             # 说明文档
├── .env                  # 环境变量 (扩展时添加)
├── database/             # 数据库相关 (扩展时添加)
├── models/               # 数据模型 (扩展时添加)
├── services/             # 业务逻辑 (扩展时添加)
├── utils/                # 工具函数 (扩展时添加)
└── tests/                # 测试文件 (扩展时添加)
```

## 🎯 学习路径

1. **熟悉FastAPI基础**
   - 路由定义
   - 请求/响应模型
   - 依赖注入

2. **学习数据库操作**
   - SQLAlchemy基础
   - 数据库设计
   - 查询优化

3. **掌握认证授权**
   - JWT原理
   - 权限控制
   - 安全最佳实践

4. **了解部署运维**
   - Docker使用
   - 环境管理
   - 监控日志

这个最小版本为你提供了一个可运行的起点，你可以根据上述建议逐步扩展功能，每个阶段都可以独立开发和测试。 