<template>
  <el-menu :default-active="activeMenu" class="sidebar-menu" router>
    <el-menu-item v-for="item in visibleMenus" :key="item.path" :index="item.path" @click="go(item.path)">
      <i :class="['fa', item.icon]"></i>
      <span>{{ item.label }}</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const activeMenu = ref(route.path)

const employee = ref(JSON.parse(sessionStorage.getItem('employee') || '{}'))

watch(
  () => route.path,
  (newPath) => {
    activeMenu.value = newPath
    // 每次路由变化都可能意味着登录状态改变，重新读取
    employee.value = JSON.parse(sessionStorage.getItem('employee') || '{}')
  },
  { immediate: true }
)

const menus = [
  { path: '/', label: '仪表盘', icon: 'fa-home', roles: ['cashier','stocker','warehouse','admin'] },
  { path: '/cashier', label: '收银台', icon: 'fa-cash-register', roles: ['cashier','admin'] },
  { path: '/orders', label: '订单管理', icon: 'fa-list', roles: ['cashier','admin'] },
  { path: '/products', label: '商品管理', icon: 'fa-box', roles: ['stocker','admin'] },
  { path: '/inventory', label: '库存管理', icon: 'fa-warehouse', roles: ['warehouse','admin'] },
  { path: '/customers', label: '客户管理', icon: 'fa-users', roles: ['admin'] },
  { path: '/reports', label: '报表统计', icon: 'fa-chart-bar', roles: ['admin'] },
  { path: '/settings', label: '系统设置', icon: 'fa-cog', roles: ['cashier','stocker','warehouse','admin'] }
]

const visibleMenus = computed(() => {
  const userRole = employee.value?.role
  if (!userRole) return []
  return menus.filter(m => m.roles.includes(userRole))
})

function go(path) { router.push(path) }
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