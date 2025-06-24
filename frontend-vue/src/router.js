import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './views/Dashboard.vue'
import Cashier from './views/Cashier.vue'
import Products from './views/Products.vue'
import Orders from './views/Orders.vue'
import Inventory from './views/Inventory.vue'
import Customers from './views/Customers.vue'
import Reports from './views/Reports.vue'
import Settings from './views/Settings.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/cashier', name: 'Cashier', component: Cashier },
  { path: '/products', name: 'Products', component: Products },
  { path: '/orders', name: 'Orders', component: Orders },
  { path: '/inventory', name: 'Inventory', component: Inventory },
  { path: '/customers', name: 'Customers', component: Customers },
  { path: '/reports', name: 'Reports', component: Reports },
  { path: '/settings', name: 'Settings', component: Settings }
]

export default createRouter({
  history: createWebHistory(),
  routes
}) 