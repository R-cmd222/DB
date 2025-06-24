<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>超市管理系统</h2>
        </div>
      </template>
      <el-form :model="form" @submit.prevent="onLogin" class="login-form">
        <el-form-item>
          <el-input 
            v-model="form.username" 
            placeholder="请输入用户名" 
            size="large" 
            :prefix-icon="UserIcon"
          />
        </el-form-item>
        <el-form-item>
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码" 
            size="large" 
            :prefix-icon="LockIcon"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onLogin" class="login-button" size="large" :loading="loading">
            登 录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'
import { User, Lock } from '@element-plus/icons-vue'

// 为了在模板中使用图标
const UserIcon = User
const LockIcon = Lock

const form = ref({ username: '', password: '' })
const router = useRouter()
const loading = ref(false)

async function onLogin() {
  loading.value = true
  try {
    const res = await api.post('/login', form.value)
    sessionStorage.setItem('token', res.data.token)
    sessionStorage.setItem('employee', JSON.stringify(res.data.employee))
    router.push('/')
  } catch (e) {
    ElMessage.error('登录失败：' + (e.response?.data?.detail || e.message))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login-card {
  width: 400px;
  border-radius: 15px;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  animation: fadeIn 0.7s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.card-header h2 {
  text-align: center;
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.login-form {
  margin-top: 25px;
}

:deep(.el-input__wrapper) {
  background-color: rgba(245, 245, 245, 0.7) !important;
  border-radius: 8px !important;
  box-shadow: none !important;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper.is-focus) {
  background-color: #ffffff !important;
  box-shadow: 0 0 0 1px var(--el-color-primary) !important;
}

.login-button {
  width: 100%;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 8px;
}

:deep(.el-card__header) {
  padding: 20px 20px 0 20px;
  border-bottom: none;
}
</style> 