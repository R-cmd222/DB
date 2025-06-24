<template>
  <el-container style="height: 100vh">
    <el-aside width="200px" v-if="isLoggedIn">
      <Sidebar />
    </el-aside>
    <el-container>
      <el-header v-if="isLoggedIn" style="background:#f5f5f5; display: flex; justify-content: space-between; align-items: center;">
        <h2>超市管理系统</h2>
        <UserMenu />
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>
<script setup>
import Sidebar from './components/Sidebar.vue'
import UserMenu from './components/UserMenu.vue'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isLoggedIn = ref(!!sessionStorage.getItem('token'))

watch(
  () => route.path,
  () => {
    isLoggedIn.value = !!sessionStorage.getItem('token')
  },
  { deep: true, immediate: true }
)
</script>

<style>
/* Global styles to remove default margin and prevent scrollbars */
html, body {
  margin: 0;
  padding: 0;
}
</style> 