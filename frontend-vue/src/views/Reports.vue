<template>
  <div class="reports-container">
    <!-- 报表类型选择 -->
    <el-card style="margin-bottom: 20px;">
      <template #header>
        <span>报表类型</span>
      </template>
      <el-radio-group v-model="currentReport" @change="loadReport">
        <el-radio-button label="sales">销售报表</el-radio-button>
        <el-radio-button label="inventory">库存报表</el-radio-button>
        <el-radio-button label="customer">客户分析</el-radio-button>
        <el-radio-button label="product">商品分析</el-radio-button>
      </el-radio-group>
    </el-card>
    
    <!-- 时间范围选择 -->
    <el-card style="margin-bottom: 20px;">
      <template #header>
        <span>时间范围</span>
      </template>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="loadReport"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="timeUnit" @change="loadReport">
            <el-option label="按天" value="day" />
            <el-option label="按周" value="week" />
            <el-option label="按月" value="month" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="loadReport" :loading="loading">
            生成报表
          </el-button>
        </el-col>
        <el-col :span="4">
          <el-button @click="exportReport">
            导出报表
          </el-button>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 销售报表 -->
    <div v-if="currentReport === 'sales'">
      <el-row :gutter="20">
        <!-- 销售统计卡片 -->
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">总销售额</div>
            <div class="stat-value">¥{{ salesStats.totalSales.toFixed(2) }}</div>
            <div class="stat-trend" :class="{ 'up': salesStats.salesGrowth > 0, 'down': salesStats.salesGrowth < 0 }">
              {{ salesStats.salesGrowth > 0 ? '+' : '' }}{{ salesStats.salesGrowth.toFixed(1) }}%
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">订单数量</div>
            <div class="stat-value">{{ salesStats.orderCount }}</div>
            <div class="stat-trend" :class="{ 'up': salesStats.orderGrowth > 0, 'down': salesStats.orderGrowth < 0 }">
              {{ salesStats.orderGrowth > 0 ? '+' : '' }}{{ salesStats.orderGrowth.toFixed(1) }}%
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">平均订单金额</div>
            <div class="stat-value">¥{{ salesStats.avgOrderValue.toFixed(2) }}</div>
            <div class="stat-trend" :class="{ 'up': salesStats.avgOrderGrowth > 0, 'down': salesStats.avgOrderGrowth < 0 }">
              {{ salesStats.avgOrderGrowth > 0 ? '+' : '' }}{{ salesStats.avgOrderGrowth.toFixed(1) }}%
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">新增客户</div>
            <div class="stat-value">{{ salesStats.newCustomers }}</div>
            <div class="stat-trend" :class="{ 'up': salesStats.customerGrowth > 0, 'down': salesStats.customerGrowth < 0 }">
              {{ salesStats.customerGrowth > 0 ? '+' : '' }}{{ salesStats.customerGrowth.toFixed(1) }}%
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 销售趋势图 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>销售趋势</span>
        </template>
        <div ref="salesChartRef" style="height: 400px;"></div>
      </el-card>
      
      <!-- 热销商品 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>热销商品 TOP 10</span>
        </template>
        <el-table :data="salesStats.topProducts" style="width: 100%">
          <el-table-column prop="rank" label="排名" width="80" />
          <el-table-column prop="name" label="商品名称" />
          <el-table-column prop="sales" label="销量" width="100" />
          <el-table-column prop="revenue" label="销售额" width="120">
            <template #default="scope">
              ¥{{ scope.row.revenue.toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column prop="percentage" label="占比" width="100">
            <template #default="scope">
              {{ scope.row.percentage.toFixed(1) }}%
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    
    <!-- 库存报表 -->
    <div v-if="currentReport === 'inventory'">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">总库存价值</div>
            <div class="stat-value">¥{{ inventoryStats.totalValue.toFixed(2) }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">商品种类</div>
            <div class="stat-value">{{ inventoryStats.productCount }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">库存预警</div>
            <div class="stat-value warning">{{ inventoryStats.lowStockCount }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">周转率</div>
            <div class="stat-value">{{ inventoryStats.turnoverRate.toFixed(2) }}</div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 库存分布图 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>库存分布</span>
        </template>
        <div ref="inventoryChartRef" style="height: 400px;"></div>
      </el-card>
      
      <!-- 库存预警列表 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>库存预警</span>
        </template>
        <el-table :data="inventoryStats.lowStockProducts" style="width: 100%">
          <el-table-column prop="name" label="商品名称" />
          <el-table-column prop="currentStock" label="当前库存" width="100" />
          <el-table-column prop="minStock" label="最低库存" width="100" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'critical' ? 'danger' : 'warning'">
                {{ scope.row.status === 'critical' ? '严重不足' : '库存不足' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button size="small" @click="replenishStock(scope.row)">
                补货
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    
    <!-- 客户分析 -->
    <div v-if="currentReport === 'customer'">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">总客户数</div>
            <div class="stat-value">{{ customerStats.totalCustomers }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">活跃客户</div>
            <div class="stat-value">{{ customerStats.activeCustomers }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">VIP客户</div>
            <div class="stat-value">{{ customerStats.vipCustomers }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">客户满意度</div>
            <div class="stat-value">{{ customerStats.satisfaction.toFixed(1) }}%</div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 客户等级分布 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>客户等级分布</span>
        </template>
        <div ref="customerChartRef" style="height: 400px;"></div>
      </el-card>
      
      <!-- 客户消费排行 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>客户消费排行 TOP 10</span>
        </template>
        <el-table :data="customerStats.topCustomers" style="width: 100%">
          <el-table-column prop="rank" label="排名" width="80" />
          <el-table-column prop="name" label="客户姓名" />
          <el-table-column prop="level" label="等级" width="100">
            <template #default="scope">
              <el-tag :type="getCustomerLevelType(scope.row.level)">
                {{ getCustomerLevelText(scope.row.level) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="totalSpent" label="累计消费" width="120">
            <template #default="scope">
              ¥{{ scope.row.totalSpent.toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column prop="orderCount" label="订单数" width="100" />
          <el-table-column prop="lastOrderDate" label="最后购买" width="150">
            <template #default="scope">
              {{ formatDate(scope.row.lastOrderDate) }}
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    
    <!-- 商品分析 -->
    <div v-if="currentReport === 'product'">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">商品总数</div>
            <div class="stat-value">{{ productStats.totalProducts }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">在售商品</div>
            <div class="stat-value">{{ productStats.activeProducts }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">平均价格</div>
            <div class="stat-value">¥{{ productStats.avgPrice.toFixed(2) }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-title">商品种类</div>
            <div class="stat-value">{{ productStats.categoryCount }}</div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 商品分类分析 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>商品分类分析</span>
        </template>
        <div ref="productChartRef" style="height: 400px;"></div>
      </el-card>
      
      <!-- 商品价格分布 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>商品价格分布</span>
        </template>
        <div ref="priceChartRef" style="height: 400px;"></div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { reportAPI } from '../api'

const currentReport = ref('sales')
const dateRange = ref([])
const timeUnit = ref('day')
const loading = ref(false)

const salesStats = ref({
  totalSales: 0,
  orderCount: 0,
  avgOrderValue: 0,
  newCustomers: 0,
  salesGrowth: 0,
  orderGrowth: 0,
  avgOrderGrowth: 0,
  customerGrowth: 0,
  trend: [],
  topProducts: []
})
const inventoryStats = ref({
  totalValue: 0,
  productCount: 0,
  lowStockCount: 0,
  turnoverRate: 0,
  lowStockProducts: []
})
const customerStats = ref({
  totalCustomers: 0,
  newCustomers: 0,
  activeCustomers: 0,
  vipCustomers: 0,
  satisfaction: 100
})
const productStats = ref({
  totalProducts: 0,
  activeProducts: 0,
  avgPrice: 0,
  categoryCount: 0,
  topProducts: []
})

// 图表引用
const salesChartRef = ref()
const inventoryChartRef = ref()
const customerChartRef = ref()
const productChartRef = ref()
const priceChartRef = ref()

// 方法
function formatDate(dateString) {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

function getCustomerLevelType(level) {
  const typeMap = {
    'normal': 'info',
    'vip': 'warning',
    'diamond': 'success'
  }
  return typeMap[level] || 'info'
}

function getCustomerLevelText(level) {
  const textMap = {
    'normal': '普通客户',
    'vip': 'VIP客户',
    'diamond': '钻石客户'
  }
  return textMap[level] || level
}

function loadReport() {
  loading.value = true
  if (currentReport.value === 'sales') {
    const [start, end] = dateRange.value.length === 2 ? dateRange.value : [null, null]
    reportAPI.getSalesReport({ start, end, unit: timeUnit.value }).then(res => {
      Object.assign(salesStats.value, res.data)
      nextTick(renderSalesChart)
      loading.value = false
    }).catch(() => loading.value = false)
  } else if (currentReport.value === 'inventory') {
    reportAPI.getInventoryReport().then(res => {
      Object.assign(inventoryStats.value, res.data)
      nextTick(renderInventoryChart)
      loading.value = false
    }).catch(() => loading.value = false)
  } else if (currentReport.value === 'customer') {
    const [start, end] = dateRange.value.length === 2 ? dateRange.value : [null, null]
    reportAPI.getCustomerReport({ start, end }).then(res => {
      Object.assign(customerStats.value, res.data)
      loading.value = false
    }).catch(() => loading.value = false)
  } else if (currentReport.value === 'product') {
    reportAPI.getProductReport().then(res => {
      Object.assign(productStats.value, res.data)
      loading.value = false
    }).catch(() => loading.value = false)
  }
}

function renderSalesChart() {
  // 仅示例，实际可根据 salesStats.value.trend 渲染
}
function renderInventoryChart() {
  // 仅示例，实际可根据 inventoryStats.value 渲染
}

function replenishStock(product) {
  ElMessage.info(`为 ${product.name} 补货`)
}

function exportReport() {
  ElMessage.success('报表导出成功')
}

// 生命周期
onMounted(() => {
  // 默认近30天
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 30)
  dateRange.value = [start.toISOString().split('T')[0], end.toISOString().split('T')[0]]
  loadReport()
})
</script>

<style scoped>
.reports-container {
  padding: 20px;
}

.stat-card {
  text-align: center;
  position: relative;
}

.stat-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 2em;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-value.warning {
  color: #E6A23C;
}

.stat-trend {
  font-size: 12px;
  font-weight: bold;
}

.stat-trend.up {
  color: #67C23A;
}

.stat-trend.down {
  color: #F56C6C;
}

.el-card {
  transition: all 0.3s;
}

.el-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style> 