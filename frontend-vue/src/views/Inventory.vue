<template>
  <el-card>
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span>库存管理</span>
        <div>
          <el-button @click="loadProducts" :loading="loading" size="small">
            刷新
          </el-button>
          <el-button type="primary" @click="showStockAdjust = true" size="small">
            调整库存
          </el-button>
        </div>
      </div>
    </template>
    
    <el-table :data="products" style="width: 100%" v-loading="loading">
      <el-table-column prop="ProductID" label="ID" width="60"/>
      <el-table-column prop="Name" label="商品名称"/>
      <el-table-column prop="Stock" label="库存" width="100">
        <template #default="scope">
          <span :class="{ 'low-stock': scope.row.Stock < 10 }">
            {{ scope.row.Stock }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="CategoryID" label="分类" width="120"/>
      <el-table-column label="状态" width="120">
        <template #default="scope">
          <el-tag v-if="scope.row.Stock === 0" type="danger">缺货</el-tag>
          <el-tag v-else-if="scope.row.Stock < 10" type="warning">库存不足</el-tag>
          <el-tag v-else type="success">库存充足</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button size="small" @click="adjustStock(scope.row)">
            调整库存
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 库存调整对话框 -->
    <el-dialog v-model="showStockAdjust" title="调整库存" width="500px">
      <el-form :model="stockForm" :rules="stockRules" ref="stockFormRef" label-width="100px">
        <el-form-item label="商品名称">
          <el-input v-model="stockForm.name" disabled/>
        </el-form-item>
        <el-form-item label="当前库存">
          <el-input v-model="stockForm.currentStock" disabled/>
        </el-form-item>
        <el-form-item label="调整方式" prop="adjustType">
          <el-radio-group v-model="stockForm.adjustType">
            <el-radio label="set">设置为</el-radio>
            <el-radio label="add">增加</el-radio>
            <el-radio label="subtract">减少</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="数量" prop="amount">
          <el-input v-model="stockForm.amount" type="number" placeholder="请输入数量"/>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="stockForm.remark" type="textarea" placeholder="请输入调整原因"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showStockAdjust = false">取消</el-button>
        <el-button type="primary" @click="confirmStockAdjust" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { productAPI } from '../api'

const products = ref([])
const loading = ref(false)
const submitting = ref(false)
const showStockAdjust = ref(false)
const stockFormRef = ref()

const stockForm = ref({
  id: null,
  name: '',
  currentStock: 0,
  adjustType: 'set',
  amount: 0,
  remark: ''
})

const stockRules = {
  adjustType: [{ required: true, message: '请选择调整方式', trigger: 'change' }],
  amount: [{ required: true, message: '请输入数量', trigger: 'blur' }],
  remark: [{ required: true, message: '请输入调整原因', trigger: 'blur' }]
}

async function loadProducts() {
  loading.value = true
  try {
    const response = await productAPI.getProducts()
    products.value = response.data
    ElMessage.success('库存信息加载成功')
  } catch (error) {
    console.error('加载库存失败:', error)
    ElMessage.error('加载库存失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

function adjustStock(product) {
  stockForm.value = {
    id: product.ProductID,
    name: product.Name,
    currentStock: product.Stock,
    adjustType: 'set',
    amount: product.Stock,
    remark: ''
  }
  showStockAdjust.value = true
}

async function confirmStockAdjust() {
  if (!stockFormRef.value) return
  
  try {
    await stockFormRef.value.validate()
  } catch (error) {
    return
  }
  
  submitting.value = true
  try {
    let newStock = stockForm.value.currentStock
    
    switch (stockForm.value.adjustType) {
      case 'set':
        newStock = parseInt(stockForm.value.amount)
        break
      case 'add':
        newStock += parseInt(stockForm.value.amount)
        break
      case 'subtract':
        newStock -= parseInt(stockForm.value.amount)
        break
    }
    
    if (newStock < 0) {
      ElMessage.error('库存不能为负数')
      return
    }
    
    // 更新商品库存
    const product = products.value.find(p => p.id === stockForm.value.id)
    if (product) {
      product.Stock = newStock
      await productAPI.updateProduct(stockForm.value.id, product)
      
      ElMessage.success('库存调整成功')
      showStockAdjust.value = false
      await loadProducts()
    }
  } catch (error) {
    console.error('调整库存失败:', error)
    ElMessage.error('调整库存失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

onMounted(loadProducts)
</script>

<style scoped>
.low-stock {
  color: #E6A23C;
  font-weight: bold;
}
</style> 