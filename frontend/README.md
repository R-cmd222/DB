# 前端文件说明

## 文件结构

```
frontend/
├── supermarket-system.html    # 主页面文件
├── supermarket-script.js      # JavaScript逻辑文件
├── supermarket-styles.css     # 样式文件
└── README.md                 # 本说明文件
```

## 文件功能

### supermarket-system.html
- 主页面HTML文件
- 包含完整的用户界面结构
- 响应式设计，支持移动端
- 包含以下功能模块：
  - 仪表板
  - 收银台
  - 商品管理
  - 库存管理
  - 员工管理
  - 会员管理
  - 报表统计
  - 系统设置

### supermarket-script.js
- 主要的JavaScript逻辑文件
- 包含以下功能：
  - API通信（与后端FastAPI交互）
  - 页面导航和路由
  - 数据加载和显示
  - 用户交互处理
  - 模态框管理
  - 表单处理
  - 错误处理和用户反馈

### supermarket-styles.css
- 样式文件
- 现代化的UI设计
- 响应式布局
- 包含以下样式：
  - 侧边导航栏
  - 主内容区域
  - 数据表格
  - 卡片组件
  - 按钮和表单
  - 模态框
  - 状态指示器

## 技术特点

- **纯前端技术**：HTML + CSS + JavaScript
- **无框架依赖**：不依赖任何前端框架
- **响应式设计**：适配不同屏幕尺寸
- **模块化代码**：功能模块清晰分离
- **API集成**：与后端FastAPI完美集成

## 使用方法

1. 直接在浏览器中打开 `supermarket-system.html`
2. 或使用项目根目录的启动脚本：`python start_system.py`

## 开发说明

### 添加新功能
1. 在HTML中添加界面元素
2. 在CSS中添加样式
3. 在JavaScript中添加逻辑

### 修改API配置
在 `supermarket-script.js` 文件开头修改：
```javascript
const API_BASE_URL = 'http://localhost:8000';
const API_TOKEN = 'admin123';
```

### 调试
- 使用浏览器开发者工具
- 查看控制台日志
- 检查网络请求 