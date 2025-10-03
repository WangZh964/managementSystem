<template>
  <div class="city-add-container">
    <!-- 浮动形状装饰 -->
    <div class="floating-shape shape-1"></div>
    <div class="floating-shape shape-2"></div>
    <div class="floating-shape shape-3"></div>
    
    <!-- 返回首页按钮 -->
    <div class="back-to-home">
      <el-button type="primary" @click="goToHome" class="home-button">
        <el-icon><HomeFilled /></el-icon>
        点击返回首页
      </el-button>
    </div>
    
    <el-card class="city-card">
      <template #header>
        <div class="card-header">
          <el-icon><Plus /></el-icon>
          <span>添加城市</span>
        </div>
      </template>

      <el-form
        ref="cityFormRef"
        :model="cityForm"
        :rules="cityFormRules"
        label-width="80px"
        enctype="multipart/form-data"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="cityForm.name" placeholder="请输入城市名称" />
        </el-form-item>
        <el-form-item label="人口" prop="count">
          <el-input-number v-model="cityForm.count" :min="0" placeholder="请输入人口数量" />
        </el-form-item>
        <el-form-item label="Logo" prop="img">
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            :http-request="handleUpload"
            :before-upload="beforeAvatarUpload"
          >
            <img v-if="cityForm.img" :src="cityForm.img" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">提交</el-button>
          <el-button @click="resetForm">重置</el-button>
          <el-button @click="goBack">返回</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, HomeFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { addCity } from '@/api/city'
import type { City } from '@/api/city'
import axios from 'axios'

// 路由
const router = useRouter()

// 表单数据
const cityForm = reactive<City>({
  name: '',
  count: 0,
  img: ''
})

// 表单引用
const cityFormRef = ref()

// 表单验证规则
const cityFormRules = {
  name: [
    { required: true, message: '请输入城市名称', trigger: 'blur' },
    { min: 2, max: 32, message: '长度在 2 到 32 个字符', trigger: 'blur' }
  ],
  count: [
    { required: true, message: '请输入人口数量', trigger: 'blur' },
    { type: 'number', min: 0, message: '人口数量不能小于0', trigger: 'blur' }
  ],
  img: [
    { required: true, message: '请上传城市Logo', trigger: 'change' }
  ]
}

// 提交表单
const submitForm = async () => {
  if (!cityFormRef.value) return
  
  await cityFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        // 创建普通对象而不是FormData，因为图片已经通过单独接口上传
        const requestData = {
          name: cityForm.name,
          count: cityForm.count,
          img: cityForm.img // 这里发送的是图片URL字符串
        }
        
        const response = await addCity(requestData)
        if (response.data && response.data.code === 200) {
          ElMessage.success('添加成功')
          router.push('/city')
        } else {
          ElMessage.error(response.data.message || '添加失败')
        }
      } catch (error) {
        ElMessage.error('添加失败')
        console.error('添加失败:', error)
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  if (cityFormRef.value) {
    cityFormRef.value.resetFields()
  }
  Object.assign(cityForm, {
    name: '',
    count: 0,
    img: ''
  })
}

// 返回列表
const goBack = () => {
  router.push('/city')
}

// 返回首页
const goToHome = () => {
  router.push('/')
}

// 处理头像上传
const handleUpload = async (options: any) => {
  try {
    const formData = new FormData()
    formData.append('file', options.file)
    
    // 使用axios直接发送上传请求
    const response = await axios.post('/city/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    if (response.data && response.data.code === 200) {
      cityForm.img = response.data.data.url
      ElMessage.success('图片上传成功')
      options.onSuccess(response)
    } else {
      ElMessage.error(response.data.message || '图片上传失败')
      options.onError(new Error('图片上传失败'))
    }
  } catch (error) {
    console.error('图片上传失败:', error)
    ElMessage.error('图片上传失败')
    options.onError(error)
  }
}

// 处理头像上传前验证
const beforeAvatarUpload = (rawFile: any) => {
  const isJPG = rawFile.type === 'image/jpeg' || rawFile.type === 'image/png'
  const isLt2M = rawFile.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }
  return true
}
</script>

<style scoped>
@import './CityAdd.css';
</style>