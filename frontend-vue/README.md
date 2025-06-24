# 超市管理系统前端（Vue 3）

本项目为超市管理系统的前端部分，基于 Vue 3 + Element Plus + Font Awesome 实现，配合 FastAPI 后端 API 实现商品、库存、订单、会员、报表等管理功能。

## 依赖环境
- Node.js 16+
- npm 8+

## 安装与启动
```bash
cd frontend-vue
npm install
npm run serve
```

默认访问地址：[http://localhost:9528](http://localhost:9528)

## 主要依赖
- vue@3
- element-plus
- axios
- @fortawesome/fontawesome-free

## 主要功能模块
- 仪表盘（数据总览、预警）
- 商品管理（增删改查、库存）
- 订单管理（下单、明细、状态）
- 库存管理（库存调整、预警）
- 会员管理（会员档案、积分）
- 报表统计（销售、库存、客户分析）
- 系统设置（主题、备份恢复）

## 与后端对接
- 后端API地址：`http://localhost:9527`
- 已配置开发代理，前端请求 `/api/*` 自动转发到后端
- 认证方式：Bearer Token，默认 `admin123`

## 常见问题
- 端口冲突：如 9528 被占用，可在 `vue.config.js` 修改
- 依赖安装失败：请确认 Node.js 和 npm 版本符合要求
- 后端连接失败：请确保后端服务已启动

---
如需完整系统说明，请参考项目根目录 `README.md`。 