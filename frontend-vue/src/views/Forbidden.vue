<template>
  <el-result icon="warning" title="403 无权限" sub-title="您没有权限访问该页面，请联系管理员。">
    <template #extra>
      <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
    </template>
  </el-result>
</template> 