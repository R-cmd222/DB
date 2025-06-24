import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'development' ? '/api' : 'http://localhost:9527',
  timeout: 10000,
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': 'Bearer admin123' 
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    console.log('发送请求:', config.url)
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('收到响应:', response.data)
    return response
  },
  error => {
    console.error('响应错误:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// 商品相关 API
export const productAPI = {
  // 获取所有商品
  getProducts() {
    return api.get('/products')
  },
  
  // 根据ID获取商品
  getProduct(id) {
    return api.get(`/products/${id}`)
  },
  
  // 创建商品
  createProduct(product) {
    const productData = {
      Name: product.Name,
      Price: product.Price,
      Stock: product.Stock,
      CategoryID: product.CategoryID,
      Unit: product.Unit
    }
    return api.post('/products', productData)
  },
  
  // 更新商品
  updateProduct(id, product) {
    const productData = {
      Name: product.Name,
      Price: product.Price,
      Stock: product.Stock,
      CategoryID: product.CategoryID,
      Unit: product.Unit
    }
    return api.put(`/products/${id}`, productData)
  },
  
  // 删除商品
  deleteProduct(id) {
    return api.delete(`/products/${id}`)
  }
}

// 类别相关 API
export const categoryAPI = {
  // 获取所有类别
  getCategories() {
    return api.get('/categories')
  }
}

// 统计相关 API
export const statsAPI = {
  // 获取统计信息
  getStats() {
    return api.get('/stats')
  }
}

// 系统相关 API
export const systemAPI = {
  // 健康检查
  healthCheck() {
    return api.get('/health')
  }
}

// 订单相关 API
export const billAPI = {
  // 获取所有订单
  getBills() {
    return api.get('/bills')
  },
  
  // 获取单个订单
  getBill(id) {
    return api.get(`/bills/${id}`)
  },
  
  // 创建订单
  createBill(bill) {
    return api.post('/bills', bill)
  }
}

// 仪表盘相关 API
export const dashboardAPI = {
  // 获取仪表盘销售额
  getDashboardSales() {
    return api.get('/dashboard/sales')
  },
  // 获取热销商品
  getTopProducts(limit = 5) {
    return api.get('/dashboard/top-products', { params: { limit } })
  }
}

export const reportAPI = {
  getSalesReport(params) {
    return api.get('/report/sales', { params })
  },
  getInventoryReport() {
    return api.get('/report/inventory')
  },
  getCustomerReport(params) {
    return api.get('/report/customer', { params })
  },
  getProductReport(params) {
    return api.get('/report/product', { params })
  }
}

export default api 