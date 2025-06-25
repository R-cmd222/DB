import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:9527',
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = sessionStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response?.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
      sessionStorage.clear()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 商品API
export const productAPI = {
  getProducts: () => api.get('/products'),
  getProduct: (id) => api.get(`/products/${id}`),
  createProduct: (data) => api.post('/products', data),
  updateProduct: (id, data) => api.put(`/products/${id}`, data),
  deleteProduct: (id) => api.delete(`/products/${id}`)
}

// 类别相关 API
export const categoryAPI = {
  // 获取所有类别
  getCategories() {
    return api.get('/categories')
  }
}

// 统计API
export const statsAPI = {
  getStats: () => api.get('/stats'),
  getSalesReport: (start, end, unit = 'day') => api.get('/report/sales', { params: { start, end, unit } }),
  getInventoryReport: () => api.get('/report/inventory'),
  getCustomerReport: (start, end) => api.get('/report/customer', { params: { start, end } }),
  getProductReport: (start, end) => api.get('/report/product', { params: { start, end } })
}

// 系统相关 API
export const systemAPI = {
  // 健康检查
  healthCheck() {
    return api.get('/health')
  }
}

// 订单API
export const billAPI = {
  getBills: () => api.get('/bills'),
  getBill: (id) => api.get(`/bills/${id}`),
  createBill: (data) => api.post('/bills', data)
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

// 收银台API
export const cashierAPI = {
  checkout: (data) => api.post('/cashier/checkout', data)
}

// 客户API
export const guestAPI = {
  getGuests: () => api.get('/guests'),
  getGuest: (id) => api.get(`/guests/${id}`),
  createGuest: (data) => api.post('/guests', data),
  updateGuest: (id, data) => api.put(`/guests/${id}`, data),
  deleteGuest: (id) => api.delete(`/guests/${id}`)
}

// 员工API
export const employeeAPI = {
  changePassword: (data) => api.post('/change_password', data)
}

export default api 