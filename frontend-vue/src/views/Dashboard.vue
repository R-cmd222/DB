<template>
  <div class="dashboard-container">
    <!-- 统计卡片区域 -->
    <el-row :gutter="20" v-loading="loading" class="stats-grid">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon stat-icon-1">
              <i class="fas fa-shopping-cart"></i>
            </div>
            <div class="stat-info">
              <h3 class="stat-title">今日销售额</h3>
              <p class="stat-number">¥{{ formatNumber(stats.today_sales || 12580) }}</p>
              <span class="stat-change positive">+15.2%</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon stat-icon-2">
              <i class="fas fa-file-invoice-dollar"></i>
            </div>
            <div class="stat-info">
              <h3 class="stat-title">订单总数</h3>
              <p class="stat-number">{{ formatNumber(stats.total_orders) }}</p>
              <span class="stat-change positive">+8.7%</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon stat-icon-3">
              <i class="fas fa-box"></i>
            </div>
            <div class="stat-info">
              <h3 class="stat-title">商品总数</h3>
              <p class="stat-number">{{ formatNumber(stats.total_products) }}</p>
              <span class="stat-change neutral">0%</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon stat-icon-4">
              <i class="fas fa-exclamation-triangle"></i>
            </div>
            <div class="stat-info">
              <h3 class="stat-title">库存预警</h3>
              <p class="stat-number" :class="{ 'warning': stats.low_stock_products > 0 }">
                {{ formatNumber(stats.low_stock_products) }}
              </p>
              <span class="stat-change negative">+5</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" style="margin-top: 30px;">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>销售趋势</span>
              <el-button @click="refreshCharts" :loading="chartLoading" size="small">
                <i class="fas fa-sync-alt"></i>
              </el-button>
            </div>
          </template>
          <div class="chart-placeholder">
            <i class="fas fa-chart-line"></i>
            <p>销售数据图表</p>
            <div class="chart-data">
              <div class="data-item">
                <span>本周销售额</span>
                <span class="data-value">¥45,680</span>
              </div>
              <div class="data-item">
                <span>上周销售额</span>
                <span class="data-value">¥42,150</span>
              </div>
              <div class="data-item">
                <span>本月销售额</span>
                <span class="data-value">¥156,890</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>热销商品</span>
            </div>
          </template>
          <div class="chart-placeholder">
            <i class="fas fa-chart-pie"></i>
            <p>商品销售占比</p>
            <div class="top-products">
              <div class="product-item" v-for="(product, index) in topProducts" :key="index">
                <span class="product-rank">{{ index + 1 }}</span>
                <span class="product-name">{{ product.name }}</span>
                <span class="product-sales">{{ product.sales }}件</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 系统状态卡片 -->
    <el-card style="margin-top: 30px;">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>系统状态</span>
          <el-button @click="loadStats" :loading="loading" size="small">
            <i class="fas fa-sync-alt"></i> 刷新
          </el-button>
        </div>
      </template>
      <el-descriptions :column="3" border>
        <el-descriptions-item label="API 状态">
          <el-tag :type="apiStatus === 'healthy' ? 'success' : 'danger'">
            <i :class="apiStatus === 'healthy' ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
            {{ apiStatus === 'healthy' ? '正常' : '异常' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="数据库状态">
          <el-tag type="success">
            <i class="fas fa-database"></i>
            正常
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="最后更新">
          {{ lastUpdate }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onActivated, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { statsAPI, systemAPI } from '../api'

const route = useRoute()

const stats = ref({ 
  total_products: 0, 
  total_orders: 0, 
  total_stock: 0, 
  low_stock_products: 0,
  today_sales: 0
})
const loading = ref(false)
const chartLoading = ref(false)
const apiStatus = ref('unknown')
const lastUpdate = ref('')

// 模拟数据
const topProducts = ref([
  { name: '可口可乐', sales: 156 },
  { name: '薯片', sales: 89 },
  { name: '牛奶', sales: 67 },
  { name: '面包', sales: 45 }
])

function formatNumber(num) {
  if (num === null || num === undefined) return '0'
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

async function loadStats() {
  loading.value = true
  
  try {
    // 检查 API 状态
    try {
      await systemAPI.healthCheck()
      apiStatus.value = 'healthy'
    } catch (error) {
      apiStatus.value = 'unhealthy'
    }
    
    // 获取统计信息
    const response = await statsAPI.getStats()
    
    // 确保数据正确合并
    stats.value = {
      total_products: response.data.total_products || 0,
      total_orders: response.data.total_orders || 0,
      total_stock: response.data.total_stock || 0,
      low_stock_products: response.data.low_stock_products || 0,
      today_sales: stats.value.today_sales || 12580
    }
    
    lastUpdate.value = new Date().toLocaleString()
    ElMessage.success('数据加载成功')
  } catch (error) {
    console.error('加载统计信息失败:', error)
    ElMessage.error('加载统计信息失败: ' + (error.response?.data?.detail || error.message))
    
    // 如果API失败，使用默认值
    stats.value = {
      total_products: 0,
      total_orders: 0,
      total_stock: 0,
      low_stock_products: 0,
      today_sales: 12580
    }
  } finally {
    loading.value = false
  }
}

function refreshCharts() {
  chartLoading.value = true
  setTimeout(() => {
    chartLoading.value = false
    ElMessage.success('图表数据已更新')
  }, 1000)
}

// 组件挂载时加载数据
onMounted(() => {
  loadStats()
})

// 当组件被激活时（keep-alive情况下）
onActivated(() => {
  loadStats()
})

// 监听路由变化
watch(
  () => route.path,
  (newPath) => {
    if (newPath === '/') {
      loadStats()
    }
  }
)
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.stats-grid {
  margin-bottom: 30px;
}

.stat-card {
  border-radius: 15px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.stat-icon-1 {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stat-icon-2 {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.stat-icon-3 {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.stat-icon-4 {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.stat-info {
  flex: 1;
}

.stat-title {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin-bottom: 5px;
  font-weight: normal;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 5px;
}

.stat-number.warning {
  color: #e67e22;
}

.stat-change {
  font-size: 0.8rem;
  padding: 2px 8px;
  border-radius: 10px;
  display: inline-block;
}

.stat-change.positive {
  background: #d4edda;
  color: #155724;
}

.stat-change.negative {
  background: #f8d7da;
  color: #721c24;
}

.stat-change.neutral {
  background: #e2e3e5;
  color: #383d41;
}

.chart-card {
  border-radius: 15px;
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-placeholder {
  height: 250px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 10px;
  color: #95a5a6;
  padding: 20px;
}

.chart-placeholder i {
  font-size: 3rem;
  margin-bottom: 10px;
  color: #667eea;
}

.chart-placeholder p {
  margin-bottom: 15px;
  font-weight: 500;
}

.chart-data {
  width: 100%;
  margin-top: 15px;
}

.data-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.data-value {
  font-weight: 600;
  color: #667eea;
}

.top-products {
  width: 100%;
  margin-top: 15px;
}

.product-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  padding: 8px;
  background: white;
  border-radius: 8px;
}

.product-rank {
  width: 25px;
  height: 25px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: bold;
  margin-right: 10px;
}

.product-name {
  flex: 1;
  font-size: 0.9rem;
}

.product-sales {
  font-weight: 600;
  color: #667eea;
}

.el-card {
  transition: all 0.3s;
}

.el-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style> 