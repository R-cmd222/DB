# 超市管理系统前端（Vue 版）

本项目为超市管理系统的前端部分，基于 [Vue.js](https://vuejs.org/) 实现，配合后端 API 实现商品、库存、订单等管理功能。

## 项目结构

```
frontend-vue/
├── public/                # 静态资源目录
│   └── index.html         # 入口 HTML 文件
├── src/                   # 源码目录
│   ├── api/               # API 请求封装
│   │   └── index.js       # API 配置和方法
│   ├── components/        # 公共组件
│   │   └── Sidebar.vue
│   ├── views/             # 页面视图
│   │   ├── Dashboard.vue  # 仪表板
│   │   ├── Inventory.vue  # 库存管理
│   │   ├── Orders.vue     # 订单管理
│   │   └── Products.vue   # 商品管理
│   ├── App.vue            # 根组件
│   ├── main.js            # 入口 JS 文件
│   └── router.js          # 路由配置
├── package.json           # 项目依赖与脚本
├── vue.config.js          # Vue 配置文件（代理设置）
└── README.md              # 项目说明
```

## 环境准备

- Node.js 16+（建议使用 [nvm](https://github.com/nvm-sh/nvm) 管理 Node 版本）
- npm 8+ 或 yarn

## 安装依赖

```bash
cd frontend-vue
npm install
# 或
# yarn
```

## 启动开发服务器

```bash
npm run serve
# 或
# yarn serve
```

启动后，默认访问地址为 [http://localhost:8080](http://localhost:8080)

## 与后端连接

### 1. 确保后端服务运行

首先启动后端服务（在项目根目录执行）：
```bash
python start_system.py
```

后端服务将在 `http://localhost:8000` 启动。

### 2. 代理配置

项目已配置开发环境代理，前端请求 `/api/*` 会自动转发到后端 `http://localhost:8000/*`。

配置文件：`vue.config.js`

### 3. API 认证

后端使用 Bearer Token 认证，默认 token 为 `admin123`。

在 `src/api/index.js` 中已配置：
```javascript
headers: { 
  'Authorization': 'Bearer admin123' 
}
```

### 4. 功能模块

- **仪表板**：显示系统统计信息，包括商品总数、订单总数、库存总量、库存预警
- **商品管理**：商品的增删改查操作
- **库存管理**：库存查询和调整功能
- **订单管理**：订单列表查看和详情展示

## 构建生产包

```bash
npm run build
# 或
# yarn build
```

构建后的静态文件会输出到 `dist/` 目录。

## 开发注意事项

1. **跨域处理**：开发环境已配置代理，生产环境需要后端配置 CORS
2. **错误处理**：所有 API 请求都包含错误处理和用户提示
3. **加载状态**：所有数据加载操作都显示加载状态
4. **表单验证**：所有表单都包含验证规则

## 常见问题

1. **端口冲突**：如 8080 端口被占用，可在 `vue.config.js` 中修改端口
2. **后端连接失败**：确保后端服务在 `http://localhost:8000` 正常运行
3. **认证失败**：检查 token 是否正确，默认使用 `admin123`
4. **依赖安装失败**：请确保 Node.js 和 npm/yarn 版本符合要求

## 启动完整系统

1. 在项目根目录执行：`python start_system.py`
2. 在 `frontend-vue` 目录执行：`npm run serve`
3. 访问前端：http://localhost:8080
4. 访问后端 API 文档：http://localhost:8000/docs

## 联系方式

如有问题或建议，请联系项目维护者。 