<template>
  <el-card>
    <div style="margin-bottom: 20px; display: flex; gap: 10px;">
      <el-button type="primary" @click="showAdd = true" :loading="loading">
        <i class="fas fa-plus"></i> 添加商品
      </el-button>
      <el-button @click="loadProducts" :loading="loading">
        <i class="fas fa-sync-alt"></i> 刷新
      </el-button>
    </div>
    
    <el-table :data="products" style="width: 100%" v-loading="loading">
      <el-table-column prop="ProductID" label="ID" width="60"/>
      <el-table-column label="图片" width="60">
        <template #default>
          <i class="fas fa-box fa-lg" style="color:#667eea;"></i>
        </template>
      </el-table-column>
      <el-table-column prop="Name" label="商品名称"/>
      <el-table-column prop="Price" label="价格">
        <template #default="scope">
          ¥{{ scope.row.Price ? scope.row.Price.toFixed(2) : '0.00' }}
        </template>
      </el-table-column>
      <el-table-column prop="Stock" label="库存">
        <template #default="scope">
          <el-tag 
            :type="scope.row.Stock === 0 ? 'info' : (scope.row.Stock < 10 ? 'danger' : 'success')"
            :effect="scope.row.Stock === 0 ? 'plain' : 'light'"
          >
            {{ scope.row.Stock === 0 ? '已下架' : scope.row.Stock }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="Category" label="分类"/>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="edit(scope.row)">
            <i class="fas fa-edit"></i> 编辑
          </el-button>
          <el-button 
            size="small" 
            :type="scope.row.Stock === 0 ? 'success' : 'danger'"
            @click="scope.row.Stock === 0 ? reStock(scope.row) : del(scope.row.ProductID)"
          >
            <i :class="scope.row.Stock === 0 ? 'fas fa-undo' : 'fas fa-trash'"></i> 
            {{ scope.row.Stock === 0 ? '重新上架' : '删除' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-dialog v-model="showAdd" title="添加/编辑商品" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="名称" prop="Name">
          <el-input v-model="form.Name" placeholder="请输入商品名称"/>
        </el-form-item>
        <el-form-item label="价格" prop="Price">
          <el-input v-model="form.Price" type="number" placeholder="请输入价格" step="0.01"/>
        </el-form-item>
        <el-form-item label="库存" prop="Stock">
          <el-input v-model="form.Stock" type="number" placeholder="请输入库存"/>
        </el-form-item>
        <el-form-item label="分类" prop="Category">
          <el-select v-model="form.Category" placeholder="请选择分类" style="width: 100%">
            <el-option
              v-for="category in categories"
              :key="category.Name"
              :label="category.Name"
              :value="category.Name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="单位" prop="Unit">
          <el-input v-model="form.Unit" placeholder="请输入单位（如：个、瓶、包）"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAdd = false">
          <i class="fas fa-times"></i> 取消
        </el-button>
        <el-button type="primary" @click="addOrUpdate" :loading="submitting">
          <i class="fas fa-check"></i> 确定
        </el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { productAPI, categoryAPI } from '../api'

const products = ref([])
const categories = ref([])
const showAdd = ref(false)
const loading = ref(false)
const submitting = ref(false)
const formRef = ref()

const form = ref({ 
  ProductID: null, 
  Name: '', 
  Price: 0, 
  Stock: 0, 
  Category: '',
  Unit: ''
})

const rules = {
  Name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  Price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  Stock: [{ required: true, message: '请输入库存', trigger: 'blur' }],
  Category: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

async function loadCategories() {
  try {
    const response = await categoryAPI.getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('加载分类失败:', error)
    ElMessage.error('加载分类失败: ' + (error.response?.data?.detail || error.message))
  }
}

async function loadProducts() {
  loading.value = true
  try {
    const response = await productAPI.getProducts()
    products.value = response.data
    ElMessage.success('商品列表加载成功')
  } catch (error) {
    console.error('加载商品失败:', error)
    ElMessage.error('加载商品失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

function edit(row) {
  Object.assign(form.value, row)
  showAdd.value = true
}

async function addOrUpdate() {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
  } catch (error) {
    return
  }
  
  submitting.value = true
  try {
    if (form.value.ProductID) {
      await productAPI.updateProduct(form.value.ProductID, form.value)
      ElMessage.success('商品更新成功')
    } else {
      await productAPI.createProduct(form.value)
      ElMessage.success('商品添加成功')
    }
    showAdd.value = false
    resetForm()
    await loadProducts()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

async function del(id) {
  try {
    await ElMessageBox.confirm('确定要删除这个商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await productAPI.deleteProduct(id)
    const result = response.data
    
    if (result.action === 'stock_zero') {
      // 商品被引用，库存设为0
      ElMessage({
        message: result.message,
        type: 'warning',
        duration: 5000
      })
    } else if (result.action === 'deleted') {
      // 商品被完全删除
      ElMessage.success(result.message)
    } else {
      // 默认成功消息
      ElMessage.success('删除成功')
    }
    
    await loadProducts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

async function reStock(product) {
  try {
    const { value: stock } = await ElMessageBox.prompt(
      `请输入商品 "${product.Name}" 的新库存数量`,
      '重新上架',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^[1-9]\d*$/,
        inputErrorMessage: '库存数量必须是正整数'
      }
    )
    
    if (stock) {
      const updatedProduct = { ...product, Stock: parseInt(stock) }
      await productAPI.updateProduct(product.ProductID, updatedProduct)
      ElMessage.success(`商品 "${product.Name}" 已重新上架，库存设为 ${stock}`)
      await loadProducts()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重新上架失败:', error)
      ElMessage.error('重新上架失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

function resetForm() {
  Object.assign(form.value, { 
    ProductID: null, 
    Name: '', 
    Price: 0, 
    Stock: 0, 
    Category: '',
    Unit: ''
  })
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

onMounted(async () => {
  await loadCategories()
  await loadProducts()
})
</script>

<style scoped>
.el-table .fa-box {
  margin: 0 auto;
  display: block;
}
</style> 