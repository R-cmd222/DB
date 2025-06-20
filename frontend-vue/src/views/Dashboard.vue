<template>
  <div>
    <el-row :gutter="20" v-loading="loading">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">商品总数</div>
          <div class="stat-value">{{ stats.total_products }}</div>
          <div class="stat-icon">📦</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">订单总数</div>
          <div class="stat-value">{{ stats.total_orders }}</div>
          <div class="stat-icon">📋</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">库存总量</div>
          <div class="stat-value">{{ stats.total_stock }}</div>
          <div class="stat-icon">📊</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">库存预警</div>
          <div class="stat-value" :class="{ 'warning': stats.low_stock_products > 0 }">
            {{ stats.low_stock_products }}
          </div>
          <div class="stat-icon">⚠️</div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card style="margin-top: 20px;">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>系统状态</span>
          <el-button @click="loadStats" :loading="loading" size="small">
            刷新
          </el-button>
        </div>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="API 状态">
          <el-tag :type="apiStatus === 'healthy' ? 'success' : 'danger'">
            {{ apiStatus === 'healthy' ? '正常' : '异常' }}
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
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { statsAPI, systemAPI } from '../api'

const stats = ref({ 
  total_products: 0, 
  total_orders: 0, 
  total_stock: 0, 
  low_stock_products: 0 
})
const loading = ref(false)
const apiStatus = ref('unknown')
const lastUpdate = ref('')

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
    stats.value = response.data
    lastUpdate.value = new Date().toLocaleString()
    
    ElMessage.success('数据加载成功')
  } catch (error) {
    console.error('加载统计信息失败:', error)
    ElMessage.error('加载统计信息失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

onMounted(loadStats)
</script>

<style scoped>
.stat-card {
  text-align: center;
  position: relative;
  overflow: hidden;
}

.stat-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 2.5em;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 10px;
}

.stat-value.warning {
  color: #E6A23C;
}

.stat-icon {
  font-size: 2em;
  opacity: 0.3;
  position: absolute;
  top: 10px;
  right: 10px;
}

.el-card {
  transition: all 0.3s;
}

.el-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style> 