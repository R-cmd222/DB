<template>
  <el-dropdown>
    <span>
      {{ employee.name }}（{{ roleText[employee.role] }}）
      <i class="el-icon-arrow-down"></i>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>
<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const employee = JSON.parse(sessionStorage.getItem('employee') || '{}')
const roleText = { cashier: '收银员', stocker: '理货员', warehouse: '仓管员', admin: '管理员' }
function logout() {
  sessionStorage.clear()
  window.location.href = '/login'
}
</script> 