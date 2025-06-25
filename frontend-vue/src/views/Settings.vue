<template>
  <el-card>
    <template #header>
      <span>系统设置</span>
    </template>
    <el-form label-width="120px" style="max-width: 500px; margin: 0 auto;">
      <el-form-item label="主题切换">
        <el-radio-group v-model="theme">
          <el-radio label="light">明亮</el-radio>
          <el-radio label="dark">暗黑</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const theme = ref('light')

// 初始化主题
onMounted(() => {
  const saved = localStorage.getItem('theme')
  if (saved === 'dark') {
    theme.value = 'dark'
    document.documentElement.classList.add('dark')
  } else {
    theme.value = 'light'
    document.documentElement.classList.remove('dark')
  }
})

// 监听主题切换
watch(theme, (val) => {
  if (val === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem('theme', val)
})
</script>

<style scoped>
.el-form {
  margin-top: 40px;
}
</style> 