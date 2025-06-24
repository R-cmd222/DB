<template>
  <el-menu :default-active="activeMenu" class="sidebar-menu" router>
    <el-menu-item index="/">
      <i class="fas fa-tachometer-alt"></i>
      <span>仪表板</span>
    </el-menu-item>
    <el-menu-item index="/cashier">
      <i class="fas fa-cash-register"></i>
      <span>收银台</span>
    </el-menu-item>
    <el-menu-item index="/products">
      <i class="fas fa-box"></i>
      <span>商品管理</span>
    </el-menu-item>
    <el-menu-item index="/inventory">
      <i class="fas fa-warehouse"></i>
      <span>库存管理</span>
    </el-menu-item>
    <el-menu-item index="/orders">
      <i class="fas fa-file-invoice-dollar"></i>
      <span>订单管理</span>
    </el-menu-item>
    <el-menu-item index="/customers">
      <i class="fas fa-id-card"></i>
      <span>客户管理</span>
    </el-menu-item>
    <el-menu-item index="/reports">
      <i class="fas fa-chart-bar"></i>
      <span>报表统计</span>
    </el-menu-item>
    <el-menu-item index="/settings">
      <i class="fas fa-cog"></i>
      <span>系统设置</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const activeMenu = ref(route.path)

// 监听路由变化，更新活动菜单项
watch(
  () => route.path,
  (newPath) => {
    activeMenu.value = newPath
  },
  { immediate: true }
)

function onSelect(index) {
  router.push(index)
}
</script>

<style scoped>
.sidebar-menu {
  height: 100vh;
  border-right: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}
.el-menu-item {
  display: flex;
  align-items: center;
  font-size: 1rem;
  padding: 18px 24px;
}
.el-menu-item i {
  width: 22px;
  margin-right: 12px;
  font-size: 1.2rem;
}
</style> 