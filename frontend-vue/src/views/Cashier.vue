<template>
  <div class="cashier-container">
    <!-- 左侧：商品扫描和列表 -->
    <div class="left-panel">
      <el-card>
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>商品扫描</span>
            <el-button type="primary" @click="showProductSearch = true">
              手动添加商品
            </el-button>
          </div>
        </template>
        
        <!-- 操作说明 -->
        <div style="margin-bottom: 8px; color: #888; font-size: 13px;">
          可扫码或输入编号，或点击右上角手动添加
        </div>
        
        <!-- 扫描输入 -->
        <div class="scan-input">
          <el-input
            v-model="scanCode"
            placeholder="请扫描商品条码或输入商品编号"
            @keyup.enter="scanProduct"
            ref="scanInputRef"
            size="large"
          >
            <template #append>
              <el-button @click="scanProduct" :loading="scanning">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </div>
        
        <!-- 购物车商品列表 -->
        <div class="cart-items">
          <h4>购物车 ({{ cartItems.length }} 件商品)</h4>
          <el-table :data="cartItems" style="width: 100%" v-loading="loading">
            <el-table-column prop="name" label="商品名称" />
            <el-table-column prop="price" label="单价" width="100">
              <template #default="scope">
                ¥{{ scope.row.price.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column label="数量" width="120">
              <template #default="scope">
                <el-input-number
                  v-model="scope.row.quantity"
                  :min="1"
                  :max="scope.row.stock"
                  size="small"
                  @change="updateTotal"
                />
              </template>
            </el-table-column>
            <el-table-column label="小计" width="100">
              <template #default="scope">
                ¥{{ (scope.row.price * scope.row.quantity).toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="80">
              <template #default="scope">
                <el-button
                  type="danger"
                  size="small"
                  @click="removeItem(scope.$index)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
    
    <!-- 右侧：结算面板 -->
    <div class="right-panel">
      <el-card class="checkout-card">
        <template #header>
          <span>结算</span>
        </template>
        
        <!-- 总计信息 -->
        <div class="total-info">
          <div class="total-row">
            <span>商品总额：</span>
            <span class="amount">¥{{ subtotal.toFixed(2) }}</span>
          </div>
          <div class="total-row">
            <span>折扣：</span>
            <span class="discount">-¥{{ discount.toFixed(2) }}</span>
          </div>
          <div class="total-row total">
            <span>应付金额：</span>
            <span class="final-amount">¥{{ finalTotal.toFixed(2) }}</span>
          </div>
        </div>
        
        <!-- 折扣设置 -->
        <div class="discount-section">
          <el-input-number
            v-model="discountPercent"
            :min="0"
            :max="100"
            placeholder="折扣百分比"
            @change="updateDiscount"
          />
          <span style="margin-left: 10px;">%</span>
        </div>
        
        <!-- 支付方式 -->
        <div class="payment-section">
          <h4>支付方式</h4>
          <el-radio-group v-model="paymentMethod">
            <el-radio label="cash">现金</el-radio>
            <el-radio label="card">银行卡</el-radio>
            <el-radio label="wechat">微信支付</el-radio>
            <el-radio label="alipay">支付宝</el-radio>
          </el-radio-group>
        </div>
        
        <!-- 客户信息 -->
        <div class="customer-section">
          <h4>客户信息 <span style="color: red;">*</span></h4>
          <el-input
            v-model="customerName"
            placeholder="客户姓名（必填）"
            style="margin-bottom: 10px;"
            required
          />
          <el-input
            v-model="customerPhone"
            placeholder="客户电话（必填）"
            required
          />
        </div>
        
        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button
            type="primary"
            size="large"
            @click="checkout"
            :loading="checkingOut"
            :disabled="cartItems.length === 0"
            style="width: 100%; margin-bottom: 10px;"
          >
            结算 (¥{{ finalTotal.toFixed(2) }})
          </el-button>
          <el-button
            @click="clearCart"
            :disabled="cartItems.length === 0"
            style="width: 100%;"
          >
            清空购物车
          </el-button>
        </div>
      </el-card>
    </div>
    
    <!-- 商品搜索对话框 -->
    <el-dialog v-model="showProductSearch" title="选择商品" width="800px">
      <div style="margin-bottom: 20px;">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索商品名称或编号"
          @keyup.enter="searchProducts"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      
      <el-table
        :data="searchResults"
        style="width: 100%"
        v-loading="searching"
      >
        <el-table-column prop="id" label="编号" width="80" />
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="price" label="价格" width="100">
          <template #default="scope">
            ¥{{ scope.row.price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="80">
          <template #default="scope">
            <span :class="{ 'low-stock': scope.row.stock <= 0 }">
              {{ scope.row.stock <= 0 ? '已下架' : scope.row.stock }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="scope">
            <el-button size="small" @click="selectProduct(scope.row)">
              选择
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    
    <!-- 支付确认对话框 -->
    <el-dialog v-model="showPaymentConfirm" title="支付确认" width="400px">
      <div class="payment-confirm">
        <h3>订单确认</h3>
        <div class="confirm-details">
          <p><strong>商品数量：</strong>{{ cartItems.length }} 件</p>
          <p><strong>应付金额：</strong>¥{{ finalTotal.toFixed(2) }}</p>
          <p><strong>支付方式：</strong>{{ getPaymentMethodText(paymentMethod) }}</p>
          <p v-if="customerName"><strong>客户姓名：</strong>{{ customerName }}</p>
          <p v-if="customerPhone"><strong>客户电话：</strong>{{ customerPhone }}</p>
          <p><strong>获得积分：</strong>{{ Math.floor(finalTotal * 10) }} 积分</p>
          <p style="color: #909399; font-size: 12px;">积分规则：消费1元获得10积分</p>
        </div>
        
        <div class="confirm-actions">
          <el-button @click="showPaymentConfirm = false">取消</el-button>
          <el-button type="primary" @click="confirmPayment" :loading="processingPayment">
            确认支付
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { productAPI, cashierAPI } from '../api'

// 响应式数据
const scanCode = ref('')
const cartItems = ref([])
const loading = ref(false)
const scanning = ref(false)
const checkingOut = ref(false)
const processingPayment = ref(false)

// 搜索相关
const showProductSearch = ref(false)
const searchKeyword = ref('')
const searchResults = ref([])
const searching = ref(false)

// 结算相关
const discountPercent = ref(0)
const paymentMethod = ref('cash')
const customerName = ref('')
const customerPhone = ref('')
const showPaymentConfirm = ref(false)

// 引用
const scanInputRef = ref()

// 计算属性
const subtotal = computed(() => {
  return cartItems.value.reduce((sum, item) => {
    return sum + (item.price * item.quantity)
  }, 0)
})

const discount = computed(() => {
  return subtotal.value * (discountPercent.value / 100)
})

const finalTotal = computed(() => {
  return subtotal.value - discount.value
})

// 方法
async function scanProduct() {
  if (!scanCode.value.trim()) {
    ElMessage.warning('请输入商品条码')
    return
  }
  scanning.value = true
  try {
    // 通过API查找商品
    const res = await productAPI.getProduct(scanCode.value.trim())
    const product = res.data
    if (!product || !product.ProductID) {
      ElMessage.error('未找到该商品')
    } else if (product.Stock <= 0) {
      ElMessage.error(`商品 "${product.Name}" 已下架，库存不足`)
    } else {
      addProductToCart({
        id: product.ProductID,
        name: product.Name,
        price: product.Price,
        stock: product.Stock
      })
    }
  } catch (error) {
    console.error('扫描商品失败:', error)
    ElMessage.error('未找到该商品或商品已下架')
  } finally {
    scanCode.value = ''
    scanning.value = false
    nextTick(() => {
      if (scanInputRef.value) {
        scanInputRef.value.focus()
      }
    })
  }
}

function addProductToCart(product) {
  // 检查库存
  if (product.stock <= 0) {
    ElMessage.error(`商品 "${product.name}" 库存不足，无法添加`)
    return
  }
  
  // 检查是否已在购物车中
  const existingItem = cartItems.value.find(item => item.id === product.id)
  if (existingItem) {
    // 检查增加数量后是否超过库存
    if (existingItem.quantity + 1 > product.stock) {
      ElMessage.warning(`商品 "${product.name}" 库存不足，当前库存: ${product.stock}`)
      return
    }
    existingItem.quantity += 1
    ElMessage.success(`已增加 ${product.name} 的数量`)
  } else {
    cartItems.value.push({
      ...product,
      quantity: 1
    })
    ElMessage.success(`已添加 ${product.name}`)
  }
  updateTotal()
}

function removeItem(index) {
  const item = cartItems.value[index]
  cartItems.value.splice(index, 1)
  ElMessage.success(`已移除 ${item.name}`)
  updateTotal()
}

function updateTotal() {
  // 总价会自动通过计算属性更新
}

function updateDiscount() {
  // 折扣会自动通过计算属性更新
}

function clearCart() {
  ElMessageBox.confirm('确定要清空购物车吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    cartItems.value = []
    discountPercent.value = 0
    customerName.value = ''
    customerPhone.value = ''
    ElMessage.success('购物车已清空')
  })
}

async function searchProducts() {
  if (!searchKeyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  searching.value = true
  try {
    // 通过API搜索商品
    const res = await productAPI.getProducts()
    // 支持名称或编号模糊搜索，并过滤掉库存为0的商品
    searchResults.value = res.data.filter(item =>
      ((item.Name && item.Name.includes(searchKeyword.value)) ||
       (item.ProductID && item.ProductID.toString().includes(searchKeyword.value))) &&
      item.Stock > 0  // 只显示有库存的商品
    ).map(item => ({
      id: item.ProductID,
      name: item.Name,
      price: item.Price,
      stock: item.Stock
    }))
    
    if (searchResults.value.length === 0) {
      ElMessage.info('未找到符合条件的商品或商品已下架')
    }
  } catch (error) {
    console.error('搜索商品失败:', error)
    ElMessage.error('搜索失败: ' + (error.response?.data?.detail || error.message))
    searchResults.value = []
  } finally {
    searching.value = false
  }
}

function selectProduct(product) {
  addProductToCart(product)
  showProductSearch.value = false
  searchKeyword.value = ''
}

function checkout() {
  if (cartItems.value.length === 0) {
    ElMessage.warning('购物车为空')
    return
  }
  
  // 验证客户信息
  if (!customerName.value.trim()) {
    ElMessage.error('请输入客户姓名')
    return
  }
  
  if (!customerPhone.value.trim()) {
    ElMessage.error('请输入客户电话')
    return
  }
  
  showPaymentConfirm.value = true
}

function getPaymentMethodText(method) {
  const methodMap = {
    cash: '现金',
    card: '银行卡',
    wechat: '微信支付',
    alipay: '支付宝'
  }
  return methodMap[method] || method
}

async function confirmPayment() {
  processingPayment.value = true
  
  try {
    // 创建收银台结算数据
    const checkoutData = {
      customer_name: customerName.value,
      customer_phone: customerPhone.value,
      items: cartItems.value.map(item => ({
        ProductID: item.id,
        Quantity: item.quantity,
        Price: item.price
      })),
      total_amount: finalTotal.value,
      payment_method: getPaymentMethodText(paymentMethod.value),
      discount: discount.value
    }
    
    // 调用收银台结算API
    const response = await cashierAPI.checkout(checkoutData)
    
    // 模拟支付过程
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('支付成功！')
    
    // 清空购物车
    cartItems.value = []
    discountPercent.value = 0
    customerName.value = ''
    customerPhone.value = ''
    showPaymentConfirm.value = false
    
    // 打印小票（这里可以调用打印机API）
    printReceipt(response.data)
    
  } catch (error) {
    console.error('支付失败:', error)
    ElMessage.error('支付失败，请重试: ' + (error.response?.data?.detail || error.message))
  } finally {
    processingPayment.value = false
  }
}

function printReceipt(orderData) {
  // 这里可以实现打印小票的功能
  console.log('打印小票:', orderData)
}

// 生命周期
onMounted(() => {
  // 聚焦到扫描输入框
  nextTick(() => {
    scanInputRef.value?.focus()
  })
})
</script>

<style scoped>
.cashier-container {
  display: flex;
  gap: 20px;
  height: calc(100vh - 120px);
}

.left-panel {
  flex: 2;
}

.right-panel {
  flex: 1;
}

.checkout-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.scan-input {
  margin-bottom: 20px;
}

.cart-items {
  flex: 1;
}

.cart-items h4 {
  margin-bottom: 15px;
  color: #333;
}

.total-info {
  margin-bottom: 20px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 16px;
}

.total-row.total {
  border-top: 1px solid #eee;
  padding-top: 10px;
  font-size: 18px;
  font-weight: bold;
}

.amount {
  color: #409EFF;
}

.discount {
  color: #67C23A;
}

.final-amount {
  color: #E6A23C;
  font-size: 20px;
}

.discount-section {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.payment-section {
  margin-bottom: 20px;
}

.payment-section h4 {
  margin-bottom: 10px;
  color: #333;
}

.customer-section {
  margin-bottom: 20px;
}

.customer-section h4 {
  margin-bottom: 10px;
  color: #333;
}

.action-buttons {
  margin-top: auto;
}

.payment-confirm {
  text-align: center;
}

.confirm-details {
  margin: 20px 0;
  text-align: left;
}

.confirm-details p {
  margin: 10px 0;
}

.confirm-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.low-stock {
  color: #F56C6C;
  font-weight: bold;
}
</style> 