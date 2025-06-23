<template>
  <el-card>
    <div style="margin-bottom: 20px;">
      <el-button type="primary" @click="showAdd = true" :loading="loading">
        添加商品
      </el-button>
      <el-button @click="loadProducts" :loading="loading">
        刷新
      </el-button>
    </div>
    
    <el-table :data="products" style="width: 100%" v-loading="loading">
      <el-table-column prop="ProductID" label="ID" width="60"/>
      <el-table-column prop="Name" label="商品名称"/>
      <el-table-column prop="Price" label="价格">
        <template #default="scope">
          ¥{{ scope.row.Price ? scope.row.Price.toFixed(2) : '0.00' }}
        </template>
      </el-table-column>
      <el-table-column prop="Stock" label="库存">
        <template #default="scope">
          <el-tag :type="scope.row.Stock < 10 ? 'danger' : 'success'">
            {{ scope.row.Stock }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="CategoryID" label="分类"/>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="edit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="del(scope.row.ProductID)">删除</el-button>
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
        <el-form-item label="分类" prop="CategoryID">
          <el-input v-model="form.CategoryID" type="number" placeholder="请输入分类ID"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAdd = false">取消</el-button>
        <el-button type="primary" @click="addOrUpdate" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { productAPI } from '../api'

const products = ref([])
const showAdd = ref(false)
const loading = ref(false)
const submitting = ref(false)
const formRef = ref()

const form = ref({ 
  ProductID: null, 
  Name: '', 
  Price: 0, 
  Stock: 0, 
  CategoryID: 1 
})

const rules = {
  Name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  Price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  Stock: [{ required: true, message: '请输入库存', trigger: 'blur' }],
  CategoryID: [{ required: true, message: '请输入分类ID', trigger: 'blur' }]
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
    
    await productAPI.deleteProduct(id)
    ElMessage.success('删除成功')
    await loadProducts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

function resetForm() {
  Object.assign(form.value, { 
    ProductID: null, 
    Name: '', 
    Price: 0, 
    Stock: 0, 
    CategoryID: 1 
  })
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

onMounted(loadProducts)
</script> 