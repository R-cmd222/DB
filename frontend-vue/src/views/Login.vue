<template>
  <el-card>
    <el-form :model="form" @submit.prevent="onLogin">
      <el-form-item label="用户名">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" type="password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onLogin">登录</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'

const form = ref({ username: '', password: '' })
const router = useRouter()

async function onLogin() {
  try {
    const res = await api.post('/login', form.value)
    sessionStorage.setItem('token', res.data.token)
    sessionStorage.setItem('employee', JSON.stringify(res.data.employee))
    router.push('/')
  } catch (e) {
    ElMessage.error('登录失败：' + (e.response?.data?.detail || e.message))
  }
}
</script> 