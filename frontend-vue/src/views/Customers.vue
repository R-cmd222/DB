<template>
  <el-card>
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span>客户管理</span>
        <div>
          <el-button type="primary" @click="showAdd = true">
            添加客户
          </el-button>
          <el-button @click="loadCustomers" :loading="loading">
            刷新
          </el-button>
        </div>
      </div>
    </template>
    
    <!-- 搜索栏 -->
    <div style="margin-bottom: 20px;">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input 
            v-model="searchForm.name" 
            placeholder="搜索客户姓名"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-input 
            v-model="searchForm.phone" 
            placeholder="搜索客户电话"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.level" placeholder="客户等级" clearable>
            <el-option label="普通客户" value="normal" />
            <el-option label="VIP客户" value="vip" />
            <el-option label="钻石客户" value="diamond" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-col>
      </el-row>
    </div>
    
    <!-- 客户列表 -->
    <el-table :data="filteredCustomers" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80"/>
      <el-table-column prop="name" label="客户姓名" width="120"/>
      <el-table-column prop="phone" label="电话" width="150"/>
      <el-table-column prop="email" label="邮箱" width="200"/>
      <el-table-column prop="level" label="等级" width="100">
        <template #default="scope">
          <el-tag :type="getLevelType(scope.row.level)">
            {{ getLevelText(scope.row.level) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="totalSpent" label="累计消费" width="120">
        <template #default="scope">
          ¥{{ Number(scope.row.totalSpent ?? 0).toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column prop="orderCount" label="订单数" width="100"/>
      <el-table-column prop="lastOrderDate" label="最后购买" width="150">
        <template #default="scope">
          {{ formatDate(scope.row.lastOrderDate) }}
        </template>
      </el-table-column>
      <el-table-column prop="createdAt" label="注册时间" width="150">
        <template #default="scope">
          {{ formatDate(scope.row.createdAt) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <div style="display: flex; gap: 10px; justify-content: center;">
            <el-tooltip content="编辑" placement="top">
              <el-button size="small" icon="el-icon-edit" @click="edit(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip content="详情" placement="top">
              <el-button size="small" type="info" icon="el-icon-document" @click="viewDetails(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip content="删除" placement="top">
              <el-button size="small" type="danger" icon="el-icon-delete" @click="deleteCustomer(scope.row.id)"></el-button>
            </el-tooltip>
          </div>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 添加/编辑客户对话框 -->
    <el-dialog v-model="showAdd" :title="isEdit ? '编辑客户' : '添加客户'" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="客户姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入客户姓名"/>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入客户电话"/>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入客户邮箱"/>
        </el-form-item>
        <el-form-item label="客户等级" prop="level">
          <el-select v-model="form.level" placeholder="请选择客户等级">
            <el-option label="普通客户" value="normal" />
            <el-option label="VIP客户" value="vip" />
            <el-option label="钻石客户" value="diamond" />
          </el-select>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address" type="textarea" placeholder="请输入客户地址"/>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.notes" type="textarea" placeholder="请输入备注信息"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAdd = false">取消</el-button>
        <el-button type="primary" @click="saveCustomer" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 客户详情对话框 -->
    <el-dialog v-model="showDetails" title="客户详情" width="800px">
      <div v-if="selectedCustomer">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="客户ID">{{ selectedCustomer.id }}</el-descriptions-item>
          <el-descriptions-item label="客户姓名">{{ selectedCustomer.name }}</el-descriptions-item>
          <el-descriptions-item label="电话">{{ selectedCustomer.phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ selectedCustomer.email }}</el-descriptions-item>
          <el-descriptions-item label="客户等级">
            <el-tag :type="getLevelType(selectedCustomer.level)">
              {{ getLevelText(selectedCustomer.level) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ formatDate(selectedCustomer.createdAt) }}</el-descriptions-item>
          <el-descriptions-item label="累计消费">¥{{ Number(selectedCustomer.totalSpent ?? 0).toFixed(2) }}</el-descriptions-item>
          <el-descriptions-item label="订单数量">{{ selectedCustomer.orderCount }}</el-descriptions-item>
          <el-descriptions-item label="最后购买">{{ formatDate(selectedCustomer.lastOrderDate) }}</el-descriptions-item>
          <el-descriptions-item label="地址" :span="2">{{ selectedCustomer.address || '未填写' }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ selectedCustomer.notes || '无' }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 订单历史 -->
        <div style="margin-top: 20px;">
          <h4>订单历史</h4>
          <el-table :data="customerOrders" border>
            <el-table-column prop="id" label="订单ID" width="100"/>
            <el-table-column prop="total" label="订单金额" width="120">
              <template #default="scope">
                ¥{{ Number(scope.row.total ?? 0).toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getOrderStatusType(scope.row.status)">
                  {{ getOrderStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createdAt" label="下单时间" width="180">
              <template #default="scope">
                {{ formatDate(scope.row.createdAt) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-button size="small" @click="viewOrder(scope.row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import api, { billAPI } from '../api'

// 响应式数据
const customers = ref([])
const loading = ref(false)
const submitting = ref(false)
const showAdd = ref(false)
const showDetails = ref(false)
const isEdit = ref(false)
const selectedCustomer = ref(null)
const customerOrders = ref([])
const formRef = ref()

// 搜索表单
const searchForm = ref({
  name: '',
  phone: '',
  level: ''
})

// 客户表单
const form = ref({
  id: null,
  name: '',
  phone: '',
  email: '',
  level: 'normal',
  address: '',
  notes: ''
})

const rules = {
  name: [
    { required: true, message: '请输入客户姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入客户电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  level: [
    { required: true, message: '请选择客户等级', trigger: 'change' }
  ]
}

// 计算属性
const filteredCustomers = computed(() => {
  let result = Array.isArray(customers.value) ? customers.value : []
  if (searchForm.value.name) {
    result = result.filter(customer => 
      (customer.name || '').toLowerCase().includes(searchForm.value.name.toLowerCase())
    )
  }
  if (searchForm.value.phone) {
    result = result.filter(customer => 
      (customer.phone || '').includes(searchForm.value.phone)
    )
  }
  if (searchForm.value.level) {
    result = result.filter(customer => 
      customer.level === searchForm.value.level
    )
  }
  return Array.isArray(result) ? result : []
})

// 方法
function formatDate(dateString) {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

function getLevelType(level) {
  const typeMap = {
    'normal': 'info',
    'vip': 'warning',
    'diamond': 'success'
  }
  return typeMap[level] || 'info'
}

function getLevelText(level) {
  const textMap = {
    'normal': '普通客户',
    'vip': 'VIP客户',
    'diamond': '钻石客户'
  }
  return textMap[level] || level
}

function getOrderStatusType(status) {
  const typeMap = {
    'pending': 'warning',
    'completed': 'success',
    'cancelled': 'danger'
  }
  return typeMap[status] || 'info'
}

function getOrderStatusText(status) {
  const textMap = {
    'pending': '待处理',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return textMap[status] || status
}

async function loadCustomers() {
  loading.value = true
  try {
    const res = await api.get('/guests')
    customers.value = Array.isArray(res.data) ? res.data : []
    ElMessage.success('客户列表加载成功')
  } catch (error) {
    console.error('加载客户失败:', error)
    customers.value = []
    ElMessage.error('加载客户失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  // 搜索功能已通过计算属性实现
}

function resetSearch() {
  searchForm.value = {
    name: '',
    phone: '',
    level: ''
  }
}

function edit(customer) {
  isEdit.value = true
  Object.assign(form.value, customer)
  showAdd.value = true
}

function viewDetails(customer) {
  selectedCustomer.value = customer
  showDetails.value = true
  loadCustomerOrders(customer.id)
}

async function loadCustomerOrders(customerId) {
  try {
    // 获取所有订单，前端过滤出该客户的订单
    const res = await billAPI.getBills()
    customerOrders.value = res.data
      .filter(order => order.GuestID === customerId)
      .map(order => ({
        id: order.BillID,
        total: order.TotalAmount,
        status: order.Status,
        createdAt: order.BillDate
      }))
  } catch (error) {
    console.error('加载订单失败:', error)
    ElMessage.error('加载订单失败')
  }
}

function viewOrder(order) {
  // 这里可以跳转到订单详情页面
  ElMessage.info(`查看订单 ${order.id}`)
}

async function saveCustomer() {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
  } catch (error) {
    return
  }
  
  submitting.value = true
  try {
    if (isEdit.value) {
      // 更新客户
      // await customerAPI.updateCustomer(form.value.id, form.value)
      const index = customers.value.findIndex(c => c.id === form.value.id)
      if (index !== -1) {
        customers.value[index] = { ...customers.value[index], ...form.value }
      }
      ElMessage.success('客户更新成功')
    } else {
      // 添加客户
      const newCustomer = {
        ...form.value,
        id: Date.now(),
        totalSpent: 0,
        orderCount: 0,
        lastOrderDate: null,
        createdAt: new Date().toISOString()
      }
      // await customerAPI.createCustomer(newCustomer)
      customers.value.unshift(newCustomer)
      ElMessage.success('客户添加成功')
    }
    
    showAdd.value = false
    resetForm()
  } catch (error) {
    console.error('保存客户失败:', error)
    ElMessage.error('保存客户失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

async function deleteCustomer(id) {
  try {
    await ElMessageBox.confirm('确定要删除这个客户吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // await customerAPI.deleteCustomer(id)
    const index = customers.value.findIndex(c => c.id === id)
    if (index !== -1) {
      customers.value.splice(index, 1)
    }
    
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

function resetForm() {
  Object.assign(form.value, {
    id: null,
    name: '',
    phone: '',
    email: '',
    level: 'normal',
    address: '',
    notes: ''
  })
  isEdit.value = false
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

onMounted(loadCustomers)
</script>

<style scoped>
.el-table .el-button {
  margin-right: 5px;
}
</style> 