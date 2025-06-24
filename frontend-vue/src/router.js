import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './views/Dashboard.vue'
import Cashier from './views/Cashier.vue'
import Products from './views/Products.vue'
import Orders from './views/Orders.vue'
import Inventory from './views/Inventory.vue'
import Customers from './views/Customers.vue'
import Reports from './views/Reports.vue'
import Settings from './views/Settings.vue'
import Login from './views/Login.vue'
import Forbidden from './views/Forbidden.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/cashier', name: 'Cashier', component: Cashier },
  { path: '/products', name: 'Products', component: Products },
  { path: '/orders', name: 'Orders', component: Orders },
  { path: '/inventory', name: 'Inventory', component: Inventory },
  { path: '/customers', name: 'Customers', component: Customers },
  { path: '/reports', name: 'Reports', component: Reports },
  { path: '/settings', name: 'Settings', component: Settings },
  { path: '/login', name: 'Login', component: Login },
  { path: '/403', name: 'Forbidden', component: Forbidden }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = sessionStorage.getItem('token')
  const employee = JSON.parse(sessionStorage.getItem('employee') || '{}')
  if (!token && to.path !== '/login') {
    next('/login')
    return
  }
  if (to.meta && to.meta.roles && !to.meta.roles.includes(employee.role) && employee.role !== 'admin') {
    next('/403')
    return
  }
  next()
})

export default router 