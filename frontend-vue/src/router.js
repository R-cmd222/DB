import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './views/Dashboard.vue'
import Products from './views/Products.vue'
import Orders from './views/Orders.vue'
import Inventory from './views/Inventory.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/products', component: Products },
  { path: '/orders', component: Orders },
  { path: '/inventory', component: Inventory }
]

export default createRouter({
  history: createWebHistory(),
  routes
}) 