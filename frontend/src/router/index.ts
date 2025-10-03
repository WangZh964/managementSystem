import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/admin/AdminList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/department',
    name: 'Department',
    component: () => import('@/views/department/DepartmentList.vue')
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('@/views/user/UserList.vue')
  },
  {
    path: '/pretty',
    name: 'Pretty',
    component: () => import('@/views/pretty/PrettyList.vue')
  },
  {
    path: '/city',
    name: 'City',
    component: () => import('@/views/city/CityList.vue')
  },
  {
    path: '/city/list',
    name: 'CityList',
    component: () => import('@/views/city/CityList.vue')
  },
  {
    path: '/city/add',
    name: 'CityAdd',
    component: () => import('@/views/city/CityAdd.vue')
  },
  {
    path: '/task',
    name: 'Task',
    component: () => import('@/views/task/TaskList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/order',
    name: 'Order',
    component: () => import('@/views/order/OrderList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chart',
    name: 'Chart',
    component: () => import('@/views/chart/ChartList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/profile',
    name: 'UserProfile',
    component: () => import('@/views/user/UserProfile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/avatar/edit',
    name: 'AvatarEdit',
    component: () => import('@/views/user/AvatarEdit.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router