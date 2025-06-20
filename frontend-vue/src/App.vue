<template>
  <el-container style="height: 100vh">
    <el-aside width="200px">
      <Sidebar />
    </el-aside>
    <el-container>
      <el-header style="background:#f5f5f5;">
        <h2>超市管理系统</h2>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>
<script setup>
import Sidebar from './components/Sidebar.vue'
</script> 