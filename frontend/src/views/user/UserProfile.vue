<template>
  <div class="user-profile-container">
    <!-- 浮动形状装饰 -->
    <div class="floating-shape shape-1"></div>
    <div class="floating-shape shape-2"></div>
    <div class="floating-shape shape-3"></div>
    
    <!-- 返回按钮 -->
    <div class="back-button">
      <el-button class="home-button" @click="goToHome">
        <el-icon><HomeFilled /></el-icon>
        返回首页
      </el-button>
    </div>

    <!-- 个人信息卡片 -->
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <el-icon><User /></el-icon>
          <span>个人信息</span>
        </div>
      </template>

      <div class="profile-content">
        <!-- 头像区域 -->
        <div class="avatar-section">
          <div class="avatar-container">
            <el-avatar :size="120" class="profile-avatar" :src="userInfo?.avatar">
              {{ userInfo?.avatar ? '' : userInfo?.username?.charAt(0).toUpperCase() }}
            </el-avatar>
            <div class="avatar-actions">
              <el-button type="primary" size="small" @click="handleAvatarEdit">
                <el-icon><Edit /></el-icon>
                更改头像
              </el-button>
            </div>
          </div>
        </div>

        <!-- 基本信息区域 -->
        <div class="info-section">
          <el-descriptions title="基本信息" :column="1" border>
            <el-descriptions-item label="用户名">
              {{ userInfo?.username || '未设置' }}
            </el-descriptions-item>
            <el-descriptions-item label="用户ID">
              {{ userInfo?.id || '未设置' }}
            </el-descriptions-item>
            <el-descriptions-item label="登录时间">
              {{ formatLoginTime() }}
            </el-descriptions-item>
            <el-descriptions-item label="角色">
              {{ getUserRole() }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 系统信息区域 -->
        <div class="system-section">
          <el-descriptions title="系统信息" :column="1" border>
            <el-descriptions-item label="最后登录IP">
              {{ systemInfo.lastLoginIp || '未知' }}
            </el-descriptions-item>
            <el-descriptions-item label="登录次数">
              {{ systemInfo.loginCount || 0 }}
            </el-descriptions-item>
            <el-descriptions-item label="账户状态">
              <el-tag :type="systemInfo.status === 'active' ? 'success' : 'danger'">
                {{ systemInfo.status === 'active' ? '正常' : '异常' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="注册时间">
              {{ systemInfo.registerTime || '未知' }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 操作按钮 -->
        <div class="action-section">
          <el-button type="primary" @click="handleEditProfile">
            <el-icon><Edit /></el-icon>
            编辑信息
          </el-button>
          <el-button type="warning" @click="handleChangePassword">
            <el-icon><Lock /></el-icon>
            修改密码
          </el-button>
          <el-button type="danger" @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            注销登录
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 头像编辑对话框 -->
    <el-dialog
      v-model="avatarDialogVisible"
      title="更改头像"
      width="400px"
      @close="handleAvatarDialogClose"
    >
      <div class="avatar-edit-dialog">
        <el-upload
          class="avatar-uploader"
          action="/api/avatar/edit/"
          :show-file-list="false"
          :before-upload="beforeAvatarUpload"
          :on-success="handleAvatarSuccess"
          :on-error="handleAvatarError"
        >
          <el-avatar v-if="avatarUrl" :src="avatarUrl" :size="100" />
          <el-icon v-else class="avatar-uploader-icon">
            <Plus />
          </el-icon>
        </el-upload>
        <div class="upload-tips">
          <p>支持 JPG、PNG 格式，文件大小不超过 2MB</p>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="avatarDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAvatar">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Edit, SwitchButton, Lock, HomeFilled, Plus } from '@element-plus/icons-vue'
import { logout } from '@/api/user'

const router = useRouter()

// 用户信息
const userInfo = ref<any>(null)

// 系统信息
const systemInfo = reactive({
  lastLoginIp: '192.168.1.100',
  loginCount: 15,
  status: 'active',
  registerTime: '2024-01-01 10:00:00'
})

// 对话框状态
const avatarDialogVisible = ref(false)
const avatarUrl = ref('')

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

// 格式化登录时间
const formatLoginTime = () => {
  const now = new Date()
  return now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 获取用户角色
const getUserRole = () => {
  return userInfo.value?.role === 'admin' ? '管理员' : '普通用户'
}

// 返回首页
const goToHome = () => {
  router.push('/')
}

// 处理头像编辑
const handleAvatarEdit = () => {
  router.push('/avatar/edit')
}

// 处理编辑信息
const handleEditProfile = () => {
  ElMessage.info('编辑信息功能开发中...')
}

// 处理修改密码
const handleChangePassword = () => {
  ElMessage.info('修改密码功能开发中...')
}

// 处理注销
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要注销登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    // 调用后端注销API
    await logout()
    
    // 清除本地存储的用户信息
    localStorage.removeItem('userInfo')
    
    // 显示成功消息
    ElMessage.success('注销成功')
    
    // 跳转到登录页
    router.push('/login')
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('注销失败:', error)
      ElMessage.error('注销失败，请重试')
    }
  }
}

// 头像上传前验证
const beforeAvatarUpload = (file: File) => {
  const isJPGOrPNG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPGOrPNG) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }
  
  // 创建预览URL
  const reader = new FileReader()
  reader.onload = (e) => {
    avatarUrl.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
  
  return true
}

// 头像上传成功
const handleAvatarSuccess = (response: any) => {
  if (response.code === 200) {
    ElMessage.success('头像上传成功')
    avatarDialogVisible.value = false
    // 更新用户信息
    getUserInfo()
  } else {
    ElMessage.error(response.message || '头像上传失败')
  }
}

// 头像上传失败
const handleAvatarError = () => {
  ElMessage.error('头像上传失败，请重试')
}

// 提交头像
const submitAvatar = () => {
  // 这里可以添加头像提交逻辑
  ElMessage.info('头像提交功能开发中...')
}

// 头像对话框关闭
const handleAvatarDialogClose = () => {
  avatarUrl.value = ''
}

// 头像更新事件处理函数
const handleAvatarUpdate = () => {
  // 重新获取用户信息以更新头像
  getUserInfo()
}

// 组件挂载时获取用户信息
onMounted(() => {
  getUserInfo()
  
  // 监听头像更新事件
  window.addEventListener('avatarUpdated', handleAvatarUpdate)
})

// 组件卸载时移除事件监听器
onUnmounted(() => {
  window.removeEventListener('avatarUpdated', handleAvatarUpdate)
})
</script>

<style scoped>
@import './UserList.css';
@import '../../assets/css/theme.css';

.user-profile-container {
  padding: 20px;
  height: 100vh;
  overflow-y: auto;
  position: relative;
  background: var(--background-color, linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%));
}

.profile-card {
  background: var(--card-background, rgba(255, 255, 255, 0.9)) !important;
  border: 1px solid var(--border-color, #e4e7ed) !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
  max-width: 800px;
  margin: 80px auto 0;
  position: relative;
  z-index: 2;
}

.profile-card :deep(.el-card__header) {
  background: var(--card-background, rgba(255, 255, 255, 0.9)) !important;
  border-bottom: 1px solid var(--border-color, #e4e7ed) !important;
  color: var(--text-color, #303133) !important;
}

.profile-card :deep(.el-descriptions__title) {
  color: var(--text-color, #303133) !important;
}

.profile-card :deep(.el-descriptions__label) {
  color: var(--text-color, #606266) !important;
}

.profile-card :deep(.el-descriptions__content) {
  color: var(--text-color, #303133) !important;
}

.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
}

.home-button {
  background: linear-gradient(45deg, var(--primary-color, #409EFF), var(--info-color, #909399)) !important;
  border: none !important;
  color: white !important;
  font-weight: bold !important;
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.3) !important;
  transition: all 0.3s ease !important;
}

.home-button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(64, 158, 255, 0.4) !important;
}

.profile-content {
  padding: 20px;
}

.avatar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.avatar-container {
  text-align: center;
}

.profile-avatar {
  margin-bottom: 15px;
}

.info-section, .system-section {
  margin-bottom: 30px;
}

.action-section {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
}

/* 浮动形状装饰 */
.floating-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
  z-index: 1;
  filter: blur(40px);
  animation: float 15s infinite ease-in-out;
}

.shape-1 {
  width: 200px;
  height: 200px;
  background: var(--primary-color, #409EFF);
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  background: var(--success-color, #67C23A);
  top: 70%;
  left: 80%;
  animation-delay: 5s;
}

.shape-3 {
  width: 120px;
  height: 120px;
  background: var(--warning-color, #E6A23C);
  top: 40%;
  left: 70%;
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-20px) rotate(5deg);
  }
  50% {
    transform: translateY(-10px) rotate(-5deg);
  }
  75% {
    transform: translateY(-15px) rotate(3deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-card {
    margin: 100px 20px 0;
  }
  
  .action-section {
    flex-direction: column;
    align-items: center;
  }
  
  .back-button {
    position: relative;
    top: 0;
    left: 0;
    margin-bottom: 20px;
  }
}
</style>