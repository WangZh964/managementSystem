<template>
  <div class="register-container">
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
    
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <h2>管理员注册</h2>
        </div>
      </template>
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="0"
        class="register-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="确认密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="code">
          <div class="captcha-container">
            <el-input
              v-model="registerForm.code"
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
          <el-button type="primary" class="register-button" @click="handleRegister" :loading="loading">
            注册
          </el-button>
        </el-form-item>
        
        <div class="login-link">
          已有账号？<router-link to="/login">立即登录</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register, getCaptcha } from '../api/user'

const router = useRouter()
const registerFormRef = ref()
const loading = ref(false)
const captchaUrl = ref('') // 验证码图片URL

// 注册表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  code: '' // 验证码
})

// 注册表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在 3 到 20 个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在 6 到 20 个字符之间', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: string, callback: any) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
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

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true
      try {
        // 创建FormData对象
        const formData = new FormData()
        formData.append('username', registerForm.username)
        formData.append('password', registerForm.password)
        formData.append('confirm_password', registerForm.confirmPassword)
        formData.append('code', registerForm.code) // 添加验证码

        const response = await register(formData)
        
        if (response.data && response.data.code === 200) {
          ElMessage.success('注册成功，请登录')
          // 跳转到登录页
          router.push('/login')
        } else {
          ElMessage.error(response.data?.message || '注册失败')
          refreshCaptcha() // 刷新验证码
        }
      } catch (error: any) {
        console.error('注册失败:', error)
        ElMessage.error('注册失败，请稍后重试')
        refreshCaptcha() // 刷新验证码
      } finally {
        loading.value = false
      }
    }
  })
}


// 组件挂载时获取验证码
onMounted(() => {
  refreshCaptcha()
})
</script>

<style scoped>
@import '../assets/css/Register.css';
</style>