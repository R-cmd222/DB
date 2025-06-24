import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '@fortawesome/fontawesome-free/css/all.min.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'

createApp(App).use(router).use(ElementPlus).mount('#app')

// 屏蔽 ResizeObserver loop completed with undelivered notifications 报错（仅开发环境）
if (process.env.NODE_ENV === 'development') {
  const realConsoleError = window.console.error
  window.console.error = (...args) => {
    if (
      typeof args[0] === 'string' &&
      args[0].includes('ResizeObserver loop completed')
    ) {
      return
    }
    realConsoleError(...args)
  }
} 