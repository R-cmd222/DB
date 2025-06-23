<template>
  <el-card>
    <template #header>
      <span>销售报表</span>
    </template>
    <div style="margin-bottom: 20px;">
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
      <el-button type="primary" @click="loadReport" :loading="loading" style="margin-left: 20px;">生成报表</el-button>
    </div>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">总销售额</div>
          <div class="stat-value">¥{{ stats.totalSales.toFixed(2) }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">订单数量</div>
          <div class="stat-value">{{ stats.orderCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">平均订单金额</div>
          <div class="stat-value">¥{{ stats.avgOrderValue.toFixed(2) }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">新增客户</div>
          <div class="stat-value">{{ stats.newCustomers }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-card style="margin-top: 20px;">
      <template #header>
        <span>销售趋势</span>
      </template>
      <div ref="chartRef" style="height: 400px;"></div>
    </el-card>
  </el-card>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const dateRange = ref([])
const loading = ref(false)
const stats = ref({
  totalSales: 0,
  orderCount: 0,
  avgOrderValue: 0,
  newCustomers: 0
})
const chartRef = ref()

function loadReport() {
  loading.value = true
  setTimeout(() => {
    stats.value = {
      totalSales: 125680.5,
      orderCount: 1256,
      avgOrderValue: 100.05,
      newCustomers: 89
    }
    nextTick(() => {
      renderChart()
    })
    loading.value = false
    ElMessage.success('报表生成成功')
  }, 800)
}

function renderChart() {
  if (!chartRef.value) return
  const chart = echarts.init(chartRef.value)
  const option = {
    title: { text: '销售趋势' },
    tooltip: { trigger: 'axis' },
    legend: { data: ['销售额', '订单数'] },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月']
    },
    yAxis: [
      { type: 'value', name: '销售额' },
      { type: 'value', name: '订单数' }
    ],
    series: [
      {
        name: '销售额',
        type: 'line',
        data: [12000, 15000, 18000, 16000, 20000, 25000]
      },
      {
        name: '订单数',
        type: 'bar',
        yAxisIndex: 1,
        data: [120, 150, 180, 160, 200, 250]
      }
    ]
  }
  chart.setOption(option)
}

onMounted(() => {
  // 默认最近30天
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 30)
  dateRange.value = [start.toISOString().split('T')[0], end.toISOString().split('T')[0]]
  loadReport()
})
</script>

<style scoped>
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
</style> 