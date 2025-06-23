import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'development' ? '/api' : 'http://localhost:8000',
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
      Name: product.name,
      Price: product.price,
      Stock: product.stock,
      CategoryID: product.categoryId,
      Unit: product.unit
    }
    return api.post('/products', productData)
  },
  
  // 更新商品
  updateProduct(id, product) {
    const productData = {
      Name: product.name,
      Price: product.price,
      Stock: product.stock,
      CategoryID: product.categoryId,
      Unit: product.unit
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

export default api 