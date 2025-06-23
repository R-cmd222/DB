<template>
  <el-menu :default-active="active" class="el-menu-vertical-demo" @select="onSelect" router>
    <el-menu-item index="/">仪表板</el-menu-item>
    <el-menu-item index="/cashier">收银台</el-menu-item>
    <el-menu-item index="/products">商品管理</el-menu-item>
    <el-menu-item index="/orders">订单管理</el-menu-item>
    <el-menu-item index="/inventory">库存管理</el-menu-item>
    <el-menu-item index="/customers">客户管理</el-menu-item>
    <el-menu-item index="/reports">报表管理</el-menu-item>
    <el-menu-item index="/settings">系统设置</el-menu-item>
  </el-menu>
</template>
<script setup>
import { useRoute, useRouter } from 'vue-router'
const route = useRoute()
const router = useRouter()
const active = route.path
function onSelect(index) {
  router.push(index)
}
</script>
<style scoped>
.el-menu-vertical-demo {
  width: 200px;
  min-height: 100vh;
}
</style> 