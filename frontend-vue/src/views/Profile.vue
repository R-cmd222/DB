<template>
  <el-card>
    <h2>个人中心</h2>
    <el-descriptions :column="1" border>
      <el-descriptions-item label="姓名">{{ employee.name }}</el-descriptions-item>
      <el-descriptions-item label="职位">{{ employee.position }}</el-descriptions-item>
      <el-descriptions-item label="角色">{{ roleText[employee.role] }}</el-descriptions-item>
      <el-descriptions-item label="员工ID">{{ employee.id }}</el-descriptions-item>
    </el-descriptions>
    <el-button type="primary" style="margin-top:20px;" @click="showPwd = true">修改密码</el-button>
    <el-dialog v-model="showPwd" title="修改密码" width="400px">
      <el-form :model="pwdForm" label-width="80px">
        <el-form-item label="新密码">
          <el-input v-model="pwdForm.newPwd" type="password" />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="pwdForm.confirmPwd" type="password" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPwd = false">取消</el-button>
        <el-button type="primary" @click="changePwd">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>
<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'
const employee = JSON.parse(localStorage.getItem('employee') || '{}')
const roleText = { cashier: '收银员', stocker: '理货员', warehouse: '仓管员', admin: '管理员' }
const showPwd = ref(false)
const pwdForm = ref({ newPwd: '', confirmPwd: '' })
async function changePwd() {
  if (!pwdForm.value.newPwd || pwdForm.value.newPwd !== pwdForm.value.confirmPwd) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  try {
    await api.post('/change_password', { id: employee.id, newPwd: pwdForm.value.newPwd })
    ElMessage.success('密码修改成功')
    showPwd.value = false
    pwdForm.value = { newPwd: '', confirmPwd: '' }
  } catch (e) {
    ElMessage.error('密码修改失败')
  }
}
</script> 