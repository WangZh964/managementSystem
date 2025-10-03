<template>
  <div class="avatar-edit-container">
    <!-- 返回首页按钮 -->
    <div class="back-to-home">
      <el-button type="primary" @click="goToHome" class="home-button">
        <el-icon><HomeFilled /></el-icon>
        点击返回主页
      </el-button>
    </div>

    <!-- 头像编辑面板 -->
    <el-card class="avatar-edit-panel" shadow="hover">
      <template #header>
        <div class="panel-header">
          <h2>更改头像</h2>
        </div>
      </template>

      <div class="avatar-edit-content">
        <!-- 头像上传表单 -->
        <el-form ref="avatarFormRef" label-width="80px">
          <el-form-item label="选择头像">
            <div class="upload-area" @click="triggerFileInput">
              <el-avatar v-if="avatarPreview" :src="avatarPreview" :size="120" />
              <div v-else class="upload-placeholder">
                <el-icon size="60"><Plus /></el-icon>
                <p>点击上传头像</p>
              </div>
            </div>
            <input
              ref="fileInput"
              type="file"
              accept="image/jpeg,image/png"
              style="display: none"
              @change="handleFileSelect"
            />
            <div class="upload-tips">
              <p>支持 JPG、PNG 格式，文件大小不超过 2MB</p>
            </div>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitAvatar" :loading="uploading" :disabled="!selectedFile">
              提交头像
            </el-button>
            <el-button @click="goToHome">返回首页</el-button>
          </el-form-item>
        </el-form>

        <!-- 当前头像预览 -->
        <div class="current-avatar-section" v-if="currentAvatar">
          <h3>当前头像</h3>
          <el-avatar :src="currentAvatar" :size="80" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { HomeFilled, Plus } from '@element-plus/icons-vue'

const router = useRouter()

// 状态管理
const avatarPreview = ref('')
const currentAvatar = ref('')
const uploading = ref(false)
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement>()

// 获取当前用户信息
const getUserInfo = () => {
  const userInfoStr = localStorage.getItem('userInfo')
  if (userInfoStr) {
    const userInfo = JSON.parse(userInfoStr)
    currentAvatar.value = userInfo.avatar || ''
  }
}

// 返回首页
const goToHome = () => {
  router.push('/')
}

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value?.click()
}

// 处理文件选择
const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  // 验证文件格式和大小
  const isJPGOrPNG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPGOrPNG) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
    return
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return
  }
  
  // 创建预览URL
  const reader = new FileReader()
  reader.onload = (e) => {
    avatarPreview.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
  
  selectedFile.value = file
}

// 提交头像
const submitAvatar = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择头像文件')
    return
  }
  
  uploading.value = true
  
  try {
    // 创建FormData对象
    const formData = new FormData()
    formData.append('avatar', selectedFile.value)
    
    // 发送POST请求到后端
    const response = await fetch('http://localhost:8000/avatar/edit/', {
      method: 'POST',
      body: formData,
      credentials: 'include' // 包含cookies
    })
    
    if (response.ok) {
      ElMessage.success('头像上传成功')
      
      // 更新本地用户信息中的头像
      const userInfoStr = localStorage.getItem('userInfo')
      if (userInfoStr) {
        const userInfo = JSON.parse(userInfoStr)
        userInfo.avatar = avatarPreview.value
        localStorage.setItem('userInfo', JSON.stringify(userInfo))
      }
      
      // 触发头像更新事件，通知首页刷新用户信息
      window.dispatchEvent(new CustomEvent('avatarUpdated'))
      
      // 跳转到城市列表页面（与后端保持一致）
      setTimeout(() => {
        router.push('/city')
      }, 1000)
    } else {
      throw new Error(`上传失败: ${response.status}`)
    }
  } catch (error: any) {
    console.error('头像上传失败:', error)
    ElMessage.error('头像上传失败，请重试')
  } finally {
    uploading.value = false
  }
}

// 组件挂载时获取用户信息
onMounted(() => {
  getUserInfo()
})
</script>

<style scoped>
@import './AvatarEdit.css';
</style>