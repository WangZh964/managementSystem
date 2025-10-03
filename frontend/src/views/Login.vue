<template>
  <div class="login-container">
    <!-- 浮动小方块背景 -->
    <div class="floating-cubes">
      <div class="cube"></div>
      <div class="cube"></div>
      <div class="cube"></div>
      <div class="cube"></div>
      <div class="cube"></div>
      <div class="cube"></div>
      <div class="cube"></div>
      <div class="cube"></div>
      <div class="cube"></div>
      <div class="cube"></div>
    </div>
    
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>中国移动用户管理系统</h2>
        </div>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="0"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="code">
          <div class="captcha-container">
            <el-input
              v-model="loginForm.code"
              placeholder="验证码"
              prefix-icon="Key"
              style="width: 200px;"
            />
            <div class="captcha-image" @click="refreshCaptcha">
              <img :src="captchaUrl" alt="验证码" />
            </div>
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" class="login-button" @click="handleLogin" :loading="loading">
            登录
          </el-button>
        </el-form-item>
        
        <div class="register-link">
          还没有账号？<router-link to="/register">立即注册</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login, getCaptcha } from '../api/user'

const router = useRouter()
const loginFormRef = ref()
const loading = ref(false)
const captchaUrl = ref('') // 验证码图片URL

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: '',
  code: ''
})

// 登录表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' }
  ]
}

// 刷新验证码
const refreshCaptcha = async () => {
  try {
    const response = await getCaptcha()
    const imageUrl = URL.createObjectURL(response.data)
    captchaUrl.value = imageUrl
  } catch (error) {
    console.error('获取验证码失败:', error)
    ElMessage.error('获取验证码失败')
  }
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true
      try {
        // 创建FormData对象
        const formData = new FormData()
        formData.append('username', loginForm.username)
        formData.append('password', loginForm.password)
        formData.append('code', loginForm.code)

        const response = await login(formData)
        
        if (response.data && response.data.code === 200) {
          ElMessage.success('登录成功')
          // 保存用户信息
          localStorage.setItem('userInfo', JSON.stringify(response.data.data.userInfo))
          
          // 跳转到首页
          router.push('/')
        } else {
          ElMessage.error(response.data?.message || '登录失败')
          refreshCaptcha() // 刷新验证码
        }
      } catch (error: any) {
        console.error('登录失败:', error)
        ElMessage.error('登录失败，请稍后重试')
        refreshCaptcha() // 刷新验证码
      } finally {
        loading.value = false
      }
    }
  })
}

// 页面加载时获取验证码
onMounted(() => {
  refreshCaptcha()
})
</script>

<style scoped>
@import '../assets/css/Login.css';
</style>