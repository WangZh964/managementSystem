<template>
  <div id="home-page" class="home-container">
    <el-container class="main-container">
      <!-- 侧边栏导航 -->
      <el-aside width="240px" class="sidebar">
        <div class="sidebar-header">
          <h3>中国移动用户管理系统</h3>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical-demo"
          @select="handleMenuSelect"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="admin/list">
            <el-icon><User /></el-icon>
            <span>管理员账户</span>
          </el-menu-item>
          <el-menu-item index="depart/list">
            <el-icon><School /></el-icon>
            <span>部门管理</span>
          </el-menu-item>
          <el-menu-item index="user/list">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="pretty/list">
            <el-icon><Phone /></el-icon>
            <span>靓号管理</span>
          </el-menu-item>
          <el-menu-item index="city/list">
            <el-icon><Location /></el-icon>
            <span>城市列表</span>
          </el-menu-item>
          <el-menu-item index="task/list">
            <el-icon><Check /></el-icon>
            <span>任务管理</span>
          </el-menu-item>
          <el-menu-item index="order/list">
            <el-icon><ShoppingCart /></el-icon>
            <span>订单管理</span>
          </el-menu-item>
          <el-menu-item index="chart/list">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据统计</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部导航栏 -->
        <el-header class="header">
          <div class="header-left">
            <el-icon><Menu /></el-icon>
          </div>
          <div class="header-right">
            <!-- 主题切换按钮 -->
            <el-dropdown trigger="click" @command="handleThemeChange" class="theme-dropdown">
              <el-button type="primary" link class="theme-button">
                <el-icon><Sunny /></el-icon>
                主题
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="light"><el-icon><Sunny /></el-icon>浅色模式</el-dropdown-item>
                  <el-dropdown-item command="dark"><el-icon><Moon /></el-icon>深色模式</el-dropdown-item>
                  <el-dropdown-item divided command="auto"><el-icon><Monitor /></el-icon>跟随系统</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            
            <el-dropdown>
              <span class="dropdown-link">
                <el-avatar class="avatar" :src="userInfo?.avatar">
                  {{ userInfo?.avatar ? '' : userInfo?.username?.charAt(0).toUpperCase() }}
                </el-avatar>
                <span>{{ userInfo?.username }}</span>
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleProfile"><el-icon><User /></el-icon>个人信息</el-dropdown-item>
                  <el-dropdown-item @click="handleAvatarEdit"><el-icon><Edit /></el-icon>更改头像</el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout"><el-icon><SwitchButton /></el-icon>退出</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>

        <!-- 内容区 -->
        <el-main class="content">
          <div class="welcome-message">
            <div class="welcome-header">
              <h2>欢迎使用中国移动用户管理系统</h2>
              <div class="animated-line"></div>
            </div>
            <p>请从左侧菜单选择要操作的功能</p>
            
            <div class="feature-cards">
              <div class="feature-card" v-for="(feature, index) in features" :key="index" 
                   :style="{animationDelay: `${index * 0.1}s`}">
                <div class="card-icon">
                  <el-icon><component :is="feature.icon" /></el-icon>
                </div>
                <h3>{{ feature.title }}</h3>
                <p>{{ feature.description }}</p>
              </div>
            </div>
            
            <div class="floating-shapes">
              <div class="shape shape-1"></div>
              <div class="shape shape-2"></div>
              <div class="shape shape-3"></div>
              <div class="shape shape-4"></div>
            </div>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Menu, User, Phone, Location, Check, ShoppingCart, DataAnalysis, ArrowDown, Edit, School, SwitchButton, Sunny, Moon, Monitor } from '@element-plus/icons-vue'
import { logout } from '../api/user'

const router = useRouter()
const activeMenu = ref('')
const userInfo = ref<any>(null)

// 功能特性数据
const features = reactive([
  {
    id: 1,
    title: '用户管理',
    description: '管理系统用户信息，包括添加、编辑、删除用户等功能',
    icon: User,
    color: '#409EFF',
    delay: 0.1
  },
  {
    id: 2,
    title: '部门管理',
    description: '组织架构管理，支持部门层级结构展示和编辑',
    icon: School,
    color: '#67C23A',
    delay: 0.2
  },
  {
    id: 3,
    title: '靓号管理',
    description: '管理特殊号码资源，支持号码分类和查询',
    icon: Phone,
    color: '#E6A23C',
    delay: 0.3
  },
  {
    id: 4,
    title: '订单管理',
    description: '订单全生命周期管理，支持订单跟踪和状态更新',
    icon: ShoppingCart,
    color: '#F56C6C',
    delay: 0.4
  },
  {
    id: 5,
    title: '数据统计',
    description: '可视化数据展示，支持多种图表类型和数据分析',
    icon: DataAnalysis,
    color: '#909399',
    delay: 0.5
  },
  {
    id: 6,
    title: '任务管理',
    description: '任务分配和跟踪，支持任务状态管理和提醒',
    icon: Check,
    color: '#7F4CE5',
    delay: 0.6
  }
])

// 获取用户信息
const getUserInfo = () => {
  const userInfoStr = localStorage.getItem('userInfo')
  if (userInfoStr) {
    userInfo.value = JSON.parse(userInfoStr)
  } else {
    // 如果没有用户信息，重定向到登录页
    router.push('/login')
  }
}

// 处理菜单选择
const handleMenuSelect = (index: string) => {
  activeMenu.value = index
  
  // 根据选择的菜单跳转到对应的页面
  switch (index) {
    case 'admin/list':
      router.push('/admin')
      break
    case 'depart/list':
      router.push('/department')
      break
    case 'user/list':
      router.push('/user')
      break
    case 'pretty/list':
      router.push('/pretty')
      break
    case 'task/list':
          router.push('/task')
          break
        case 'order/list':
          router.push('/order')
          break
        case 'chart/list':
          router.push('/chart')
          break
        case 'city/list':
          router.push('/city')
          break
    // 其他菜单项的路由跳转可以在这里添加
    default:
      // 默认情况下不跳转，显示欢迎信息
      break
  }
}

// 处理个人信息
const handleProfile = () => {
  router.push('/user/profile')
}

// 处理更改头像
const handleAvatarEdit = () => {
  router.push('/avatar/edit')
}

// 处理主题切换
const handleThemeChange = (command: string) => {
  switch (command) {
    case 'light':
      ElMessage.success('已切换到浅色模式')
      // 应用浅色模式主题
      document.documentElement.classList.remove('theme-dark')
      document.documentElement.classList.add('theme-light')
      document.documentElement.style.setProperty('--background-color', 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)')
      document.documentElement.style.setProperty('--header-background', '#fff')
      break
    case 'dark':
      ElMessage.success('已切换到深色模式')
      // 应用深色模式主题
      document.documentElement.classList.remove('theme-light')
      document.documentElement.classList.add('theme-dark')
      document.documentElement.style.setProperty('--background-color', 'linear-gradient(135deg, #2d3748 0%, #4a5568 100%)')
      document.documentElement.style.setProperty('--header-background', '#4a5568')
      break
    case 'auto':
      ElMessage.success('已切换到跟随系统')
      // 检测系统主题并应用
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.remove('theme-light')
        document.documentElement.classList.add('theme-dark')
        document.documentElement.style.setProperty('--background-color', 'linear-gradient(135deg, #2d3748 0%, #4a5568 100%)')
        document.documentElement.style.setProperty('--header-background', '#4a5568')
      } else {
        document.documentElement.classList.remove('theme-dark')
        document.documentElement.classList.add('theme-light')
        document.documentElement.style.setProperty('--background-color', 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)')
        document.documentElement.style.setProperty('--header-background', '#fff')
      }
      break
  }
}

// 处理注销
const handleLogout = async () => {
  try {
    // 调用后端注销API
    await logout()
    
    // 清除本地存储的用户信息
    localStorage.removeItem('userInfo')
    
    // 显示成功消息
    ElMessage.success('注销成功')
    
    // 跳转到登录页
    router.push('/login')
  } catch (error: any) {
    console.error('注销失败:', error)
    ElMessage.error('注销失败，请重试')
  }
}

// 鼠标位置跟踪
const mouseX = ref(0);
const mouseY = ref(0);

// 更新鼠标位置
const updateMousePosition = (e: MouseEvent) => {
  mouseX.value = e.clientX;
  mouseY.value = e.clientY;
};

// 监听头像更新事件
const handleAvatarUpdate = () => {
  getUserInfo()
}

// 页面加载时获取用户信息
onMounted(() => {
  getUserInfo()
  
  // 添加头像更新事件监听
  window.addEventListener('avatarUpdated', handleAvatarUpdate)
  
  // 添加鼠标移动监听
  document.addEventListener('mousemove', updateMousePosition);
  
  // 为功能卡片添加动画延迟
  const cards = document.querySelectorAll('.feature-card');
  cards.forEach((card, index) => {
    if (card instanceof HTMLElement) {
      card.style.animationDelay = `${index * 0.1}s`;
    }
  });
  
  // 添加页面加载动画
  const welcomeMessage = document.querySelector('.welcome-message');
  if (welcomeMessage) {
    if (welcomeMessage instanceof HTMLElement) {
      welcomeMessage.style.opacity = '0'; 
    }
    if (welcomeMessage instanceof HTMLElement) {
      welcomeMessage.style.transform = 'translateY(30px)';
    }
    
    setTimeout(() => {
      if (welcomeMessage instanceof HTMLElement) {
        welcomeMessage.style.transition = 'all 0.8s ease';
        welcomeMessage.style.opacity = '1';
        welcomeMessage.style.transform = 'translateY(0)';
      }
    }, 300);
  }
});

// 组件卸载时移除事件监听
onUnmounted(() => {
  document.removeEventListener('mousemove', updateMousePosition);
  window.removeEventListener('avatarUpdated', handleAvatarUpdate);
});
</script>

<style scoped>
@import '../assets/css/Home.css';
</style>