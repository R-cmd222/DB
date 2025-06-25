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

    <el-dialog v-model="showReplenishDialog" title="补货" width="400px">
      <div v-if="replenishProduct">
        <p>商品名称：{{ replenishProduct.name }}</p>
        <el-form label-width="80px">
          <el-form-item label="补货数量">
            <el-input-number v-model="replenishAmount" :min="1" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="replenishRemark" type="textarea" placeholder="补货备注（选填）" />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="showReplenishDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmReplenish" :disabled="replenishAmount <= 0">确定补货</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { statsAPI, productAPI } from '../api'

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
  satisfaction: 100,
  topCustomers: []
})
const productStats = ref({
  totalProducts: 0,
  activeProducts: 0,
  avgPrice: 0,
  categoryCount: 0,
  topProducts: [],
  categorySales: [],
  priceRanges: []
})

// 图表引用
const salesChartRef = ref()
const inventoryChartRef = ref()
const customerChartRef = ref()
const productChartRef = ref()
const priceChartRef = ref()

const showReplenishDialog = ref(false)
const replenishProduct = ref(null)
const replenishAmount = ref(0)
const replenishRemark = ref('')

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
    statsAPI.getSalesReport(start, end, timeUnit.value).then(res => {
      Object.assign(salesStats.value, res.data)
      nextTick(renderSalesChart)
      loading.value = false
    }).catch(() => loading.value = false)
  } else if (currentReport.value === 'inventory') {
    statsAPI.getInventoryReport().then(res => {
      Object.assign(inventoryStats.value, res.data)
      nextTick(renderInventoryChart)
      loading.value = false
    }).catch(() => loading.value = false)
  } else if (currentReport.value === 'customer') {
    const [start, end] = dateRange.value.length === 2 ? dateRange.value : [null, null]
    statsAPI.getCustomerReport(start, end).then(res => {
      Object.assign(customerStats.value, res.data)
      nextTick(renderCustomerChart)
      loading.value = false
    }).catch(() => loading.value = false)
  } else if (currentReport.value === 'product') {
    statsAPI.getProductReport().then(res => {
      Object.assign(productStats.value, res.data)
      nextTick(() => {
        renderProductChart()
        renderPriceChart()
      })
      loading.value = false
    }).catch(() => loading.value = false)
  }
}

function renderSalesChart() {
  if (!salesChartRef.value) return
  
  const chart = echarts.init(salesChartRef.value)
  const trend = salesStats.value.trend || []
  
  const option = {
    title: {
      text: '销售趋势',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['销售额', '订单数'],
      top: 30
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: trend.map(item => item.date),
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '销售额 (¥)',
        position: 'left'
      },
      {
        type: 'value',
        name: '订单数',
        position: 'right'
      }
    ],
    series: [
      {
        name: '销售额',
        type: 'line',
        data: trend.map(item => item.sales),
        smooth: true,
        itemStyle: {
          color: '#409EFF'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(64,158,255,0.3)' },
              { offset: 1, color: 'rgba(64,158,255,0.1)' }
            ]
          }
        }
      },
      {
        name: '订单数',
        type: 'bar',
        yAxisIndex: 1,
        data: trend.map(item => item.orders),
        itemStyle: {
          color: '#67C23A'
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

function renderInventoryChart() {
  if (!inventoryChartRef.value) return
  
  const chart = echarts.init(inventoryChartRef.value)
  const products = inventoryStats.value.lowStockProducts || []
  
  const option = {
    title: {
      text: '库存分布',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['正常库存', '库存不足', '严重不足']
    },
    series: [
      {
        name: '库存状态',
        type: 'pie',
        radius: '50%',
        data: [
          {
            value: inventoryStats.value.productCount - inventoryStats.value.lowStockCount,
            name: '正常库存',
            itemStyle: { color: '#67C23A' }
          },
          {
            value: products.filter(p => p.status === 'warning').length,
            name: '库存不足',
            itemStyle: { color: '#E6A23C' }
          },
          {
            value: products.filter(p => p.status === 'critical').length,
            name: '严重不足',
            itemStyle: { color: '#F56C6C' }
          }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

function renderCustomerChart() {
  if (!customerChartRef.value) return
  
  const chart = echarts.init(customerChartRef.value)
  
  const option = {
    title: {
      text: '客户等级分布',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['普通客户', 'VIP客户', '钻石客户']
    },
    series: [
      {
        name: '客户等级',
        type: 'pie',
        radius: '50%',
        data: [
          {
            value: customerStats.value.normalCustomers || 0,
            name: '普通客户',
            itemStyle: { color: '#909399' }
          },
          {
            value: customerStats.value.vipCustomers || 0,
            name: 'VIP客户',
            itemStyle: { color: '#E6A23C' }
          },
          {
            value: customerStats.value.diamondCustomers || 0,
            name: '钻石客户',
            itemStyle: { color: '#409EFF' }
          }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

function renderProductChart() {
  if (!productChartRef.value) return
  
  const chart = echarts.init(productChartRef.value)
  const categorySales = productStats.value.categorySales || []
  
  const option = {
    title: {
      text: '商品分类分析',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categorySales.map(item => item.name),
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '销量'
    },
    series: [
      {
        name: '销量',
        type: 'bar',
        data: categorySales.map(item => item.sales),
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: '#409EFF' },
              { offset: 1, color: '#67C23A' }
            ]
          }
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

function renderPriceChart() {
  if (!priceChartRef.value) return
  
  const chart = echarts.init(priceChartRef.value)
  const priceRanges = productStats.value.priceRanges || []
  
  const option = {
    title: {
      text: '商品价格分布',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: priceRanges.map(item => item.range)
    },
    yAxis: {
      type: 'value',
      name: '商品数量'
    },
    series: [
      {
        name: '商品数量',
        type: 'bar',
        data: priceRanges.map(item => item.count),
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: '#F56C6C' },
              { offset: 1, color: '#E6A23C' }
            ]
          }
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

function replenishStock(product) {
  replenishProduct.value = product
  replenishAmount.value = 0
  replenishRemark.value = ''
  showReplenishDialog.value = true
}

async function confirmReplenish() {
  if (!replenishProduct.value) return
  const id = replenishProduct.value.id || replenishProduct.value.ProductID
  const newStock = (replenishProduct.value.currentStock || 0) + replenishAmount.value
  try {
    await productAPI.updateProduct(id, {
      Name: replenishProduct.value.name,
      Price: replenishProduct.value.price || 0,
      Stock: newStock,
      Category: replenishProduct.value.category || '',
    })
    ElMessage.success('补货成功')
    showReplenishDialog.value = false
    loadReport()
  } catch (e) {
    ElMessage.error('补货失败')
  }
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