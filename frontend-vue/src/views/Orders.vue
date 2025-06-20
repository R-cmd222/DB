<template>
  <el-card>
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span>订单管理</span>
        <el-button @click="loadOrders" :loading="loading" size="small">
          刷新
        </el-button>
      </div>
    </template>
    
    <el-table :data="orders" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="订单ID" width="80"/>
      <el-table-column prop="customer_name" label="客户名" width="120"/>
      <el-table-column prop="total" label="总价" width="100">
        <template #default="scope">
          ¥{{ scope.row.total.toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="下单时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="商品数量" width="100">
        <template #default="scope">
          {{ scope.row.items ? scope.row.items.length : 0 }} 件
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button size="small" @click="viewOrderDetail(scope.row)">
            查看详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 订单详情对话框 -->
    <el-dialog v-model="showDetail" title="订单详情" width="600px">
      <div v-if="selectedOrder">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单ID">{{ selectedOrder.id }}</el-descriptions-item>
          <el-descriptions-item label="客户名">{{ selectedOrder.customer_name }}</el-descriptions-item>
          <el-descriptions-item label="总价">¥{{ selectedOrder.total.toFixed(2) }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ formatDate(selectedOrder.created_at) }}</el-descriptions-item>
        </el-descriptions>
        
        <div style="margin-top: 20px;">
          <h4>商品清单</h4>
          <el-table :data="selectedOrder.items || []" border>
            <el-table-column prop="name" label="商品名称"/>
            <el-table-column prop="quantity" label="数量" width="80"/>
            <el-table-column prop="price" label="单价" width="100">
              <template #default="scope">
                ¥{{ scope.row.price.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column label="小计" width="100">
              <template #default="scope">
                ¥{{ (scope.row.price * scope.row.quantity).toFixed(2) }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { orderAPI } from '../api'

const orders = ref([])
const loading = ref(false)
const showDetail = ref(false)
const selectedOrder = ref(null)

function formatDate(dateString) {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

async function loadOrders() {
  loading.value = true
  try {
    const response = await orderAPI.getOrders()
    orders.value = response.data
    ElMessage.success('订单列表加载成功')
  } catch (error) {
    console.error('加载订单失败:', error)
    ElMessage.error('加载订单失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

function viewOrderDetail(order) {
  selectedOrder.value = order
  showDetail.value = true
}

onMounted(loadOrders)
</script> 