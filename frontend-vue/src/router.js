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
  { path: '/', component: Dashboard },
  { path: '/cashier', component: Cashier },
  { path: '/products', component: Products },
  { path: '/orders', component: Orders },
  { path: '/inventory', component: Inventory },
  { path: '/customers', component: Customers },
  { path: '/reports', component: Reports },
  { path: '/settings', component: Settings }
]

export default createRouter({
  history: createWebHistory(),
  routes
}) 